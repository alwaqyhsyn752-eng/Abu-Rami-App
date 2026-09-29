import logging
import httpx
import os
from typing import Optional

logger = logging.getLogger(__name__)

# تخزين مؤقت في الذاكرة (يمكن استبداله بـ Redis لاحقاً)
_telegram_tokens = {}
_telegram_last_update = {}


async def set_webhook(bot_token: str, webhook_url: str) -> dict:
    api = "https://api.telegram.org/bot" + bot_token + "/setWebhook"
    try:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.post(api, json={"url": webhook_url})
            data = r.json()
            if data.get("ok"):
                _telegram_tokens["default"] = bot_token
                return {"success": True}
            return {"success": False, "message": data.get("description", "فشل")}
    except Exception as e:
        return {"success": False, "message": str(e)}


async def get_bot_info(bot_token: str) -> dict:
    api = "https://api.telegram.org/bot" + bot_token + "/getMe"
    try:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.get(api)
            data = r.json()
            if data.get("ok"):
                return data["result"]
            return {}
    except Exception as e:
        logger.warning("getMe failed: %s", e)
        return {}


async def send_message(bot_token: str, chat_id: int, text: str) -> bool:
    api = "https://api.telegram.org/bot" + bot_token + "/sendMessage"
    try:
        async with httpx.AsyncClient(timeout=20.0) as c:
            r = await c.post(api, json={
                "chat_id": chat_id,
                "text": text[:4000],
                "parse_mode": "Markdown",
            })
            return r.json().get("ok", False)
    except Exception as e:
        logger.warning("sendMessage failed: %s", e)
        return False


async def handle_update(bot_token: str, update: dict):
    try:
        msg = update.get("message") or update.get("edited_message")
        if not msg:
            return
        chat_id = msg.get("chat", {}).get("id")
        text = (msg.get("text") or "").strip()
        if not chat_id or not text:
            return

        # رد بسيط للأوامر
        if text == "/start":
            await send_message(
                bot_token, chat_id,
                "مرحباً! أنا أبو عولق، مساعدك الذكي. اكتب أي سؤال وسأجيبك."
            )
            return

        # استدعاء الذكاء الاصطناعي
        from app.services.ai.router import ai_router
        response, provider = await ai_router.generate_response(
            text, None, None
        )
        await send_message(
            bot_token, chat_id,
            response or "عذراً، لم أتمكن من الإجابة."
        )
    except Exception as e:
        logger.exception("handle_update failed: %s", e)
