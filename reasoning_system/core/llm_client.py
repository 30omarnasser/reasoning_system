import ollama
from config.settings import settings

class LLMClient:
    def __init__(self):
        self._client = ollama.Client(host=settings.ollama_host)

    def complete(self, messages: list[dict], **kwargs) -> str:
        response = self._client.chat(
            model=settings.model_name,
            messages=messages,
            options={
                "temperature": settings.temperature,
                "num_predict": settings.max_tokens,
            },
        )
        return response["message"]["content"]