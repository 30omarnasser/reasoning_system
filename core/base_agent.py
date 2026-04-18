from abc import ABC, abstractmethod
from core.llm_client import LLMClient
from core.memory import Memory
from core.tools import ToolRegistry

class BaseAgent(ABC):
    def __init__(self):
        self.llm = LLMClient()
        self.memory = Memory()
        self.tools = ToolRegistry()

    @abstractmethod
    def run(self, question: str) -> str:
        ...

    def _chat(self, messages: list[dict]) -> str:
        return self.llm.complete(messages)