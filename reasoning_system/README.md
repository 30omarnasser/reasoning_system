```markdown
# Reasoning System 🧠

A modular multi-step reasoning system built with **Llama 3.1:8b** (via Ollama) supporting three reasoning strategies:

- **CoT** — Chain-of-Thought
- **ReAct** — Reason + Act (with tool use)
- **ToT** — Tree of Thoughts (beam search)

---

## Project Structure

```
reasoning_system/
│
├── core/
│   ├── base_agent.py       # Abstract base class for all agents
│   ├── llm_client.py       # Ollama client wrapper
│   ├── memory.py           # Step-by-step memory store
│   ├── tools.py            # Tool registry (search, calculator)
│   └── prompts.py          # All system prompts
│
├── strategies/
│   ├── cot.py              # Chain-of-Thought agent
│   ├── react.py            # ReAct agent
│   ├── tot.py              # Tree of Thoughts agent
│   └── evaluator.py        # ToT branch scorer
│
├── tests/
│   ├── test_cot.py
│   ├── test_react.py
│   └── test_tot.py
│
├── config/
│   └── settings.py         # Pydantic settings (model, temperature, etc.)
│
├── main.py                 # CLI entry point
├── requirements.txt
└── README.md
```

---

## Reasoning Strategies

### Chain-of-Thought (CoT)
Linear step-by-step reasoning. The model thinks aloud before giving a final answer. Best for math, logic, and structured problems.

```
Question → Thought 1 → Thought 2 → ... → Final Answer
```

### ReAct (Reason + Act)
Interleaves reasoning with real tool calls. The model loops through Thought → Action → Observation until it has enough information to answer. Best for factual questions and agentic tasks.

```
Question → Thought → Action → Observation → Thought → ... → Final Answer
```

### Tree of Thoughts (ToT)
Beam search over reasoning branches. The model generates multiple candidate next steps, scores each with an evaluator, prunes weak paths, and expands the best ones. Best for planning, puzzles, and problems that require backtracking.

```
Problem
├── Branch A (score: 0.9) → expand
│   ├── A1 (score: 0.8) → expand → Final Answer
│   └── A2 (score: 0.3) → pruned
├── Branch B (score: 0.5) → pruned
└── Branch C (score: 0.2) → pruned
```

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- Llama 3.1:8b pulled

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/30omarnasser/reasoning_system.git
cd reasoning_system

# 2. Install dependencies
pip install -r requirements.txt

# 3. Pull the model
ollama pull llama3.1:8b

# 4. Run
python main.py
```

---

## Usage

```bash
python main.py
```

```
==================================================
  Reasoning System  —  llama3.1:8b via Ollama
==================================================
Strategies: cot | react | tot

Strategy: react
Question: What is the population of Egypt?

Thinking...

Answer:
The population of Egypt is approximately 105 million people.
```

---

## Configuration

Edit `config/settings.py` or create a `.env` file:

```env
MODEL_NAME=llama3.1:8b
OLLAMA_HOST=http://localhost:11434
TEMPERATURE=0.7
MAX_TOKENS=2048
MAX_ITERATIONS=10
TOT_BRANCHES=3
TOT_DEPTH=3
TOT_BEAM_WIDTH=2
```

| Setting | Default | Description |
|---|---|---|
| `MODEL_NAME` | `llama3.1:8b` | Ollama model to use |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `TEMPERATURE` | `0.7` | Sampling temperature |
| `MAX_TOKENS` | `2048` | Max tokens per response |
| `MAX_ITERATIONS` | `10` | ReAct loop limit |
| `TOT_BRANCHES` | `3` | Candidates generated per ToT level |
| `TOT_DEPTH` | `3` | Maximum tree depth |
| `TOT_BEAM_WIDTH` | `2` | Beams kept after pruning |

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Adding a Custom Tool

In `core/tools.py`, register any Python function:

```python
def my_tool(input: str) -> str:
    return f"Result for {input}"

registry = ToolRegistry()
registry.register("my_tool", my_tool)
```

It will automatically be available to the ReAct agent.

---

## Adding a New Strategy

1. Create `strategies/my_strategy.py`
2. Inherit from `BaseAgent` and implement `run()`
3. Register it in `main.py`

```python
from core.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def run(self, question: str) -> str:
        messages = [{"role": "user", "content": question}]
        return self._chat(messages)
```

```python
# main.py
AGENTS = {
    "cot":   CoTAgent,
    "react": ReActAgent,
    "tot":   ToTAgent,
    "mine":  MyAgent,   # add here
}
```

---

## Strategy Comparison

| | CoT | ReAct | ToT |
|---|---|---|---|
| Search style | Linear | Iterative loop | Beam search |
| Tool use | No | Yes | No |
| Backtracks | No | No | Yes |
| Speed | Fast | Medium | Slow |
| Best for | Math / logic | Search / agents | Planning / puzzles |

---

## License

MIT

---

## Author

[@30omarnasser](https://github.com/30omarnasser)
```
