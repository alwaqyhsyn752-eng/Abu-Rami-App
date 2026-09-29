#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة البناء الشاملة لمشروع [أبو رامي AI]
- واجهة عربية كاملة
- محادثة صوتية مباشرة
- توليد تطبيقات (PWA)
- تحديث تلقائي فوري
- بنية نظيفة بدون أخطاء
"""

import os
import sys

PROJECT_FILES = {}

# ============================================================
# 1) ملفات البيئة والنشر
# ============================================================

PROJECT_FILES[".python-version"] = "3.11\n"

PROJECT_FILES["requirements.txt"] = r"""fastapi>=0.109.0
uvicorn[standard]>=0.27.0
httpx>=0.26.0
pydantic>=2.6.0
pydantic-settings>=2.1.0
sqlalchemy[asyncio]>=2.0.25
greenlet>=3.0.0
aiosqlite>=0.19.0
asyncpg>=0.29.0
redis>=5.0.1
jinja2>=3.1.3
python-multipart>=0.0.6
python-dotenv>=1.0.0
"""

PROJECT_FILES["render.yaml"] = r"""services:
  - type: web
    name: abu-rami-app
    env: python
    plan: free
    buildCommand: "pip install --upgrade pip && pip install -r requirements.txt"
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    healthCheckPath: /health
    autoDeploy: true
    envVars:
      - key: PYTHON_VERSION
        value: "3.11.0"
      - key: GEMINI_API_KEY
        sync: false
      - key: GROQ_API_KEY
        sync: false
      - key: OPENROUTER_API_KEY
        sync: false
      - key: DEEPSEEK_API_KEY
        sync: false
      - key: APP_VERSION
        value: "1.0.0"
"""

PROJECT_FILES[".env.example"] = r"""GEMINI_API_KEY=
GROQ_API_KEY=
OPENROUTER_API_KEY=
DEEPSEEK_API_KEY=
DATABASE_URL=
REDIS_URL=redis://localhost:6379/0
GEMINI_MODEL=gemini-2.0-flash
GROQ_MODEL=llama-3.3-70b-versatile
OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free
DEEPSEEK_MODEL=deepseek-chat
APP_VERSION=1.0.0
"""

PROJECT_FILES[".gitignore"] = r"""__pycache__/
*.py[cod]
*$py.class
.env
*.db
*.sqlite
*.sqlite3
logs/
.venv/
venv/
ENV/
.idea/
.vscode/
.DS_Store
static/apks/
"""

PROJECT_FILES["README.md"] = "\n".join([
    "# أبو رامي AI",
    "",
    "تطبيق ذكي متعدد الموديلات + محادثة صوتية + توليد تطبيقات.",
    "",
    "الشعار: لسنا الوحيدين، لكن الأفضل بذكاء",
    "",
    "## الميزات",
    "",
    "- واجهة عربية كاملة RTL",
    "- محادثة صوتية مباشرة",
    "- تبديل تلقائي بين Gemini / Groq / OpenRouter / DeepSeek",
    "- توليد تطبيقات PWA قابلة للتثبيت",
    "- تحديث تلقائي فوري عند تحديث الخادم",
    "",
    "## التشغيل",
    "",
    "pip install -r requirements.txt",
    "cp .env.example .env",
    "uvicorn app.main:app --reload",
    "",
])

# ============================================================
# 2) ملفات __init__.py
# ============================================================

for _pkg in [
    "app/__init__.py",
    "app/core/__init__.py",
    "app/db/__init__.py",
    "app/db/repositories/__init__.py",
    "app/models/__init__.py",
    "app/services/__init__.py",
    "app/services/ai/__init__.py",
    "app/prompts/__init__.py",
    "app/api/__init__.py",
    "app/api/v1/__init__.py",
    "app/api/v1/endpoints/__init__.py",
]:
    PROJECT_FILES[_pkg] = ""


# ============================================================
# 3) Core
# ============================================================

PROJECT_FILES["app/core/config.py"] = r"""import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "أبو رامي AI"

    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""

    GEMINI_MODEL: str = "gemini-2.0-flash"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    OPENROUTER_MODEL: str = "google/gemini-2.0-flash-exp:free"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    DATABASE_URL: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"

    APP_VERSION: str = "1.0.0"

    def get_database_url(self) -> str:
        url = (self.DATABASE_URL or "").strip()
        if not url:
            return "sqlite+aiosqlite:////tmp/abu_rami.db"
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://") and "asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
"""

PROJECT_FILES["app/core/logging_config.py"] = r"""import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    root.setLevel(level)
    for handler in list(root.handlers):
        root.removeHandler(handler)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)
"""


# ============================================================
# 4) DB
# ============================================================

PROJECT_FILES["app/db/engine.py"] = r"""from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from app.core.config import settings

db_url = settings.get_database_url()

engine = create_async_engine(
    db_url, echo=False, future=True, pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
"""

PROJECT_FILES["app/db/redis.py"] = r"""import logging
import redis.asyncio as aioredis
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisManager:
    def __init__(self) -> None:
        self.client = None

    async def connect(self) -> None:
        try:
            self.client = aioredis.from_url(
                settings.REDIS_URL, decode_responses=True
            )
            await self.client.ping()
            logger.info("Redis connected.")
        except Exception as e:
            logger.warning("Redis unavailable: %s", e)
            self.client = None

    async def close(self) -> None:
        if self.client is not None:
            try:
                await self.client.close()
            except Exception:
                pass


redis_manager = RedisManager()
"""


# ============================================================
# 5) Models
# ============================================================

PROJECT_FILES["app/models/db_models.py"] = r"""import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), default="محادثة جديدة")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey("conversations.id"))
    role = Column(String(50))
    content = Column(Text)
    provider = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")
"""

PROJECT_FILES["app/models/schemas.py"] = r"""from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None
    image_base64: Optional[str] = None
    media_type: Optional[str] = None


class ChatResponse(BaseModel):
    success: bool
    conversation_id: str
    message: str
    provider: str


class AppGenRequest(BaseModel):
    app_name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
"""


# ============================================================
# 6) Repositories
# ============================================================

PROJECT_FILES["app/db/repositories/chat.py"] = r"""import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.db_models import Conversation, Message


class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_conversation(
        self, conversation_id: Optional[str] = None,
        title: str = "محادثة جديدة"
    ) -> Conversation:
        if conversation_id:
            result = await self.db.execute(
                select(Conversation).where(Conversation.id == conversation_id)
            )
            conv = result.scalars().first()
            if conv:
                return conv

        new_conv = Conversation(
            id=conversation_id or str(uuid.uuid4()), title=title
        )
        self.db.add(new_conv)
        await self.db.commit()
        await self.db.refresh(new_conv)
        return new_conv

    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        provider: Optional[str] = None,
    ) -> Message:
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            provider=provider,
        )
        self.db.add(msg)
        await self.db.commit()
        await self.db.refresh(msg)
        return msg

    async def list_conversations(self):
        result = await self.db.execute(
            select(Conversation).order_by(Conversation.updated_at.desc())
        )
        return result.scalars().all()
"""


# ============================================================
# 7) AI Providers
# ============================================================

PROJECT_FILES["app/services/ai/base.py"] = r"""from abc import ABC, abstractmethod
from typing import Optional


class BaseAIProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: str,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> str:
        raise NotImplementedError
"""

PROJECT_FILES["app/services/ai/gemini.py"] = r"""from typing import Optional
import httpx
from app.services.ai.base import BaseAIProvider
from app.core.config import settings


class GeminiProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL
        self.base_url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            + self.model + ":generateContent"
        )

    async def generate(
        self, prompt: str, system_prompt: str,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> str:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY missing")

        parts = [{"text": system_prompt + "\n\n" + prompt}]
        if image_base64:
            parts.append({
                "inline_data": {
                    "mime_type": media_type or "image/jpeg",
                    "data": image_base64,
                }
            })

        payload = {"contents": [{"parts": parts}]}
        url = self.base_url + "?key=" + self.api_key

        async with httpx.AsyncClient(timeout=60.0) as client:
            res = await client.post(url, json=payload)
            if res.status_code != 200:
                raise RuntimeError("Gemini: " + res.text[:200])
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
"""

PROJECT_FILES["app/services/ai/groq.py"] = r"""from typing import Optional
import httpx
from app.services.ai.base import BaseAIProvider
from app.core.config import settings


class GroqProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    async def generate(
        self, prompt: str, system_prompt: str,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> str:
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY missing")
        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        }
        async with httpx.AsyncClient(timeout=45.0) as client:
            res = await client.post(self.url, json=payload, headers=headers)
            if res.status_code != 200:
                raise RuntimeError("Groq: " + res.text[:200])
            return res.json()["choices"][0]["message"]["content"]
"""

PROJECT_FILES["app/services/ai/openrouter.py"] = r"""from typing import Optional
import httpx
from app.services.ai.base import BaseAIProvider
from app.core.config import settings


class OpenRouterProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    async def generate(
        self, prompt: str, system_prompt: str,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> str:
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY missing")
        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
            "HTTP-Referer": "https://abu-rami-app.onrender.com",
            "X-Title": "Abu Rami AI",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        }
        async with httpx.AsyncClient(timeout=45.0) as client:
            res = await client.post(self.url, json=payload, headers=headers)
            if res.status_code != 200:
                raise RuntimeError("OpenRouter: " + res.text[:200])
            return res.json()["choices"][0]["message"]["content"]
"""

PROJECT_FILES["app/services/ai/deepseek.py"] = r"""from typing import Optional
import httpx
from app.services.ai.base import BaseAIProvider
from app.core.config import settings


class DeepSeekProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.model = settings.DEEPSEEK_MODEL
        self.url = "https://api.deepseek.com/v1/chat/completions"

    async def generate(
        self, prompt: str, system_prompt: str,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> str:
        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY missing")
        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            res = await client.post(self.url, json=payload, headers=headers)
            if res.status_code != 200:
                raise RuntimeError("DeepSeek: " + res.text[:200])
            return res.json()["choices"][0]["message"]["content"]
"""


# ============================================================
# 8) System Prompt
# ============================================================

_sys_lines = [
    'SYSTEM_PROMPT = """أنت "أبو رامي AI" — مساعد ذكي، سريع، وخبير برمجي شامل.',
    '',
    'الشعار: "لسنا الوحيدين، لكن الأفضل بذكاء".',
    '',
    'قواعد:',
    '1. تحدث بالعربية دائماً بأسلوب راقٍ وواضح.',
    '2. أنت خبير في Python, Kotlin, Java, JavaScript, HTML/CSS, Termux, Linux, Android.',
    '3. عندما يُطلب كود، اكتبه كاملاً بدون اختصار.',
    '4. نظّم الردود بعناوين ونقاط.',
    '5. إذا لم تكن متأكداً، قل ذلك بصراحة.',
    '6. خاطب المستخدم بأسلوب ودود واحترافي.',
    '"""',
    '',
]
PROJECT_FILES["app/prompts/system_prompt.py"] = "\n".join(_sys_lines)


# ============================================================
# 9) Router
# ============================================================

PROJECT_FILES["app/services/ai/router.py"] = r"""import logging
from typing import Optional, Tuple
from app.services.ai.gemini import GeminiProvider
from app.services.ai.groq import GroqProvider
from app.services.ai.openrouter import OpenRouterProvider
from app.services.ai.deepseek import DeepSeekProvider
from app.prompts.system_prompt import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class AIRouter:
    def __init__(self):
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
                    return response, name
                errors.append(name + ": empty")
            except Exception as e:
                logger.warning("Provider %s failed: %s", name, e)
                errors.append(name + ": " + str(e)[:80])

        logger.error("All providers failed: %s", errors)
        return (
            "عذراً، تعذر الاتصال بخادم الذكاء الاصطناعي. حاول مرة أخرى بعد قليل.",
            "none",
        )


ai_router = AIRouter()
"""


# ============================================================
# 10) Chat Service
# ============================================================

PROJECT_FILES["app/services/chat_service.py"] = r"""from typing import Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.chat import ChatRepository
from app.services.ai.router import ai_router


class ChatService:
    def __init__(self, db: AsyncSession):
        self.repo = ChatRepository(db)

    async def process_chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> Dict:
        conv = await self.repo.get_or_create_conversation(conversation_id)
        await self.repo.add_message(conv.id, "user", message)

        response_text, provider_used = await ai_router.generate_response(
            message, image_base64, media_type
        )

        await self.repo.add_message(
            conv.id, "assistant", response_text, provider=provider_used
        )

        return {
            "success": True,
            "conversation_id": conv.id,
            "message": response_text,
            "provider": provider_used,
        }
"""


# ============================================================
# 11) App Generator (PWA)
# ============================================================

PROJECT_FILES["app/services/app_builder.py"] = r"""import os
import uuid
import re
from datetime import datetime


class AppBuilderService:
    @staticmethod
    def _safe_name(name: str) -> str:
        return re.sub(r"[^a-zA-Z0-9_-]", "_", name.strip())[:40] or "app"

    @staticmethod
    async def build_pwa(app_name: str, html_content: str) -> str:
        os.makedirs("static/apps", exist_ok=True)
        safe = AppBuilderService._safe_name(app_name)
        token = str(uuid.uuid4())[:8]
        filename = safe + "_" + token + ".html"
        path = os.path.join("static/apps", filename)

        manifest = (
            '{"name":"' + app_name + '","short_name":"' + app_name[:12] + '",'
            '"start_url":".","display":"standalone","background_color":"#0f172a",'
            '"theme_color":"#06b6d4","icons":[]}'
        )

        full_html = (
            '<!DOCTYPE html><html lang="ar" dir="rtl"><head>'
            '<meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<meta name="theme-color" content="#06b6d4">'
            '<title>' + app_name + '</title>'
            '<link rel="manifest" href="data:application/json;charset=utf-8,'
            + manifest.replace("#", "%23") + '">'
            '<style>body{font-family:system-ui;margin:0;padding:20px;'
            'background:#0f172a;color:#f8fafc}</style>'
            '</head><body>' + html_content + '</body></html>'
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write(full_html)

        return "/static/apps/" + filename
"""


# ============================================================
# 12) API Endpoints
# ============================================================

PROJECT_FILES["app/api/v1/endpoints/chat.py"] = r"""import logging
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
"""

PROJECT_FILES["app/api/v1/endpoints/system.py"] = r"""from fastapi import APIRouter
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
"""

PROJECT_FILES["app/api/v1/router.py"] = r"""from fastapi import APIRouter
from app.api.v1.endpoints import chat, system

api_router = APIRouter()
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(system.router, tags=["system"])
"""


# ============================================================
# 13) Main App
# ============================================================

PROJECT_FILES["app/main.py"] = r"""import os
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
async def read_root(request: Request):
    response = templates.TemplateResponse(
        request=request, name="index.html",
        context={"version": settings.APP_VERSION}
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
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
"""

PROJECT_FILES["app.py"] = r"""from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
"""


# ============================================================
# 14) HTML Template (Arabic + Voice + App Generator + Auto-Update)
# ============================================================

PROJECT_FILES["templates/index.html"] = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="theme-color" content="#06b6d4">
<title>أبو رامي AI</title>
<style>
:root {
  --bg-deep: #050b14;
  --cyan: #06b6d4;
  --sky: #38bdf8;
  --text: #f8fafc;
  --muted: #94a3b8;
  --danger: #ef4444;
  --success: #10b981;
}
* { box-sizing: border-box; margin: 0; padding: 0;
    font-family: system-ui, -apple-system, "Segoe UI", Tahoma, sans-serif;
    -webkit-tap-highlight-color: transparent; }
body { background: var(--bg-deep); color: var(--text); height: 100vh;
       display: flex; overflow: hidden; }

/* Splash */
#splash { position: fixed; inset: 0; background: #000; z-index: 2000;
          display: flex; flex-direction: column; align-items: center;
          justify-content: center; transition: opacity 0.8s; }
#splash.hidden { opacity: 0; pointer-events: none; }
#splash h1 { font-size: 2.8rem; font-weight: 900;
             background: linear-gradient(45deg, #06b6d4, #38bdf8, #fff);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
             filter: drop-shadow(0 0 15px var(--cyan)); margin-bottom: 12px; }
#splash p { color: var(--muted); font-size: 1.1rem; margin-bottom: 30px; }
#splash button { padding: 12px 40px; background: var(--cyan); border: none;
                 border-radius: 24px; font-size: 1.1rem; font-weight: bold;
                 cursor: pointer; }

/* Layout */
.app { display: flex; width: 100%; height: 100%; }

/* Sidebar */
.sidebar { width: 280px; background: rgba(6,182,212,0.04);
           backdrop-filter: blur(12px);
           border-left: 1px solid rgba(255,255,255,0.08);
           padding: 16px; display: flex; flex-direction: column; gap: 12px; }
.sidebar h2 { color: var(--cyan); font-size: 1.2rem; margin-bottom: 4px; }
.status { font-size: 0.8rem; color: var(--muted); }
.status span { color: var(--success); }
.btn { padding: 10px; background: rgba(255,255,255,0.05); color: var(--text);
       border: 1px solid rgba(255,255,255,0.15); border-radius: 10px;
       cursor: pointer; font-size: 0.95rem; transition: all 0.2s;
       display: flex; align-items: center; justify-content: center; gap: 8px; }
.btn:hover { background: rgba(6,182,212,0.15); border-color: var(--cyan); }
.btn.primary { background: var(--cyan); color: #000; border: none;
               font-weight: bold; }

/* Main */
.main { flex: 1; display: flex; flex-direction: column;
        background: radial-gradient(circle at 50% 50%, #0f172a 0%, #050b14 100%); }
.messages { flex: 1; overflow-y: auto; padding: 20px;
            display: flex; flex-direction: column; gap: 14px;
            scroll-behavior: smooth; }
.msg { max-width: 85%; padding: 14px 18px; border-radius: 16px;
       line-height: 1.7; font-size: 0.98rem; word-wrap: break-word;
       animation: fadeIn 0.3s ease; white-space: pre-wrap; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); }
                    to { opacity: 1; transform: translateY(0); } }
.msg.user { background: linear-gradient(135deg, #06b6d4, #0284c7);
            color: #fff; align-self: flex-start;
            border-bottom-right-radius: 4px; }
.msg.assistant { background: rgba(255,255,255,0.06);
                 backdrop-filter: blur(10px);
                 border: 1px solid rgba(255,255,255,0.1);
                 align-self: flex-end; border-bottom-left-radius: 4px; }
.msg.error { color: var(--danger); border-color: var(--danger); }

/* Input */
.input-area { padding: 14px; background: rgba(10,25,47,0.85);
              backdrop-filter: blur(20px);
              border-top: 1px solid rgba(255,255,255,0.08);
              display: flex; gap: 8px; align-items: flex-end; }
textarea { flex: 1; height: 46px; min-height: 46px; max-height: 180px;
           background: rgba(255,255,255,0.05);
           border: 1px solid rgba(255,255,255,0.15);
           border-radius: 23px; padding: 12px 18px; color: #fff;
           resize: none; outline: none; font-size: 0.98rem; }
textarea:focus { border-color: var(--cyan); }
.icon-btn { width: 46px; height: 46px; border-radius: 50%;
            background: rgba(6,182,212,0.15); border: 1px solid var(--cyan);
            color: var(--cyan); cursor: pointer; display: flex;
            align-items: center; justify-content: center;
            font-size: 1.3rem; transition: all 0.25s; flex-shrink: 0; }
.icon-btn:hover { background: var(--cyan); color: #000;
                  transform: scale(1.08); }
.icon-btn.send { background: var(--cyan); color: #000; }

/* Voice Overlay */
#voice-overlay { position: fixed; inset: 0; z-index: 1500;
                 background: rgba(5,11,20,0.95);
                 backdrop-filter: blur(25px); display: none;
                 flex-direction: column; align-items: center;
                 justify-content: center; gap: 30px; }
#voice-overlay.active { display: flex; }
.orb { width: 140px; height: 140px; border-radius: 50%;
       background: radial-gradient(circle, #38bdf8, #06b6d4);
       filter: drop-shadow(0 0 30px var(--cyan));
       animation: pulse 2s infinite alternate; }
@keyframes pulse { 0% { transform: scale(0.9); }
                   100% { transform: scale(1.15); } }
#voice-text { color: var(--cyan); font-size: 1.2rem; text-align: center;
              max-width: 80%; }
#voice-heard { color: var(--muted); font-size: 1rem; text-align: center;
               max-width: 80%; font-style: italic; }

/* Modal */
.modal { position: fixed; inset: 0; background: rgba(0,0,0,0.85);
         z-index: 1600; display: none; align-items: center;
         justify-content: center; padding: 16px; }
.modal.active { display: flex; }
.modal-body { width: 100%; max-width: 460px; background: #0f172a;
              border: 1px solid var(--cyan); border-radius: 18px;
              padding: 24px; display: flex; flex-direction: column; gap: 14px; }
.modal-body h3 { color: var(--cyan); margin-bottom: 6px; }
.modal-body input, .modal-body textarea {
  width: 100%; background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.15); padding: 12px;
  color: #fff; border-radius: 10px; font-size: 1rem;
  font-family: inherit; outline: none;
}
.modal-body input:focus, .modal-body textarea:focus { border-color: var(--cyan); }

/* Update Banner */
#update-banner { position: fixed; top: 12px; left: 50%;
                 transform: translateX(-50%);
                 background: var(--cyan); color: #000;
                 padding: 10px 20px; border-radius: 24px;
                 font-weight: bold; z-index: 3000; cursor: pointer;
                 display: none; box-shadow: 0 4px 20px rgba(6,182,212,0.5); }
#update-banner.active { display: block; animation: slideDown 0.4s ease; }
@keyframes slideDown { from { transform: translate(-50%, -60px); }
                       to { transform: translate(-50%, 0); } }

/* Mobile */
@media (max-width: 700px) {
  .sidebar { display: none; }
}
</style>
</head>
<body>

<div id="update-banner" onclick="location.reload(true)">
  تحديث جديد متاح — اضغط للتحديث
</div>

<div id="splash">
  <h1>أبو رامي AI</h1>
  <p>لسنا الوحيدين، لكن الأفضل بذكاء</p>
  <button onclick="closeSplash()">ابدأ الآن</button>
</div>

<div class="app">
  <aside class="sidebar">
    <h2>أبو رامي AI</h2>
    <div class="status">الحالة: <span id="status-text">جاري الفحص...</span></div>
    <div class="status">الإصدار: <span id="version-text">-</span></div>
    <button class="btn" onclick="newChat()">محادثة جديدة</button>
    <button class="btn" onclick="openAppModal()">توليد تطبيق</button>
    <button class="btn" onclick="checkUpdate(true)">فحص التحديثات</button>
  </aside>

  <main class="main">
    <div class="messages" id="messages">
      <div class="msg assistant">مرحباً بك! أنا أبو رامي AI. يمكنني مساعدتك في البرمجة، الإجابة عن الأسئلة، وتوليد تطبيقات كاملة. كيف أخدمك؟</div>
    </div>

    <div class="input-area">
      <button class="icon-btn" onclick="toggleVoice()" title="محادثة صوتية">🎙️</button>
      <textarea id="input" placeholder="اكتب رسالتك..." rows="1"></textarea>
      <button class="icon-btn send" onclick="send()" title="إرسال">➤</button>
    </div>
  </main>
</div>

<div id="voice-overlay">
  <div class="orb"></div>
  <div id="voice-text">جاري الاستماع...</div>
  <div id="voice-heard"></div>
  <button class="btn primary" onclick="toggleVoice()" style="padding: 12px 30px;">إيقاف</button>
</div>

<div class="modal" id="app-modal">
  <div class="modal-body">
    <h3>توليد تطبيق جديد</h3>
    <input id="app-name" placeholder="اسم التطبيق (مثال: Notes App)" />
    <textarea id="app-desc" rows="4" placeholder="اوصف التطبيق: ماذا يفعل؟ ما شاشته؟"></textarea>
    <button class="btn primary" onclick="generateApp()" style="padding: 14px;">توليد التطبيق</button>
    <button class="btn" onclick="closeAppModal()">إلغاء</button>
  </div>
</div>

<script>
const $ = (id) => document.getElementById(id);
let currentConv = null;
let currentVersion = null;

function closeSplash() { $('splash').classList.add('hidden'); }

async function checkStatus() {
  try {
    const r = await fetch('/v1/system/status');
    if (r.ok) {
      const d = await r.json();
      $('status-text').innerText = 'متصل';
      $('status-text').style.color = '#10b981';
      $('version-text').innerText = d.version || '-';
      currentVersion = d.version;
    }
  } catch (e) {
    $('status-text').innerText = 'غير متصل';
    $('status-text').style.color = '#ef4444';
  }
}
checkStatus();

async function checkUpdate(manual) {
  try {
    const r = await fetch('/version?t=' + Date.now());
    const d = await r.json();
    if (currentVersion && d.version && d.version !== currentVersion) {
      $('update-banner').classList.add('active');
      if (manual) alert('يوجد تحديث جديد: ' + d.version);
    } else if (manual) {
      alert('أنت على أحدث إصدار: ' + d.version);
    }
  } catch (e) {
    if (manual) alert('تعذر فحص التحديثات');
  }
}
setInterval(() => checkUpdate(false), 60000);

function escapeHtml(text) {
  const d = document.createElement('div');
  d.textContent = text;
  return d.innerHTML;
}

function addMsg(text, cls) {
  const div = document.createElement('div');
  div.className = 'msg ' + cls;
  div.textContent = text;
  $('messages').appendChild(div);
  $('messages').scrollTop = $('messages').scrollHeight;
  return div;
}

async function send() {
  const text = $('input').value.trim();
  if (!text) return;

  addMsg(text, 'user');
  $('input').value = '';
  $('input').style.height = '46px';

  const thinking = addMsg('... جاري التفكير', 'assistant');
  thinking.style.opacity = '0.6';

  try {
    const r = await fetch('/v1/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, conversation_id: currentConv })
    });
    const d = await r.json();
    if (d.conversation_id) currentConv = d.conversation_id;
    thinking.remove();
    addMsg(d.message || 'لا يوجد رد', 'assistant');
    if (voiceEnabled) speak(d.message || '');
  } catch (e) {
    thinking.remove();
    addMsg('تعذر الاتصال بالخادم. حاول مرة أخرى.', 'assistant error');
  }
}

function newChat() {
  currentConv = null;
  $('messages').innerHTML = '<div class="msg assistant">محادثة جديدة بدأت. كيف أخدمك؟</div>';
}

// Voice
let recognition = null;
let voiceEnabled = false;

function toggleVoice() {
  const overlay = $('voice-overlay');
  const isActive = overlay.classList.contains('active');

  if (!isActive) {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert('المتصفح لا يدعم التعرف على الصوت');
      return;
    }
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SR();
    recognition.lang = 'ar-SA';
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = (e) => {
      let text = '';
      for (let i = e.resultIndex; i < e.results.length; i++) {
        text += e.results[i][0].transcript;
      }
      $('voice-heard').innerText = text;
      if (e.results[e.results.length - 1].isFinal) {
        $('input').value = text.trim();
        overlay.classList.remove('active');
        recognition.stop();
        voiceEnabled = true;
        send();
      }
    };

    recognition.onerror = () => {
      overlay.classList.remove('active');
    };

    recognition.start();
    overlay.classList.add('active');
    $('voice-text').innerText = 'جاري الاستماع... تحدث الآن';
    $('voice-heard').innerText = '';
  } else {
    overlay.classList.remove('active');
    if (recognition) recognition.stop();
  }
}

function speak(text) {
  if (!('speechSynthesis' in window)) return;
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'ar-SA';
  u.rate = 1.0;
  window.speechSynthesis.speak(u);
}

// App Generator
function openAppModal() { $('app-modal').classList.add('active'); }
function closeAppModal() { $('app-modal').classList.remove('active'); }

async function generateApp() {
  const name = $('app-name').value.trim();
  const desc = $('app-desc').value.trim();
  if (!name || !desc) { alert('الرجاء إدخال الاسم والوصف'); return; }

  closeAppModal();
  addMsg('طلب توليد تطبيق: ' + name, 'user');
  const loading = addMsg('جاري بناء تطبيقك... قد يستغرق 20 ثانية', 'assistant');

  try {
    const r = await fetch('/v1/generate/app', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ app_name: name, description: desc })
    });
    const d = await r.json();
    loading.remove();
    if (d.app_url) {
      const link = '<div class="msg assistant">تم توليد التطبيق بنجاح!<br>'
        + '<a href="' + d.app_url + '" target="_blank" '
        + 'style="color:#06b6d4; font-weight:bold;">'
        + 'اضغط لفتح التطبيق</a>'
        + '<br><small style="color:#94a3b8;">'
        + 'افتحه في Chrome ← ⋮ ← إضافة إلى الشاشة الرئيسية</small></div>';
      $('messages').insertAdjacentHTML('beforeend', link);
      $('messages').scrollTop = $('messages').scrollHeight;
    } else {
      addMsg('تعذر توليد التطبيق.', 'assistant error');
    }
  } catch (e) {
    loading.remove();
    addMsg('فشل التوليد: ' + e.message, 'assistant error');
  }
}

// Input autosize
$('input').addEventListener('input', function () {
  this.style.height = '46px';
  this.style.height = Math.min(this.scrollHeight, 180) + 'px';
});

$('input').addEventListener('keydown', function (e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    send();
  }
});
</script>

</body>
</html>
"""


# ============================================================
# 15) Android
# ============================================================

PROJECT_FILES["android/app/src/main/AndroidManifest.xml"] = r"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.aburami.ai">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />

    <application
        android:allowBackup="true"
        android:label="أبو رامي AI"
        android:supportsRtl="true"
        android:usesCleartextTraffic="true"
        android:theme="@android:style/Theme.NoTitleBar">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""

PROJECT_FILES["android/app/src/main/java/com/aburami/ai/MainActivity.kt"] = r"""package com.aburami.ai

import android.Manifest
import android.app.DownloadManager
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.webkit.PermissionRequest
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private val SERVER_URL = "https://abu-rami-app.onrender.com/"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
            != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.RECORD_AUDIO),
                101
            )
        }

        webView = WebView(this)
        setContentView(webView)

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            mediaPlaybackRequiresUserGesture = false
            cacheMode = WebSettings.LOAD_NO_CACHE
            allowFileAccess = true
            databaseEnabled = true
        }

        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(
                view: WebView?, url: String?
            ): Boolean {
                if (url != null && url.contains("/static/apps/")) {
                    val intent = android.content.Intent(
                        android.content.Intent.ACTION_VIEW,
                        Uri.parse(url)
                    )
                    startActivity(intent)
                    return true
                }
                return false
            }
        }

        webView.webChromeClient = object : WebChromeClient() {
            override fun onPermissionRequest(request: PermissionRequest?) {
                request?.grant(request.resources)
            }
        }

        webView.setDownloadListener { url, _, _, _, _ ->
            val req = DownloadManager.Request(Uri.parse(url))
            req.setNotificationVisibility(
                DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED
            )
            req.setDestinationInExternalPublicDir(
                Environment.DIRECTORY_DOWNLOADS, "app.html"
            )
            val dm = getSystemService(DOWNLOAD_SERVICE) as DownloadManager
            dm.enqueue(req)
        }

        // إضافة كاش بريكر لضمان التحديث الفوري
        webView.loadUrl(SERVER_URL + "?v=" + System.currentTimeMillis())
    }

    override fun onBackPressed() {
        if (::webView.isInitialized && webView.canGoBack()) {
            webView.goBack()
        } else {
            @Suppress("DEPRECATION")
            super.onBackPressed()
        }
    }
}
"""

PROJECT_FILES["android/app/build.gradle"] = r"""plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.aburami.ai'
    compileSdk 34
    defaultConfig {
        applicationId "com.aburami.ai"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }
    buildTypes { release { minifyEnabled false } }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = '17' }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'androidx.core:core-ktx:1.12.0'
}
"""


# ============================================================
# 16) GitHub Actions
# ============================================================

PROJECT_FILES[".github/workflows/build.yml"] = r"""name: Python CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Syntax check
        run: python -m compileall app
"""


# ============================================================
# 17) Generator
# ============================================================

def generate_project():
    print("=" * 65)
    print("بدء توليد مشروع [أبو رامي AI] النسخة الشاملة")
    print("=" * 65)

    count = 0
    for path, content in PROJECT_FILES.items():
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content if content.endswith("\n") else content + "\n")
        print(" [+] " + path)
        count += 1

    os.makedirs("static/apps", exist_ok=True)
    os.makedirs("templates", exist_ok=True)

    print("=" * 65)
    print("اكتمل التوليد بنجاح! عدد الملفات: " + str(count))
    print("=" * 65)
    print("الخطوات التالية:")
    print("  1. pip install -r requirements.txt")
    print("  2. cp .env.example .env")
    print("  3. nano .env  (ضع المفاتيح)")
    print("  4. uvicorn app.main:app --reload")
    print("=" * 65)


if __name__ == "__main__":
    generate_project()
