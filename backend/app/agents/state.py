from typing import TypedDict, List, Dict, Any, Optional
from operator import add
from typing_extensions import Annotated

class GraphState(TypedDict):
    """
    The main LangGraph state dictionary.
    """
    # Inputs
    farm_dict: Dict[str, Any]
    language: str
    request_type: str # 'advisory' or 'chat'
    
    # Chat specific
    messages: List[Dict[str, Any]]
    current_message: str
    
    # RAG
    rag_context: str
    
    # Output
    advisory_result: Optional[Dict[str, Any]]
    chat_reply: Optional[str]
