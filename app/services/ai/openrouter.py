from typing import Optional
import httpx
import logging
from app.services.ai.base import BaseAIProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


# قائمة شاملة لموديلات OpenRouter المجانية
OPENROUTER_MODELS = [
    "google/gemini-2.0-flash-exp:free",
    "google/gemini-flash-1.5:free",
    "google/gemini-pro-1.5:free",
    "google/gemma-2-9b-it:free",
    "google/gemma-2-27b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "meta-llama/llama-3.1-70b-instruct:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "meta-llama/llama-3-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "mistralai/mistral-nemo:free",
    "mistralai/mixtral-8x7b-instruct:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "qwen/qwen-2.5-coder-32b-instruct:free",
    "qwen/qwq-32b-preview:free",
    "deepseek/deepseek-r1:free",
    "deepseek/deepseek-chat:free",
    "microsoft/phi-3-medium-128k-instruct:free",
    "nousresearch/hermes-3-llama-3.1-405b:free",
    "openchat/openchat-7b:free",
    "huggingfaceh4/zephyr-7b-beta:free",
    "gryphe/mythomax-l2-13b:free",
    "undi95/toppy-m-7b:free",
]


class OpenRouterProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    async def _try_model(
        self, model: str, prompt: str, system_prompt: str
    ) -> str:
        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
            "HTTP-Referer": "https://abu-rami-app.onrender.com",
            "X-Title": "Abu Rami AI",
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
            data = res.json()
            return data["choices"][0]["message"]["content"]

    async def generate(
        self,
        prompt: str,
        system_prompt: str,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> str:
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY missing")

        preferred = settings.OPENROUTER_MODEL
        models = [preferred] + [m for m in OPENROUTER_MODELS if m != preferred]

        last_error = None
        for model in models:
            try:
                logger.info("OpenRouter trying model: %s", model)
                text = await self._try_model(model, prompt, system_prompt)
                if text and text.strip():
                    logger.info("OpenRouter success with: %s", model)
                    return text
            except Exception as e:
                msg = str(e)
                logger.warning("OpenRouter model %s failed: %s", model, msg[:120])
                last_error = msg
                if "AUTH_ERROR" in msg:
                    raise RuntimeError("OpenRouter auth error: " + msg[:200])
                continue

        raise RuntimeError("OpenRouter: all models failed. Last: " + str(last_error)[:200])
