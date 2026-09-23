from app.models.chat_message import ChatMessage
from app.models.enums import ChatMessageStatus
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ChatMessageRepository(BaseRepository[ChatMessage]):
    def __init__(self, db: AsyncSession):
        super().__init__(ChatMessage, db)

    async def select_by_chat_msg_id(self, chat_msg_id: int) -> ChatMessage | None:
        return await self.select_one(ChatMessage.id == chat_msg_id)

    async def update_model(self, chat_msg_id: int, **value) -> bool:
        res = await self.select_by_chat_msg_id(chat_msg_id)
        if res is not None:
            await self.update_one(chat_msg_id, **value)
            return True
        return False

    async def update_status(self, status: ChatMessageStatus, chat_msg_id: int) -> bool:
        return await self.update_model(chat_msg_id, status=status)

    async def update_content(self, content: str, chat_msg_id: int) -> bool:
        return await self.update_model(chat_msg_id, content=content)

    async def update_is_delete(self, is_delete: bool, chat_msg_id: int) -> bool:
        return await self.update_model(chat_msg_id, is_delete=is_delete)
