import pytest
from unittest.mock import patch, MagicMock

from app.agents.nodes.advisory import generate_advisory_node
from app.agents.state import GraphState
from app.agents.schemas import AdvisoryReport


@patch('app.agents.nodes.advisory.get_llm')
def test_generate_advisory_node_success(mock_get_llm):
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

    # Patch the entire chain at the prompt level - before | operator
    with patch('app.agents.nodes.advisory.ChatPromptTemplate') as mock_prompt_cls:
        mock_prompt = MagicMock()
        mock_prompt_cls.from_messages.return_value = mock_prompt

        mock_chain = MagicMock()
        mock_chain.invoke.return_value = mock_report
        mock_prompt.__or__ = MagicMock(return_value=mock_chain)  # prompt | structured_llm

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
    with patch('app.agents.nodes.advisory.ChatPromptTemplate') as mock_prompt_cls:
        mock_prompt = MagicMock()
        mock_prompt_cls.from_messages.return_value = mock_prompt

        mock_chain = MagicMock()
        mock_chain.invoke.side_effect = Exception("LLM Timeout")
        mock_prompt.__or__ = MagicMock(return_value=mock_chain)

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