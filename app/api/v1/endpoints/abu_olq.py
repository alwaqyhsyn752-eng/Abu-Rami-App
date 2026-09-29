import logging
from fastapi import APIRouter, Request
from app.services.thinking_modes import thinking_modes
from app.services.telegram_bot import (
    set_webhook, get_bot_info, handle_update
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/api/chat")
async def api_chat(req: dict):
    message = (req or {}).get("message", "").strip()
    mode = (req or {}).get("mode", "normal").strip()

    if not message:
        return {"success": False, "message": "الرسالة فارغة"}

    try:
        if mode == "fast":
            text, provider = await thinking_modes.fast(message)
        elif mode == "deep":
            text, provider = await thinking_modes.deep(message)
        elif mode == "expert":
            text, provider = await thinking_modes.expert(message)
        elif mode == "expanded":
            text, provider = await thinking_modes.expanded(message)
        elif mode == "search":
            text, provider = await thinking_modes.search(message)
        elif mode == "termux":
            text, provider = await thinking_modes.termux(message)
        else:
            text, provider = await thinking_modes.normal(message)

        return {
            "success": True,
            "conversation_id": None,
            "message": text,
            "provider": provider,
            "mode": mode,
        }
    except Exception as e:
        logger.exception("api_chat failed")
        return {
            "success": False,
            "message": "خطأ: " + str(e)[:200],
            "provider": "none",
        }


@router.post("/api/generate")
async def api_generate(req: dict):
    prompt = (req or {}).get("prompt", "").strip()
    if not prompt:
        return {"success": False, "message": "الرجاء إدخال الوصف"}
    from app.services.web_search import search_web
    text, provider = await thinking_modes.normal(
        "توليد محتوى إبداعي احترافي لـ: " + prompt
    )
    return {"success": True, "content": text, "provider": provider}


@router.post("/api/search")
async def api_search(req: dict):
    query = (req or {}).get("query", "").strip()
    if not query:
        return {"success": False, "message": "الرجاء إدخال كلمة البحث"}
    from app.services.web_search import search_web
    results = await search_web(query, max_results=8)
    return {"success": True, "query": query, "results": results}


@router.post("/api/analyze-code")
async def api_analyze_code(req: dict):
    code = (req or {}).get("code", "").strip()
    if not code:
        return {"success": False, "message": "الرجاء لصق الكود"}
    prompt = (
        "حلّل الكود التالي واذكر: الأخطاء، التحسينات المقترحة،"
        " الأداء، الأمان، وأعد نسخة محسّنة:\n\n" + code
    )
    text, provider = await thinking_modes.deep(prompt)
    return {"success": True, "analysis": text, "provider": provider}


# ============ Telegram ============
@router.post("/telegram/link")
async def telegram_link(req: dict):
    token = (req or {}).get("token", "").strip()
    webhook = (req or {}).get("webhook_url", "").strip()
    if not token:
        return {"success": False, "message": "أدخل توكن البوت"}

    info = await get_bot_info(token)
    if not info:
        return {"success": False, "message": "توكن غير صالح"}

    if webhook:
        result = await set_webhook(token, webhook)
        if not result.get("success"):
            return result

    return {
        "success": True,
        "bot_username": info.get("username", ""),
        "bot_name": info.get("first_name", ""),
    }


@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    try:
        body = await request.json()
        import os
        token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        if not token:
            return {"ok": True}
        await handle_update(token, body)
        return {"ok": True}
    except Exception as e:
        logger.warning("Webhook error: %s", e)
        return {"ok": True}
