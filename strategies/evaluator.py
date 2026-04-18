import json
import re
from core.llm_client import LLMClient
from core.prompts import TOT_EVALUATE

class ThoughtEvaluator:
    def __init__(self):
        self.llm = LLMClient()

    def score(self, problem: str, step: str) -> float:
        prompt = TOT_EVALUATE.format(problem=problem, step=step)
        messages = [{"role": "user", "content": prompt}]
        raw = self.llm.complete(messages)

        # Llama sometimes wraps JSON in markdown — strip it
        clean = re.sub(r"```(?:json)?|```", "", raw).strip()
        try:
            data = json.loads(clean)
            return max(0.0, min(1.0, float(data.get("score", 0.0))))
        except (json.JSONDecodeError, ValueError):
            return 0.0