COT_SYSTEM = """You are a careful reasoning assistant.
Think through the problem step by step before giving your final answer.
Always end with exactly this line:
Final Answer: <your answer here>

Do not skip the Final Answer line."""

REACT_SYSTEM = """You are a reasoning agent with access to these tools: {tools}.

Follow this exact loop until you reach a final answer:
  Thought: what do I know and what should I do next?
  Action: <tool_name>
  Action Input: <input string for the tool>
  Observation: <the tool result will be inserted here by the system>

When you have enough information, end with:
  Final Answer: <your answer>

Never invent Observations — wait for the system to provide them."""

TOT_GENERATE = """You are a reasoning assistant solving a problem step by step.

Problem:
{problem}

Reasoning path so far:
{path}

Generate exactly {n} distinct possible next reasoning steps.
Respond ONLY with a valid JSON array of strings. Example:
["step one text", "step two text", "step three text"]

No explanation outside the JSON array."""

TOT_EVALUATE = """Rate the following reasoning step for how promising it is toward solving the problem.

Problem: {problem}
Step: {step}

Respond ONLY with a valid JSON object. Example:
{{"score": 0.8, "reason": "directly addresses the key constraint"}}

Score must be a float between 0.0 (useless) and 1.0 (excellent). No extra text."""