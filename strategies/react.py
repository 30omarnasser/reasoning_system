import re
from core.base_agent import BaseAgent
from core.prompts import REACT_SYSTEM
from config.settings import settings

class ReActAgent(BaseAgent):
    """ReAct: interleaved Thought → Action → Observation loop."""

    def run(self, question: str) -> str:
        system = REACT_SYSTEM.format(tools=self.tools.list_tools())
        messages = [
            {"role": "system", "content": system},
            {"role": "user",   "content": question},
        ]

        for i in range(settings.max_iterations):
            response = self._chat(messages)
            messages.append({"role": "assistant", "content": response})
            self.memory.add("thought", response)

            if "Final Answer:" in response:
                return self._extract_answer(response)

            action, action_input = self._parse_action(response)
            if not action:
                # Llama sometimes skips formatting — prompt it back on track
                messages.append({
                    "role": "user",
                    "content": (
                        "Please continue using the Thought/Action/Action Input format, "
                        "or write 'Final Answer:' if you are done."
                    ),
                })
                continue

            observation = self.tools.call(action, action_input)
            self.memory.add("observation", observation)
            messages.append({"role": "user", "content": f"Observation: {observation}"})

        return "Max iterations reached without a final answer."

    def _parse_action(self, text: str) -> tuple[str, str]:
        action_match = re.search(r"Action:\s*(.+)",       text)
        input_match  = re.search(r"Action Input:\s*(.+)", text)
        if action_match and input_match:
            return action_match.group(1).strip(), input_match.group(1).strip()
        return "", ""

    def _extract_answer(self, text: str) -> str:
        match = re.search(r"Final Answer:\s*(.+)", text, re.DOTALL)
        return match.group(1).strip() if match else text