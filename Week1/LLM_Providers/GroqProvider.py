from dataclasses import dataclass
from groq import Groq
import os
from typing import Iterator

# USD per 1M tokens: (input, output). Source: https://console.groq.com/docs/models
PRICING = {
    "openai/gpt-oss-120b": (0.15, 0.60),
}


@dataclass
class Usage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost_usd: float = 0.0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


class GroqProvider:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set in environment.")

        model = os.getenv("GROQ_MODEL")
        if not model:
            raise RuntimeError("GROQ_MODEL is not set in environment.")
        if model not in PRICING:
            raise RuntimeError(
                f"No pricing configured for model '{model}'. Add it to PRICING."
            )

        self._client = Groq(api_key=api_key)
        self._model = model
        self.last_usage: Usage | None = None

    def call(self, user_prompt: str, history: list) -> Iterator[str]:
        self.last_usage = None
        history.append({"role": "user", "content": user_prompt})
        stream = self._client.chat.completions.create(
            model=self._model,
            max_completion_tokens=1024,
            messages=history,
            stream=True,
        )

        ai_reply = ""
        prompt_tokens = 0
        completion_tokens = 0

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                ai_reply += content
                yield content
            if chunk.x_groq and chunk.x_groq.usage:
                prompt_tokens = chunk.x_groq.usage.prompt_tokens
                completion_tokens = chunk.x_groq.usage.completion_tokens

        history.append({"role": "assistant", "content": ai_reply})

        input_rate, output_rate = PRICING[self._model]
        cost = (prompt_tokens * input_rate + completion_tokens * output_rate) / 1_000_000
        self.last_usage = Usage(prompt_tokens, completion_tokens, cost)
