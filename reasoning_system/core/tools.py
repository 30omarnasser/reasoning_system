import json
from typing import Callable

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Callable] = {}
        self._register_defaults()

    def _register_defaults(self):
        self.register("search", self._mock_search)
        self.register("calculator", self._calculator)

    def register(self, name: str, fn: Callable) -> None:
        self._tools[name] = fn

    def call(self, name: str, args: str) -> str:
        if name not in self._tools:
            return f"Error: tool '{name}' not found."
        try:
            parsed = json.loads(args) if args.strip().startswith("{") else {"input": args}
            return str(self._tools[name](**parsed))
        except Exception as e:
            return f"Tool error: {e}"

    def list_tools(self) -> str:
        return ", ".join(self._tools.keys())

    @staticmethod
    def _mock_search(input: str) -> str:
        return f"[Search result for '{input}': placeholder — wire a real API here]"

    @staticmethod
    def _calculator(expression: str) -> str:
        try:
            return str(eval(expression, {"__builtins__": {}}))
        except Exception as e:
            return f"Calc error: {e}"