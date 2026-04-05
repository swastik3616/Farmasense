from unittest.mock import patch, MagicMock
from app.agents.schemas import AdvisoryReport


def test_agent_generate():
    from app.agents.nodes.advisory import generate_advisory_node

    mock_report = AdvisoryReport(
        season="Kharif",
        recommended_crop="Rice",
        second_option_crop="Maize",
        avoid_crop="Wheat",
        expected_profit_min=8000,
        expected_profit_max=12000,
        confidence_score=0.85,
        final_advisory="Kharif season advice."
    )

    with patch('app.agents.nodes.advisory.ChatPromptTemplate') as mock_prompt_cls:
        mock_prompt = MagicMock()
        mock_prompt_cls.from_messages.return_value = mock_prompt

        mock_chain = MagicMock()
        mock_chain.invoke.return_value = mock_report
        mock_prompt.__or__ = MagicMock(return_value=mock_chain)

        with patch('app.agents.nodes.advisory.get_llm'):
            state = {
                "farm_dict": {
                    "land_size_acres": 1.0,
                    "soil_type": "Loamy",
                    "district": "Test",
                    "state": "Test",
                    "water_source": "Well"
                },
                "language": "English",
                "rag_context": ""
            }

            result = generate_advisory_node(state)

            assert "advisory_result" in result
            assert result["advisory_result"]["season"] == "Kharif"


def test_agent_chat():
    from app.agents.nodes.chat import chat_node

    mock_response = MagicMock()
    mock_response.content = "You should water your crops carefully."

    mock_llm = MagicMock()
    mock_llm.invoke.return_value = mock_response

    with patch('app.agents.nodes.chat.get_chat_llm', return_value=mock_llm):
        state = {
            "farm_dict": {"district": "Test"},
            "language": "English",
            "messages": [],
            "current_message": "Should I water?",
            "rag_context": ""
        }

        result = chat_node(state)

        assert "water" in result["chat_reply"].lower()