import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from tenacity import retry, stop_after_attempt, wait_exponential

from app.agents.state import GraphState

def get_chat_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.7  # Higher temp for conversational flow
    )

def chat_node(state: GraphState) -> dict:
    """
    LangGraph node dedicated to generating responses for conversational interactions.
    It combines RAG knowledge with conversation history and localized language generation.
    """
    llm = get_chat_llm()
    
    farm = state["farm_dict"]
    language = state["language"]
    rag_context = state.get("rag_context", "")

    # Convert dictionary history back into LangChain message objects
    raw_history = state.get("messages", [])
    lc_messages = []
    
    # Prepend Dynamic System Prompt
    system_instruction = f"""
You are the Farmasense AI AI Agricultural Assistant. Be conversational, brilliant, and helpful.
Strictly reply in {language}.

Farmer's Profile:
- Size: {farm.get('land_size_acres', 'Unknown')} acres
- Soil: {farm.get('soil_type', 'Unknown')}
- District: {farm.get('district', 'Unknown')}, {farm.get('state', 'Unknown')}
- Water Source: {farm.get('water_source', 'Unknown')}

Database Knowledge (RAG facts injected here):
{rag_context if rag_context else "No distinct knowledge found for this query."}
"""
    lc_messages.append(SystemMessage(content=system_instruction.strip()))
    
    # Rebuild history
    for msg in raw_history:
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "user":
            lc_messages.append(HumanMessage(content=content))
        elif role == "ai":
            lc_messages.append(AIMessage(content=content))
            
    # Append the absolute current message
    current_mes = state.get("current_message", "")
    if current_mes:
        lc_messages.append(HumanMessage(content=current_mes))
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1.5, min=2, max=6), reraise=True)
    def _invoke():
        return llm.invoke(lc_messages)

    try:
        response = _invoke()
        return {"chat_reply": response.content}
    except Exception as e:
        print(f"Chat Node Failure: {e}")
        return {"chat_reply": "I'm having trouble connecting to my agricultural database right now (API timeout). Please try again."}
