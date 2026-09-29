from fastapi import APIRouter
from app.api.v1.endpoints import chat, system, abu_olq

api_router = APIRouter()
api_router.include_router(abu_olq.router, tags=["abu-olq"])
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(system.router, tags=["system"])
