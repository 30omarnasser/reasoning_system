from core.base_agent import BaseAgent
from core.prompts import COT_SYSTEM

class CoTAgent(BaseAgent):
    """Chain-of-Thought: linear step-by-step reasoning."""

    def run(self, question: str) -> str:
        messages = [
            {"role": "system", "content": COT_SYSTEM},
            {"role": "user",   "content": question},
        ]
        response = self._chat(messages)
        self.memory.add("answer", response)
        return self._extract_answer(response)

    def _extract_answer(self, text: str) -> str:
        for line in reversed(text.splitlines()):
            if line.lower().startswith("final answer:"):
                return line.split(":", 1)[1].strip()
        return text