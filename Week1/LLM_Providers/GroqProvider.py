from groq import Groq
import os

class GroqProvider():

    def __init__(self):
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set in environment.")
        self._client = Groq(api_key=api_key)
        self._model = os.getenv("GROQ_MODEL")
        

    def call(self, user_prompt: str, history: list ):

        history.append({"role": "user", "content": user_prompt})
        stream = self._client.chat.completions.create(
            model=str(self._model),
            max_completion_tokens=1024,
            messages= history,
            stream=True
        )
        ai_reply = ''
        
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                ai_reply += content
                print(content, end="", flush=True)
                
        history.append({"role": "assistant", "content": ai_reply})
        