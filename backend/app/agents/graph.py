import os
from langgraph.graph import StateGraph, START, END

from app.agents.state import GraphState
from app.agents.rag import get_rag_context
from app.agents.nodes.chat import chat_node
from app.agents.nodes.advisory import generate_advisory_node

def retrieve_rag_node(state: GraphState) -> dict:
    """
    Node that hooks to MongoDB Atlas Vector Search.
    Injects knowledge back into the graph state before LLM generation.
    """
    farm = state["farm_dict"]
    loc = f"{farm.get('district', '')}, {farm.get('state', '')}"
    
    # Decide what to search based on workflow
    if state["request_type"] == "chat":
        query = state.get("current_message", "")
    else:
        query = f"Best crop practices for {farm.get('soil_type', '')} soil, {farm.get('land_size_acres')} acres."
        
    knowledge = get_rag_context(query, state_or_district=loc)
    return {"rag_context": knowledge}

def build_farmasense_graph():
    """
    Compiles the Master LangGraph.
    Routing happens based on the request_type parameter in state.
    """
    workflow = StateGraph(GraphState)
    
    # 1. State nodes
    workflow.add_node("rag_retrieval", retrieve_rag_node)
    workflow.add_node("advisory_generation", generate_advisory_node)
    workflow.add_node("chat_generation", chat_node)
    
    # 2. Logic Router
    def edge_router(state: GraphState):
        if state["request_type"] == "advisory":
            return "advisory_generation"
        return "chat_generation"
    
    # 3. Wire the graph
    workflow.add_edge(START, "rag_retrieval")
    # Conditionally route from RAG to either chat or advisory
    workflow.add_conditional_edges("rag_retrieval", edge_router)
    
    # Conclude
    workflow.add_edge("advisory_generation", END)
    workflow.add_edge("chat_generation", END)
    
    compiled_app = workflow.compile()
    return compiled_app

# Singleton instance for high performance
farm_graph = build_farmasense_graph()
