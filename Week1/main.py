import os
from dotenv import load_dotenv
from LLM_Providers.GroqProvider import GroqProvider

def main():
    """Main execution function for the script."""
    load_dotenv()

    conversation_history = [
            {"role": "system", "content": "You are a helpful and concise AI assistant."}
        ]
    
    while True:
        # 1. Wait for user input
        user_input = input("Enter something (or type 'exit' to quit): ")
        
        # 2. Check for the exit condition (case-insensitive and strips extra spaces)
        if user_input.strip().lower() == 'exit':
            print("Goodbye!")
            break  # Exits the loop immediately
            
        groq_provider = GroqProvider()
        resp = groq_provider.call(user_input, conversation_history)
        print(resp)

# This starts the script
if __name__ == "__main__":
    main()