from typing import Optional
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
