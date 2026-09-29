from typing import Optional, Dict
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
