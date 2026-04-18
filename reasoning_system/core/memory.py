from dataclasses import dataclass, field

@dataclass
class Step:
    role: str
    content: str

class Memory:
    def __init__(self):
        self._steps: list[Step] = []

    def add(self, role: str, content: str) -> None:
        self._steps.append(Step(role=role, content=content))

    def get_all(self) -> list[Step]:
        return list(self._steps)

    def to_messages(self, system_prompt: str) -> list[dict]:
        msgs = [{"role": "system", "content": system_prompt}]
        for s in self._steps:
            role = "assistant" if s.role in ("thought", "answer") else "user"
            msgs.append({"role": role, "content": f"[{s.role.upper()}] {s.content}"})
        return msgs

    def clear(self) -> None:
        self._steps.clear()