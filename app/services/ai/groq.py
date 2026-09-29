from typing import Optional
import httpx
import logging
from app.services.ai.base import BaseAIProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


# قائمة شاملة لموديلات Groq المجانية
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.3-70b-specdec",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "llama-guard-3-8b",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
    "gemma-7b-it",
    "qwen-qwq-32b",
    "qwen-2.5-32b",
    "qwen-2.5-coder-32b",
    "deepseek-r1-distill-llama-70b",
    "deepseek-r1-distill-qwen-32b",
    "mistral-saba-24b",
]


class GroqProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    async def _try_model(
        self, model: str, prompt: str, system_prompt: str
    ) -> str:
        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 4096,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            res = await client.post(self.url, json=payload, headers=headers)
            if res.status_code == 404:
                raise RuntimeError("MODEL_NOT_FOUND")
            if res.status_code == 400:
                raise RuntimeError("BAD_REQUEST: " + res.text[:150])
            if res.status_code == 429:
                raise RuntimeError("RATE_LIMIT")
            if res.status_code in (401, 403):
                raise RuntimeError("AUTH_ERROR: " + res.text[:150])
            if res.status_code != 200:
                raise RuntimeError("HTTP " + str(res.status_code) + ": " + res.text[:150])
            return res.json()["choices"][0]["message"]["content"]

    async def generate(
        self,
        prompt: str,
        system_prompt: str,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> str:
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY missing")

        preferred = settings.GROQ_MODEL
        models = [preferred] + [m for m in GROQ_MODELS if m != preferred]

        last_error = None
        for model in models:
            try:
                logger.info("Groq trying model: %s", model)
                text = await self._try_model(model, prompt, system_prompt)
                if text and text.strip():
                    logger.info("Groq success with: %s", model)
                    return text
            except Exception as e:
                msg = str(e)
                logger.warning("Groq model %s failed: %s", model, msg[:120])
                last_error = msg
                if "AUTH_ERROR" in msg:
                    raise RuntimeError("Groq auth error: " + msg[:200])
                continue
