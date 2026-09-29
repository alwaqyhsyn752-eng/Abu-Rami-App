from typing import Optional
import httpx
from app.services.ai.base import BaseAIProvider
from app.core.config import settings


class OpenRouterProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    async def generate(
        self, prompt: str, system_prompt: str,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> str:
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY missing")
        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
            "HTTP-Referer": "https://abu-rami-app.onrender.com",
            "X-Title": "Abu Rami AI",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        }
        async with httpx.AsyncClient(timeout=45.0) as client:
            res = await client.post(self.url, json=payload, headers=headers)
            if res.status_code != 200:
                raise RuntimeError("OpenRouter: " + res.text[:200])
            return res.json()["choices"][0]["message"]["content"]
