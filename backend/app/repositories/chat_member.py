from datetime import datetime
from app.models.chat_member import ChatGroupMember
from app.models.enums import GroupRole
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ChatMemberRepository(BaseRepository[ChatGroupMember]):
    def __init__(self, db: AsyncSession):
        super().__init__(ChatGroupMember, db)

    async def select_by_chat_member_id(self, chat_member_id: int) -> ChatGroupMember | None:
        return await self.select_one(ChatGroupMember.id == chat_member_id)

    async def update_model(self, chat_member_id: int, **value) -> bool:
        res = await self.select_by_chat_member_id(chat_member_id)
        if res is not None:
            await self.update_one(chat_member_id, **value)
            return True
        return False

    async def update_role(self, role: GroupRole, chat_member_id: int) -> bool:
        return await self.update_model(chat_member_id, role=role)

    async def update_mute_until(self, mute_until: datetime | None, chat_member_id: int) -> bool:
        return await self.update_model(chat_member_id, mute_until=mute_until)

    async def update_last_read_msg_id(self, last_read_msg_id: int | None, chat_member_id: int) -> bool:
        return await self.update_model(chat_member_id, last_read_msg_id=last_read_msg_id)

    async def update_is_pinned(self, is_pinned: bool, chat_member_id: int) -> bool:
        return await self.update_model(chat_member_id, is_pinned=is_pinned)

    async def update_is_delete(self, is_delete: bool, chat_member_id: int) -> bool:
        return await self.update_model(chat_member_id, is_delete=is_delete)
