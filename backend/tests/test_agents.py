import pytest
from unittest.mock import patch, MagicMock

from app.agents.nodes.advisory import generate_advisory_node
from app.agents.state import GraphState
from app.agents.schemas import AdvisoryReport


@patch('app.agents.nodes.advisory.get_llm')
def test_generate_advisory_node_success(mock_get_llm):
    """Test successful advisory generation with mocked LLM."""
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    mock_get_llm.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_structured_llm

    mock_report = AdvisoryReport(
        season="Rabi",
        recommended_crop="Wheat",
        second_option_crop="Mustard",
        avoid_crop="Rice",
        expected_profit_min=10000,
        expected_profit_max=15000,
        confidence_score=0.9,
        final_advisory="Test advice"
    )

    mock_chain = MagicMock()
    mock_chain.invoke.return_value = mock_report
    mock_structured_llm.__ror__ = MagicMock(return_value=mock_chain)

    state: GraphState = {
        "farm_dict": {"land_size_acres": 5, "soil_type": "Clay", "district": "Test", "state": "Test", "water_source": "Rain"},
        "language": "English",
        "request_type": "advisory",
        "messages": [],
        "current_message": ""
    }

    result = generate_advisory_node(state)

    assert "advisory_result" in result
    assert result["advisory_result"]["recommended_crop"] == "Wheat"
    assert result["advisory_result"]["confidence_score"] == 0.9


@patch('app.agents.nodes.advisory.get_llm')
def test_generate_advisory_node_fallback(mock_get_llm):
    """Test advisory node fallback when LLM fails."""
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    mock_get_llm.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_structured_llm

    mock_chain = MagicMock()
    mock_chain.invoke.side_effect = Exception("LLM Timeout")
    mock_structured_llm.__ror__ = MagicMock(return_value=mock_chain)

    state: GraphState = {
        "farm_dict": {"land_size_acres": 5, "soil_type": "Clay", "district": "Test", "state": "Test", "water_source": "Rain"},
        "language": "English",
        "request_type": "advisory",
        "messages": [],
        "current_message": ""
    }

    result = generate_advisory_node(state)

    assert "advisory_result" in result
    assert result["advisory_result"]["recommended_crop"] == "Service Degraded"
    assert "LLM Timeout" in result["advisory_result"]["final_advisory"]


@patch('app.agents.nodes.chat.get_chat_llm')
def test_chat_node_success(mock_get_chat_llm):
    """Test successful chat response."""
    mock_llm = MagicMock()
    mock_get_chat_llm.return_value = mock_llm

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