from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from app.models.message_center import MsgCenter
from app.repositories.base import BaseRepository


class MsgCenterRepository(BaseRepository[MsgCenter]):

    def __init__(self, db: AsyncSession):
        super().__init__(MsgCenter, db)

    async def create_msg(self, **values) -> MsgCenter:
        return await self.insert_into(MsgCenter(**values))

    async def update_is_read_to_true(self, msg_id: list[int], stu_num: int) -> None:
        if not msg_id:
            return
        stmt = (
            update(MsgCenter)
            .where(MsgCenter.id.in_(msg_id), MsgCenter.stu_num == stu_num)
            .values(is_read=True)
        )
        await self.db.execute(stmt)
        await self.db.flush()

    async def select_unread_msg(self, stu_num: int) -> Sequence[MsgCenter]:
        return await self.select_many(MsgCenter.stu_num == stu_num, MsgCenter.is_read.is_(False))
