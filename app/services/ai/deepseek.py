from typing import Optional
import httpx
import logging
from app.services.ai.base import BaseAIProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


DEEPSEEK_MODELS = [
    "deepseek-chat",
    "deepseek-coder",
    "deepseek-reasoner",
]


class DeepSeekProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.url = "https://api.deepseek.com/v1/chat/completions"

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
        }

        async with httpx.AsyncClient(timeout=90.0) as client:
            res = await client.post(self.url, json=payload, headers=headers)
            if res.status_code == 402:
                raise RuntimeError("INSUFFICIENT_BALANCE")
            if res.status_code == 404:
                raise RuntimeError("MODEL_NOT_FOUND")
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
            raise RuntimeError("DEEPSEEK_API_KEY missing")

        preferred = settings.DEEPSEEK_MODEL
        models = [preferred] + [m for m in DEEPSEEK_MODELS if m != preferred]

        last_error = None
        for model in models:
            try:
                logger.info("DeepSeek trying model: %s", model)
                text = await self._try_model(model, prompt, system_prompt)
                if text and text.strip():
                    logger.info("DeepSeek success with: %s", model)
                    return text
            except Exception as e:
                msg = str(e)
                logger.warning("DeepSeek model %s failed: %s", model, msg[:120])
                last_error = msg
                if "INSUFFICIENT_BALANCE" in msg:
                    raise RuntimeError("DeepSeek: no balance")
                continue

        raise RuntimeError("DeepSeek: all models failed. Last: " + str(last_error)[:200])
