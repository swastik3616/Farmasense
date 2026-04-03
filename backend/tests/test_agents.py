import pytest
from unittest.mock import patch, MagicMock

from app.agents.nodes.advisory import generate_advisory_node
from app.agents.state import GraphState
from app.agents.schemas import AdvisoryReport

@patch('app.agents.nodes.advisory.get_llm')
def test_generate_advisory_node_mocked_llm(mock_get_llm):
    """
    Test the LangChain integration explicitly by mocking the Groq API call 
    and returning a fake structured payload.
    """
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    
    # Setup mock chain
    mock_get_llm.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_structured_llm
    
    # When the chain is invoked in the node, return this Pydantic object
    mock_chain_invoke = MagicMock()
    mock_chain_invoke.return_value = AdvisoryReport(
        season="Rabi",
        recommended_crop="Wheat",
        second_option_crop="Mustard",
        avoid_crop="Rice",
        expected_profit_min=10000,
        expected_profit_max=15000,
        confidence_score=0.9,
        final_advisory="Test string"
    )
    
    # Alternatively, we patch the chain invoke entirely:
    with patch('langchain_core.runnables.base.RunnableSequence.invoke', return_value=mock_chain_invoke.return_value):
        state: GraphState = {
            "farm_dict": {"land_size_acres": 5, "soil_type": "Clay", "district": "Test", "state": "Test", "water_source": "Rain"},
            "language": "English",
            "request_type": "advisory",
            "messages": [],
            "current_message": ""
        }
        
        result = generate_advisory_node(state)
        
        # Verify the node wrapped the logic and returned the structured advisory result
        assert "advisory_result" in result
        assert result["advisory_result"]["recommended_crop"] == "Wheat"
        assert result["advisory_result"]["confidence_score"] == 0.9

@patch('app.agents.nodes.chat.get_chat_llm')
def test_chat_node_mocked_llm(mock_get_chat_llm):
    mock_llm = MagicMock()
    mock_get_chat_llm.return_value = mock_llm
    
    # Mock return value of chat LLM
    mock_response = MagicMock()
    mock_response.content = "Mocked chat response"
    mock_llm.invoke.return_value = mock_response
    
    state: GraphState = {
        "farm_dict": {"land_size_acres": 5, "soil_type": "Clay", "district": "Test", "state": "Test", "water_source": "Rain"},
        "language": "English",
        "request_type": "chat",
        "messages": [],
        "current_message": "Hello"
    }
    
    from app.agents.nodes.chat import chat_node
    result = chat_node(state)
    
    assert "chat_reply" in result
    assert result["chat_reply"] == "Mocked chat response"
