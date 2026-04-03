def test_agent_generate():
    from app.agents.nodes.advisory import generate_advisory_node  
    
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
    
    state = {
        "farm_dict": {"district": "Test"},
        "language": "English",
        "messages": [],
        "current_message": "Should I water?",
        "rag_context": ""
    }
    
    result = chat_node(state)
    
    assert "water" in result["chat_reply"].lower()