import os
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )

def generate_advisory(farm_dict, language="English"):
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert agricultural consultant in India. 
Return the advisory EXCLUSIVELY in valid JSON format with the following keys:
- 'season' (string)
- 'recommended_crop' (string)
- 'second_option_crop' (string)
- 'avoid_crop' (string)
- 'expected_profit_min' (integer)
- 'expected_profit_max' (integer)
- 'confidence_score' (float 0-1)
- 'final_advisory' (A detailed 3 paragraph advisory report). 

DO NOT include any markdown formatting like ```json or newlines outside the JSON string, just return raw JSON text. 
CRITICAL: The values for 'season', 'recommended_crop', 'second_option_crop', 'avoid_crop', and 'final_advisory' MUST BE TRANSLATED AND WRITTEN ENTIRELY IN {language}."""),
        ("human", "Farm size: {land_size_acres} acres. Soil: {soil_type}. District: {district}, {state}. Water: {water_source}. Generate advisory.")
    ])
    chain = prompt | llm
    
    @retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1.5, min=2, max=10), reraise=True)
    def _invoke_chain():
        return chain.invoke({
            "language": language,
            "land_size_acres": farm_dict.get("land_size_acres", 1),
            "soil_type": farm_dict.get("soil_type", "Unknown"),
            "district": farm_dict.get("district", "Unknown"),
            "state": farm_dict.get("state", "Unknown"),
            "water_source": farm_dict.get("water_source", "Unknown")
        })

    try:
        res = _invoke_chain()
    except Exception as e:
        print(f"CRITICAL: AI generation failed completely after retries: {e}")
        return {
            "season": "Upcoming",
            "recommended_crop": "Network timeout, please try again",
            "second_option_crop": "-",
            "avoid_crop": "-",
            "expected_profit_min": 0,
            "expected_profit_max": 0,
            "confidence_score": 0.0,
            "final_advisory": f"Internal Error: API timeouts ({e})"
        }
    
    content = res.content.strip()
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
        
    try:
        data = json.loads(content)
        return data
    except Exception as e:
        print("Error parsing JSON:", e)
        print("Raw Content:", res.content)
        return {
            "season": "Upcoming",
            "recommended_crop": "Parse Error",
            "second_option_crop": "-",
            "avoid_crop": "-",
            "expected_profit_min": 0,
            "expected_profit_max": 0,
            "confidence_score": 0.5,
            "final_advisory": content
        }

def chat_with_advisory(farm_dict, history, message, language="English"):
    llm = get_llm()
    
    messages = [
        SystemMessage(content=f"You are a helpful agricultural AI assistant for a farmer in India. The farmer's farm details: Size: {farm_dict.get('land_size_acres', 'Unknown')} acres. Soil: {farm_dict.get('soil_type', 'Unknown')}. Location: {farm_dict.get('district', 'Unknown')}, {farm_dict.get('state', 'Unknown')}. Water: {farm_dict.get('water_source', 'Unknown')}. You must reply naturally and exclusively in {language}. Keep responses concise, supportive, and helpful.")
    ]
    
    for msg in history:
        if msg.get("role") == "user":
            messages.append(HumanMessage(content=msg.get("content")))
        else:
            messages.append(AIMessage(content=msg.get("content")))
            
    messages.append(HumanMessage(content=message))
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6), reraise=True)
    def _invoke_chat():
        return llm.invoke(messages)
    
    try:
        res = _invoke_chat()
        return res.content
    except Exception as e:
        return "I'm having trouble connecting to my agricultural database right now (API timeout). Please ask your question again in a minute."
