from typing import Optional
import httpx
from app.services.ai.base import BaseAIProvider
from app.core.config import settings


class GeminiProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL
        self.base_url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            + self.model + ":generateContent"
        )

    async def generate(
        self, prompt: str, system_prompt: str,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> str:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY missing")

        parts = [{"text": system_prompt + "\n\n" + prompt}]
        if image_base64:
            parts.append({
                "inline_data": {
                    "mime_type": media_type or "image/jpeg",
                    "data": image_base64,
                }
            })

        payload = {"contents": [{"parts": parts}]}
        url = self.base_url + "?key=" + self.api_key

        async with httpx.AsyncClient(timeout=60.0) as client:
            res = await client.post(url, json=payload)
            if res.status_code != 200:
                raise RuntimeError("Gemini: " + res.text[:200])
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
