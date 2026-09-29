import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.v1.router import api_router
from app.db.engine import engine
from app.models.db_models import Base
from app.db.redis import redis_manager

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("DB initialized")
    except Exception as e:
        logger.error("DB init failed: %s", e)

    try:
        await redis_manager.connect()
    except Exception as e:
        logger.warning("Redis failed: %s", e)

    yield

    try:
        await redis_manager.close()
    except Exception:
        pass


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/apps", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_choice(request: Request):
    """شاشة اختيار الواجهة."""
    response = templates.TemplateResponse(
        request=request, name="choice.html",
        context={"version": settings.APP_VERSION}
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.get("/abu-rami")
async def read_root(request: Request):
    """واجهة أبو رامي الكلاسيكية."""
    response = templates.TemplateResponse(
        request=request, name="index.html",
        context={"version": settings.APP_VERSION}
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/olq")
async def read_olq(request: Request):
    """واجهة أبو عولق المستقبلية."""
    response = templates.TemplateResponse(
        request=request, name="abu_olq.html",
        context={"version": settings.APP_VERSION}
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
@app.get("/olq")
async def read_olq(request: Request):
    response = templates.TemplateResponse(
        request=request, name="abu_olq.html",
        context={"version": settings.APP_VERSION}
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response




@app.get("/programming")
async def read_programming(request: Request):
    response = templates.TemplateResponse(
        request=request, name="programming.html",
        context={"version": settings.APP_VERSION}
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}


@app.get("/version")
async def version_info():
    return {
        "version": settings.APP_VERSION,
        "name": settings.PROJECT_NAME,
    }


@app.exception_handler(Exception)
async def global_handler(request: Request, exc: Exception):
    logger.exception("Unhandled")
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "path": str(request.url.path)},
    )


app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router, prefix="/v1")
