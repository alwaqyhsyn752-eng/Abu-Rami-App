import logging
from typing import Tuple, List
from app.services.ai.router import ai_router
from app.prompts.system_prompt import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


# موجهات كل وضع
MODE_PROMPTS = {
    "normal": (
        "أنت مساعد ذكي متوازن. أجب بوضوح وإيجاز مع تفاصيل كافية."
    ),
    "fast": (
        "أنت مساعد سريع. أجب بإيجاز شديد مباشرة بدون مقدمات. "
        "أعطِ الجواب فقط في جملة أو جملتين إن أمكن."
    ),
    "deep": (
        "أنت محلل عميق. فكّر خطوة بخطوة قبل الإجابة. "
        "قسّم إجابتك إلى: التحليل ← الأسباب ← الحل ← الخلاصة. "
        "اذكر الافتراضات والقيود."
    ),
    "expert": (
        "أنت خبير عالمي في مجالك. استخدم مصطلحات دقيقة. "
        "اذكر أفضل الممارسات والمراجع إن أمكن. "
        "قدّم إجابة بمستوى مقالة احترافية."
    ),
    "expanded": (
        "أنت مفكر موسّع. ادمج وجهات نظر متعددة. "
        "اذكر إيجابيات وسلبيات كل خيار. "
        "أعطِ توصية نهائية واضحة."
    ),
    "search": (
        "أنت باحث. سأعطيك نتائج بحث الويب وسؤال المستخدم. "
        "لخّص النتائج وقدّم إجابة موثوقة مستندة إلى المصادر."
    ),
    "termux": (
        "أنت خبير Termux و Linux على أندرويد. "
        "اشرح الأخطاء بدقة. أعطِ الأوامر جاهزة للنسخ. "
        "استخدم رموز ``` للأوامر."
    ),
}


class ThinkingModes:
    async def fast(self, prompt: str) -> Tuple[str, str]:
        return await ai_router.generate_response(
            MODE_PROMPTS["fast"] + "\n\nسؤال: " + prompt
        )

    async def normal(self, prompt: str) -> Tuple[str, str]:
        return await ai_router.generate_response(
            MODE_PROMPTS["normal"] + "\n\nسؤال: " + prompt
        )

    async def deep(self, prompt: str) -> Tuple[str, str]:
        return await ai_router.generate_response(
            MODE_PROMPTS["deep"] + "\n\nسؤال: " + prompt
        )

    async def expert(self, prompt: str) -> Tuple[str, str]:
        return await ai_router.generate_response(
            MODE_PROMPTS["expert"] + "\n\nسؤال: " + prompt
        )

    async def expanded(self, prompt: str) -> Tuple[str, str]:
        from app.services.ai.gemini import GeminiProvider
        from app.services.ai.groq import GroqProvider
        from app.services.ai.openrouter import OpenRouterProvider

        providers = [
            GeminiProvider(),
            GroqProvider(),
            OpenRouterProvider(),
        ]
        answers = []
        source_names = []

        for p in providers:
            try:
                name = type(p).__name__.replace("Provider", "").lower()
                text = await p.generate(
                    prompt, MODE_PROMPTS["expanded"], None, None
                )
                if text and text.strip():
                    answers.append("[من " + name + "]: " + text[:800])
                    source_names.append(name)
            except Exception as e:
                logger.warning("Expanded: %s failed: %s", name, e)

        if not answers:
            return await ai_router.generate_response(prompt)

        combined = (
            MODE_PROMPTS["expanded"]
            + "\n\nسؤال: " + prompt
            + "\n\nإجابات مقترحة:\n\n" + "\n\n".join(answers)
            + "\n\nلخّص الإجابات أعلاه في رد موحّد دقيق ومفيد."
        )
        text, _ = await ai_router.generate_response(combined)
        return text, "expanded(" + ",".join(source_names) + ")"

    async def search(self, prompt: str) -> Tuple[str, str]:
        try:
            from app.services.web_search import search_web
            results = await search_web(prompt, max_results=5)
            if not results:
                return await self.normal(prompt)

            context = "\n\n".join([
                "[" + str(i+1) + "] " + r["title"] + "\n" + r["snippet"]
                for i, r in enumerate(results)
            ])
            combined = (
                MODE_PROMPTS["search"]
                + "\n\nسؤال: " + prompt
                + "\n\nنتائج البحث:\n" + context
            )
            text, _ = await ai_router.generate_response(combined)
            return text, "search"
        except Exception as e:
            logger.warning("Search failed: %s", e)
            return await self.normal(prompt)

    async def termux(self, prompt: str) -> Tuple[str, str]:
        return await ai_router.generate_response(
            MODE_PROMPTS["termux"] + "\n\nالمشكلة: " + prompt
        )


thinking_modes = ThinkingModes()
