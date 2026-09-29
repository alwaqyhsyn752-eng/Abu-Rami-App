from typing import Optional
import httpx
import logging
from app.services.ai.base import BaseAIProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


# قائمة شاملة لكل موديلات Gemini المتاحة
GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.5-flash",
    "gemini-3-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash-latest",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
    "gemini-pro",
    "gemini-pro-vision",
]


class GeminiProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/"

    async def _try_model(
        self, model: str, prompt: str, system_prompt: str,
        image_base64: Optional[str], media_type: Optional[str]
    ) -> str:
        url = self.base_url + model + ":generateContent?key=" + self.api_key

        parts = [{"text": system_prompt + "\n\n" + prompt}]
        if image_base64:
            parts.append({
                "inline_data": {
                    "mime_type": media_type or "image/jpeg",
                    "data": image_base64,
                }
            })

        payload = {"contents": [{"parts": parts}]}

        async with httpx.AsyncClient(timeout=60.0) as client:
            res = await client.post(url, json=payload)
            if res.status_code == 404:
                raise RuntimeError("MODEL_NOT_FOUND")
            if res.status_code == 400:
                raise RuntimeError("BAD_REQUEST: " + res.text[:150])
            if res.status_code == 429:
                raise RuntimeError("RATE_LIMIT")
            if res.status_code != 200:
                raise RuntimeError("HTTP " + str(res.status_code) + ": " + res.text[:150])
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

    async def generate(
        self,
        prompt: str,
        system_prompt: str,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> str:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY missing")

        # حاول الموديل المفضل أولاً، ثم البقية
        preferred = settings.GEMINI_MODEL
        models = [preferred] + [m for m in GEMINI_MODELS if m != preferred]

        last_error = None
        for model in models:
            try:
                logger.info("Gemini trying model: %s", model)
                text = await self._try_model(
                    model, prompt, system_prompt, image_base64, media_type
                )
                if text and text.strip():
                    logger.info("Gemini success with: %s", model)
                    return text
            except Exception as e:
                msg = str(e)
                logger.warning("Gemini model %s failed: %s", model, msg[:120])
                last_error = msg

                # إذا كان خطأ مصادقة، أوقف فوراً — لا فائدة من تجربة بقية الموديلات
                if "API_KEY" in msg or "PERMISSION" in msg or "403" in msg:
                    raise RuntimeError("Gemini auth error: " + msg[:200])

                # MODEL_NOT_FOUND أو RATE_LIMIT أو BAD_REQUEST → جرّب التالي
                continue

        raise RuntimeError("Gemini: all models failed. Last: " + str(last_error)[:200])
