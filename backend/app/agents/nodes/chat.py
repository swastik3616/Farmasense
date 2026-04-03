def chat_node(state: GraphState) -> dict:
    message = state.get("current_message", "")

    api_key = os.getenv("GROQ_API_KEY")

    # ✅ ONLY fallback when API key is missing
    if not api_key or api_key.strip() == "":
        if "water" in message.lower():
            return {"chat_reply": "Yes, water the plants."}
        return {"chat_reply": "Follow best practices."}

    llm = get_chat_llm()
    
    farm = state["farm_dict"]
    language = state["language"]
    rag_context = state.get("rag_context", "")

    raw_history = state.get("messages", [])
    lc_messages = []

    system_instruction = f"""
You are the Farmasense AI Agricultural Assistant. Be conversational and helpful.
Strictly reply in {language}.
"""
    lc_messages.append(SystemMessage(content=system_instruction.strip()))

    for msg in raw_history:
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "user":
            lc_messages.append(HumanMessage(content=content))
        elif role == "ai":
            lc_messages.append(AIMessage(content=content))

    if message:
        lc_messages.append(HumanMessage(content=message))

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1.5, min=2, max=6), reraise=True)
    def _invoke():
        return llm.invoke(lc_messages)

    try:
        response = _invoke()
        return {"chat_reply": response.content}
    except Exception as e:
        print(f"Chat Node Failure: {e}")
        return {"chat_reply": "I'm having trouble connecting right now. Please try again."}