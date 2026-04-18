import pytest
from unittest.mock import patch, MagicMock
from strategies.cot import CoTAgent

@pytest.fixture
def mock_llm(monkeypatch):
    mock = MagicMock()
    mock.complete.return_value = (
        "Thought 1: Let me think...\nFinal Answer: 42"
    )
    monkeypatch.setattr("core.llm_client.ollama.Client", lambda **_: mock)
    return mock

def test_cot_returns_string():
    with patch("core.llm_client.ollama.Client") as MockClient:
        instance = MockClient.return_value
        instance.chat.return_value = {
            "message": {"content": "Thought 1: ...\nFinal Answer: Paris"}
        }
        agent = CoTAgent()
        result = agent.run("What is the capital of France?")
        assert isinstance(result, str)
        assert result == "Paris"

def test_cot_fallback_no_final_answer():
    with patch("core.llm_client.ollama.Client") as MockClient:
        instance = MockClient.return_value
        instance.chat.return_value = {
            "message": {"content": "I think the answer is Paris."}
        }
        agent = CoTAgent()
        result = agent.run("Capital of France?")
        assert "Paris" in result