import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.engine import get_db
from app.models.schemas import ChatRequest, ChatResponse, AppGenRequest
from app.services.chat_service import ChatService
from app.services.app_builder import AppBuilderService
from app.db.repositories.chat import ChatRepository

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/chat/completions", response_model=ChatResponse)
async def chat_completions(
    req: ChatRequest, db: AsyncSession = Depends(get_db)
):
    try:
        service = ChatService(db)
        res = await service.process_chat(
            req.message, req.conversation_id, req.image_base64, req.media_type
        )
        return res
    except Exception as e:
        logger.exception("chat failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/conversations")
async def list_conversations(db: AsyncSession = Depends(get_db)):
    repo = ChatRepository(db)
    convs = await repo.list_conversations()
    return [{"id": c.id, "title": c.title} for c in convs]


@router.post("/generate/app")
async def generate_app(
    req: AppGenRequest, db: AsyncSession = Depends(get_db)
):
    service = ChatService(db)

    prompt = (
        "أنشئ كود HTML+CSS+JS كامل لتطبيق ويب باسم: "
        + req.app_name + "\n"
        "الوصف: " + req.description + "\n"
        "القواعد: أعد فقط وسوم HTML الداخلية (بدون html/head/body). "
        "اجعل التصميم جميلاً وعربياً وسريعاً. استخدم ألوان داكنة مع لمسات سماوية."
    )

    ai_res = await service.process_chat(prompt)
    html_code = ai_res["message"]

    # تنظيف أي وسوم خارجية
    for tag in ["<!DOCTYPE html>", "<html", "</html>", "<head>", "</head>", "<body>", "</body>"]:
        html_code = html_code.replace(tag, "")

    url = await AppBuilderService.build_pwa(req.app_name, html_code)

    return {
        "success": True,
        "app_name": req.app_name,
        "app_url": url,
        "full_url": url,
    }
