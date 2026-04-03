def test_rag_no_env(monkeypatch):
    from app.agents.rag import get_rag_context
    
    monkeypatch.delenv("MONGO_URI", raising=False)
    
    result = get_rag_context("test")
    assert result == ""


def test_agent_generate():
    from app.agents.advisory import farm_advisor
    
    class DummyFarm:
        name = "Test Farm"
        latitude = 1.0
        longitude = 2.0
    
    result = farm_advisor.generate_advisory(DummyFarm())
    
    assert "advisory_result" in result
    assert result["advisory_result"]["season"] == "Kharif"


def test_agent_chat():
    from app.agents.agent_advisory import farm_advisor
    
    class DummyFarm:
        name = "Test Farm"
    
    result = farm_advisor.chat(DummyFarm(), "Should I water?", [])
    
    assert "water" in result["chat_reply"].lower()