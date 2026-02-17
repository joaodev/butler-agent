from src.agent import run_agent_loop
from src.agent_configs import SYSTEM_PROMPT


def main():
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        user_message = input("[user]:").strip()

        # Check for exit commands
        if user_message.lower() in ["q", "quit", "exit"]:
            print("Goodbye!")
            break

        if not user_message:
            continue

        # Add a user message to context
        messages.append({"role": "user", "content": user_message})

        # Run agent loop
        assistant_text = run_agent_loop(messages)

        # Add assistant response to context
        messages.append({"role": "assistant", "content": assistant_text})

        print(f"[assistant]: {assistant_text}")

if __name__ == "__main__":
    main()