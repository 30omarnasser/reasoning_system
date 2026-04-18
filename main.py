from strategies.cot   import CoTAgent
from strategies.react import ReActAgent
from strategies.tot   import ToTAgent

AGENTS = {
    "cot":   CoTAgent,
    "react": ReActAgent,
    "tot":   ToTAgent,
}

def main():
    print("=" * 50)
    print("  Reasoning System  —  llama3.1:8b via Ollama")
    print("=" * 50)
    print("Strategies: cot | react | tot\n")

    strategy = input("Strategy: ").strip().lower()
    question = input("Question: ").strip()

    AgentClass = AGENTS.get(strategy)
    if not AgentClass:
        print(f"Unknown strategy '{strategy}'. Choose from: {list(AGENTS)}")
        return

    agent = AgentClass()
    print("\nThinking...\n")
    answer = agent.run(question)
    print(f"Answer:\n{answer}")

if __name__ == "__main__":
    main()