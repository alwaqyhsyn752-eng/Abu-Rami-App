from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/system/status")
async def system_status():
    return {
        "status": "online",
        "version": settings.APP_VERSION,
        "providers": {
            "gemini": bool(settings.GEMINI_API_KEY),
            "groq": bool(settings.GROQ_API_KEY),
            "openrouter": bool(settings.OPENROUTER_API_KEY),
            "deepseek": bool(settings.DEEPSEEK_API_KEY),
        },
    }


@router.get("/system/version")
async def system_version():
    return {
        "version": settings.APP_VERSION,
        "name": settings.PROJECT_NAME,
        "updated_at": "auto",
    }
