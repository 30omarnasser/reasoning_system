from unittest.mock import patch, MagicMock
from strategies.react import ReActAgent

def make_agent(responses: list[str]) -> ReActAgent:
    with patch("core.llm_client.ollama.Client") as MockClient:
        instance = MockClient.return_value
        instance.chat.side_effect = [
            {"message": {"content": r}} for r in responses
        ]
        return ReActAgent()

def test_react_direct_answer():
    with patch("core.llm_client.ollama.Client") as MockClient:
        instance = MockClient.return_value
        instance.chat.return_value = {
            "message": {"content": "Thought: I know this.\nFinal Answer: 4"}
        }
        agent = ReActAgent()
        result = agent.run("What is 2+2?")
        assert result == "4"

def test_react_uses_tool():
    responses = [
        "Thought: I need to calculate.\nAction: calculator\nAction Input: 10 * 5",
        "Thought: I have the result.\nFinal Answer: 50",
    ]
    with patch("core.llm_client.ollama.Client") as MockClient:
        instance = MockClient.return_value
        instance.chat.side_effect = [
            {"message": {"content": r}} for r in responses
        ]
        agent = ReActAgent()
        result = agent.run("What is 10 times 5?")
        assert result == "50"