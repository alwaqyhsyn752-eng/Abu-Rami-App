import os
import logging
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, Header
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "hussein2026")


def check_auth(x_admin_password: str = Header(None, alias="X-Admin-Password")):
    if not x_admin_password or x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="كلمة المرور خاطئة")
    return True


@router.post("/admin/login")
async def admin_login(req: dict):
    pwd = (req or {}).get("password", "")
    if pwd == ADMIN_PASSWORD:
        return {"success": True, "token": ADMIN_PASSWORD}
    return {"success": False, "message": "كلمة المرور خاطئة"}


@router.get("/admin/overview")
async def admin_overview(
    request: Request,
    x_admin_password: str = Header(None, alias="X-Admin-Password")
):
    check_auth(x_admin_password)

    # جلب معلومات النظام
    import platform
    import sys

    providers = {
        "gemini": bool(settings.GEMINI_API_KEY),
        "groq": bool(settings.GROQ_API_KEY),
        "openrouter": bool(settings.OPENROUTER_API_KEY),
        "deepseek": bool(settings.DEEPSEEK_API_KEY),
    }

    # حالة قاعدة البيانات
    db_ok = False
    try:
        from app.db.engine import engine
        from sqlalchemy import text
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_ok = True
    except Exception as e:
        logger.warning("DB check failed: %s", e)

    # حالة Redis
    redis_ok = False
    try:
        from app.db.redis import redis_manager
        redis_ok = redis_manager.client is not None
    except Exception:
        pass

    # حالة GitHub Actions
    gh_token = os.getenv("GITHUB_ACTIONS_TOKEN", "").strip()
    gh_ok = bool(gh_token)

    # حالة APK builder
    apk_ready = gh_ok and bool(os.getenv("KEYSTORE_BASE64", "").strip())

    return {
        "success": True,
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION,
        "developer": getattr(settings, "APP_DEVELOPER", "حسين غلاب"),
        "system": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor() or "unknown",
        },
        "providers": providers,
        "database": db_ok,
        "redis": redis_ok,
        "github_actions": gh_ok,
        "apk_builder_ready": apk_ready,
    }


@router.get("/admin/env-status")
async def admin_env_status(
    x_admin_password: str = Header(None, alias="X-Admin-Password")
):
    check_auth(x_admin_password)

    def mask(value: str) -> str:
        if not value:
            return ""
        if len(value) < 10:
            return "***"
        return value[:6] + "..." + value[-4:]

    env_keys = [
        "GEMINI_API_KEY", "GROQ_API_KEY", "OPENROUTER_API_KEY",
        "DEEPSEEK_API_KEY", "GITHUB_ACTIONS_TOKEN", "TELEGRAM_BOT_TOKEN",
        "DATABASE_URL", "REDIS_URL", "ADMIN_PASSWORD",
    ]

    result = {}
    for key in env_keys:
        val = os.getenv(key, "").strip()
        result[key] = {
            "set": bool(val),
            "masked": mask(val) if val else "",
            "length": len(val) if val else 0,
        }

    return {"success": True, "env": result}


@router.get("/admin/logs")
async def admin_logs(
    lines: int = 100,
    x_admin_password: str = Header(None, alias="X-Admin-Password")
):
    check_auth(x_admin_password)

    log_file = "/tmp/hussein.log"
    if not os.path.isfile(log_file):
        return {"success": True, "logs": [], "message": "لا يوجد ملف سجل بعد"}

    try:
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            all_lines = f.readlines()
        last = all_lines[-lines:] if len(all_lines) > lines else all_lines
        return {"success": True, "logs": [l.rstrip() for l in last]}
    except Exception as e:
        return {"success": False, "message": str(e)}


@router.get("/admin/gh-builds")
async def admin_gh_builds(
    x_admin_password: str = Header(None, alias="X-Admin-Password")
):
    check_auth(x_admin_password)

    gh_token = os.getenv("GITHUB_ACTIONS_TOKEN", "").strip()
    if not gh_token:
        return {"success": False, "message": "GITHUB_ACTIONS_TOKEN غير موجود"}

    import httpx
    owner = "alwaqyhsyn752-eng"
    repo = "Abu-Rami-App"

    try:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.get(
                f"https://api.github.com/repos/{owner}/{repo}/actions/runs?per_page=10",
                headers={
                    "Authorization": "Bearer " + gh_token,
                    "Accept": "application/vnd.github+json",
                },
            )
            if r.status_code != 200:
                return {"success": False, "message": f"GitHub: {r.status_code}"}

            data = r.json()
            runs = []
            for run in data.get("workflow_runs", [])[:10]:
                runs.append({
                    "id": run.get("id"),
                    "name": run.get("name", ""),
                    "status": run.get("status", ""),
                    "conclusion": run.get("conclusion", ""),
                    "created_at": run.get("created_at", ""),
                    "updated_at": run.get("updated_at", ""),
                    "html_url": run.get("html_url", ""),
                    "run_number": run.get("run_number"),
                })
            return {"success": True, "runs": runs}
    except Exception as e:
        return {"success": False, "message": str(e)}


@router.get("/admin/gh-releases")
async def admin_gh_releases(
    x_admin_password: str = Header(None, alias="X-Admin-Password")
):
    check_auth(x_admin_password)

    gh_token = os.getenv("GITHUB_ACTIONS_TOKEN", "").strip()
    if not gh_token:
        return {"success": False, "message": "التوكن غير موجود"}

    import httpx
    owner = "alwaqyhsyn752-eng"
    repo = "Abu-Rami-App"

    try:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.get(
                f"https://api.github.com/repos/{owner}/{repo}/releases?per_page=10",
                headers={
                    "Authorization": "Bearer " + gh_token,
                    "Accept": "application/vnd.github+json",
                },
            )
            if r.status_code != 200:
                return {"success": False, "message": f"GitHub: {r.status_code}"}

            releases = []
            for rel in r.json():
                assets = [
                    {"name": a.get("name"), "url": a.get("browser_download_url"),
                     "size": a.get("size")}
                    for a in rel.get("assets", [])
                ]
                releases.append({
                    "tag": rel.get("tag_name"),
                    "name": rel.get("name"),
                    "created_at": rel.get("created_at"),
                    "assets": assets,
                })
            return {"success": True, "releases": releases}
    except Exception as e:
        return {"success": False, "message": str(e)}


@router.post("/admin/test-provider")
async def admin_test_provider(
    req: dict,
    x_admin_password: str = Header(None, alias="X-Admin-Password")
):
    check_auth(x_admin_password)

    provider = (req or {}).get("provider", "gemini")
    test_prompt = "قل فقط: OK"

    from app.services.ai.router import ai_router

    try:
        # اختبار مزود محدد
        from app.services.ai.gemini import GeminiProvider
        from app.services.ai.groq import GroqProvider
        from app.services.ai.openrouter import OpenRouterProvider
        from app.services.ai.deepseek import DeepSeekProvider

        mapping = {
            "gemini": GeminiProvider(),
            "groq": GroqProvider(),
            "openrouter": OpenRouterProvider(),
            "deepseek": DeepSeekProvider(),
        }

        p = mapping.get(provider)
        if not p:
            return {"success": False, "message": "مزود غير معروف"}

        import time
        start = time.time()
        from app.prompts.system_prompt import SYSTEM_PROMPT
        response = await p.generate(test_prompt, SYSTEM_PROMPT, None, None)
        elapsed = round(time.time() - start, 2)

        return {
            "success": True,
            "provider": provider,
            "response": (response or "")[:200],
            "time_seconds": elapsed,
        }
    except Exception as e:
        return {"success": False, "provider": provider, "message": str(e)[:200]}
