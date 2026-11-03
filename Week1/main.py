from pathlib import Path
from dotenv import load_dotenv
from LLM_Providers.GroqProvider import GroqProvider

SYSTEM_PROMPT_PATH = Path(__file__).parent / "system_prompt.txt"


def main():
    """Main execution function for the script."""
    load_dotenv()

    conversation_history = []
    content = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    conversation_history.append({"role": "system", "content": content})

    groq_provider = GroqProvider()

    while True:
        # 1. Wait for user input
        user_input = input("Enter something (or type 'exit' to quit): ")

        # 2. Check for the exit condition (case-insensitive and strips extra spaces)
        if user_input.strip().lower() == 'exit':
            print("Goodbye!")
            break  # Exits the loop immediately

        for piece in groq_provider.call(user_input, conversation_history):
            print(piece, end="", flush=True)
        print()  # the last chunk usually has no trailing newline

        usage = groq_provider.last_usage
        if usage:
            print(f"Input Tokens (Prompt): {usage.prompt_tokens}")
            print(f"Output Tokens (Completion): {usage.completion_tokens}")
            print(f"Total Tokens: {usage.total_tokens}")
            print(f"Total Cost: {usage.cost_usd:.6f} USD")


# This starts the script
if __name__ == "__main__":
    main()
