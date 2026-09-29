from typing import Optional
import httpx
from app.services.ai.base import BaseAIProvider
from app.core.config import settings


class DeepSeekProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.model = settings.DEEPSEEK_MODEL
        self.url = "https://api.deepseek.com/v1/chat/completions"

    async def generate(
        self, prompt: str, system_prompt: str,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> str:
        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY missing")
        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            res = await client.post(self.url, json=payload, headers=headers)
            if res.status_code != 200:
                raise RuntimeError("DeepSeek: " + res.text[:200])
            return res.json()["choices"][0]["message"]["content"]
