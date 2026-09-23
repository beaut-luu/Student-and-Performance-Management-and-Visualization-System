from datetime import datetime
from app.models.chatgroup import ChatGroup
from app.models.enums import GroupJoinMode, GroupStatus
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ChatGroupRepository(BaseRepository[ChatGroup]):
    def __init__(self, db: AsyncSession):
        super().__init__(ChatGroup, db)

    async def select_by_chat_id(self, chat_id: int) -> ChatGroup | None:
        return await self.select_one(ChatGroup.id == chat_id)

    async def update_model(self, chat_id: int, **value) -> bool:
        res = await self.select_by_chat_id(chat_id)
        if res is not None:
            await self.update_one(chat_id, **value)
            return True
        return False

    async def update_name(self, name: str, chat_id: int) -> bool:
        return await self.update_model(chat_id, name=name)

    async def update_avatar(self, avatar: str | None, chat_id: int) -> bool:
        return await self.update_model(chat_id, avatar=avatar)

    async def update_description(self, description: str | None, chat_id: int) -> bool:
        return await self.update_model(chat_id, description=description)

    async def update_category(self, category: str, chat_id: int) -> bool:
        return await self.update_model(chat_id, category=category)

    async def update_tags(self, tags: list | None, chat_id: int) -> bool:
        return await self.update_model(chat_id, tags=tags)

    async def update_join_mode(self, join_mode: GroupJoinMode, chat_id: int) -> bool:
        return await self.update_model(chat_id, join_mode=join_mode)

    async def update_max_members(self, max_members: int, chat_id: int) -> bool:
        return await self.update_model(chat_id, max_members=max_members)

    async def update_invite_code(self, invite_code: str | None, chat_id: int) -> bool:
        return await self.update_model(chat_id, invite_code=invite_code)

    async def update_owner_stu_num(self, owner_stu_num: int, chat_id: int) -> bool:
        return await self.update_model(chat_id, owner_stu_num=owner_stu_num)

    async def update_member_count(self, member_count: int, chat_id: int) -> bool:
        return await self.update_model(chat_id, member_count=member_count)

    async def update_message_count(self, message_count: int, chat_id: int) -> bool:
        return await self.update_model(chat_id, message_count=message_count)

    async def update_status(self, status: GroupStatus, chat_id: int) -> bool:
        return await self.update_model(chat_id, status=status)

    async def update_last_active_time(self, last_active_time: datetime | None, chat_id: int) -> bool:
        return await self.update_model(chat_id, last_active_time=last_active_time)

    async def update_is_delete(self, is_delete: bool, chat_id: int) -> bool:
        return await self.update_model(chat_id, is_delete=is_delete)
