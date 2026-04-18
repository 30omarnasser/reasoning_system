from unittest.mock import patch, MagicMock
from strategies.tot import ToTAgent

def test_tot_returns_string():
    with patch("core.llm_client.ollama.Client") as MockClient:
        instance = MockClient.return_value
        instance.chat.return_value = {
            "message": {
                "content": '["step A", "step B", "step C"]'
            }
        }
        agent = ToTAgent()
        result = agent.run("What is the best way to learn Python?")
        assert isinstance(result, str)