import uuid
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
