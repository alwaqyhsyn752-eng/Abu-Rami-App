import logging
from typing import Optional, Tuple
from app.services.ai.gemini import GeminiProvider
from app.services.ai.groq import GroqProvider
from app.services.ai.openrouter import OpenRouterProvider
from app.services.ai.deepseek import DeepSeekProvider
from app.prompts.system_prompt import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class AIRouter:
    def __init__(self):
        # الترتيب حسب السرعة والموثوقية
        self.providers = [
            ("gemini", GeminiProvider()),
            ("groq", GroqProvider()),
            ("openrouter", OpenRouterProvider()),
            ("deepseek", DeepSeekProvider()),
        ]

    async def generate_response(
        self,
        prompt: str,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> Tuple[str, str]:
        errors = []
        for name, provider in self.providers:
            try:
                logger.info("Trying provider: %s", name)
                response = await provider.generate(
                    prompt, SYSTEM_PROMPT, image_base64, media_type
                )
                if response and response.strip():
                    logger.info("Provider %s succeeded", name)
                    return response, name
                errors.append(name + ": empty response")
            except Exception as e:
                logger.warning("Provider %s failed: %s", name, str(e)[:150])
                errors.append(name + ": " + str(e)[:100])

        logger.error("All providers failed: %s", errors)
        return (
            "عذراً، تعذر الاتصال بخادم الذكاء الاصطناعي. "
            "تحقق من مفاتيح API في Render Environment.",
            "none",
        )


ai_router = AIRouter()
