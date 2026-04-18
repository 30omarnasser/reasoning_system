import json
import re
from core.base_agent import BaseAgent
from core.prompts import TOT_GENERATE
from strategies.evaluator import ThoughtEvaluator
from config.settings import settings

class ToTAgent(BaseAgent):
    """Tree of Thoughts: beam search over reasoning branches."""

    def __init__(self):
        super().__init__()
        self.evaluator = ThoughtEvaluator()

    def run(self, question: str) -> str:
        beams: list[list[str]] = [[]]

        for depth in range(settings.tot_depth):
            candidates: list[tuple[float, list[str]]] = []

            for path in beams:
                expansions = self._expand(question, path)
                for step in expansions:
                    score = self.evaluator.score(question, step)
                    candidates.append((score, path + [step]))

            candidates.sort(key=lambda x: x[0], reverse=True)
            beams = [path for _, path in candidates[: settings.tot_beam_width]]

            if beams and self._is_terminal(beams[0][-1]):
                break

        best_path = beams[0] if beams else []
        return self._synthesize(question, best_path)

    def _expand(self, problem: str, path: list[str]) -> list[str]:
        path_str = (
            "\n".join(f"Step {i+1}: {s}" for i, s in enumerate(path))
            or "None yet."
        )
        prompt = TOT_GENERATE.format(
            problem=problem,
            path=path_str,
            n=settings.tot_branches,
        )
        messages = [{"role": "user", "content": prompt}]
        raw = self.llm.complete(messages)

        # Strip markdown fences Llama sometimes adds
        clean = re.sub(r"```(?:json)?|```", "", raw).strip()
        try:
            steps = json.loads(clean)
            return [str(s) for s in steps]
        except json.JSONDecodeError:
            # Fallback: split by newline and treat each as a branch
            return [line.strip() for line in clean.splitlines() if line.strip()]

    def _is_terminal(self, step: str) -> bool:
        keywords = ("final answer", "conclusion", "therefore", "in summary")
        return any(kw in step.lower() for kw in keywords)

    def _synthesize(self, problem: str, path: list[str]) -> str:
        path_str = "\n".join(f"Step {i+1}: {s}" for i, s in enumerate(path))
        messages = [
            {
                "role": "system",
                "content": "Synthesize the reasoning path into a clear, concise final answer.",
            },
            {
                "role": "user",
                "content": f"Problem: {problem}\n\nReasoning path:\n{path_str}",
            },
        ]
        return self.llm.complete(messages)