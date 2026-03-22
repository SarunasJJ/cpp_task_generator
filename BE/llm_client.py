"""
Unified text generation for Gemini, Anthropic Claude, and OpenAI GPT.
"""

import os


class LLMClientError(Exception):
    pass


class LLMClient:
    def __init__(self, provider: str, api_key: str):
        p = (provider or "").strip().lower()
        if p not in ("gemini", "claude", "gpt"):
            raise ValueError("provider must be 'gemini', 'claude', or 'gpt'")
        if not api_key:
            raise ValueError("api_key is required")

        self.provider = p
        self.api_key = api_key
        self._gemini_model = None
        self._anthropic_client = None
        self._openai_client = None

        if self.provider == "gemini":
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            model_name = os.getenv("GEMINI_MODEL", "gemini-3.0-flash")
            self._gemini_model = genai.GenerativeModel(model_name=model_name)
        elif self.provider == "claude":
            from anthropic import Anthropic

            self._anthropic_client = Anthropic(api_key=api_key)
        else:
            from openai import OpenAI

            self._openai_client = OpenAI(api_key=api_key)

    def generate_text(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise LLMClientError("Empty prompt")

        try:
            if self.provider == "gemini":
                response = self._gemini_model.generate_content(prompt)
                if not response.text:
                    raise LLMClientError("Gemini returned empty text")
                return response.text

            if self.provider == "claude":
                model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
                msg = self._anthropic_client.messages.create(
                    model=model,
                    max_tokens=8192,
                    messages=[{"role": "user", "content": prompt}],
                )
                block = msg.content[0]
                if block.type != "text":
                    raise LLMClientError("Unexpected Claude response block type")
                return block.text

            model = os.getenv("OPENAI_MODEL", "gpt-5o-mini")
            chat = self._openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            text = chat.choices[0].message.content
            if not text:
                raise LLMClientError("OpenAI returned empty content")
            return text

        except LLMClientError:
            raise
        except Exception as e:
            raise LLMClientError(str(e)) from e
