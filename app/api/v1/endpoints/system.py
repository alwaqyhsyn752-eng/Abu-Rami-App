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


@router.get("/system/about")
async def system_about():
    from app.core.config import settings
    return {
        "name": settings.PROJECT_NAME,
        "developer": getattr(settings, "APP_DEVELOPER", "حسين غلاب"),
        "tagline": getattr(settings, "APP_TAGLINE", "من المستقبل — بلغة الحاضر"),
        "version": settings.APP_VERSION,
        "interfaces": {
            "choice": "/",
            "hussein_ghallab": "/olq",
            "abu_rami": "/abu-rami",
            "programming": "/programming"
        }
    }
