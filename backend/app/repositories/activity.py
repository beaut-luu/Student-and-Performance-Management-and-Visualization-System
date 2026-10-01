from datetime import datetime
from sqlalchemy import update
from app.models.activity import Activity
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence


class ActivityRepository(BaseRepository[Activity]):
    def __init__(self, db: AsyncSession):
        super().__init__(Activity, db)

    async def select_by_act_id(self, act_id: int) -> Activity | None:
        return await self.select_one(Activity.id == act_id)

    async def select_by_category(self, category: str) -> Sequence[Activity]:
        return await self.select_many(Activity.category == category)

    async def select_by_title(self, title: str) -> Sequence[Activity]:
        return await self.select_many(Activity.title.like(f"%{title}%"))

    async def select_by_org_id(self, org_id: int) -> Sequence[Activity]:
        return await self.select_many(Activity.org_id == org_id)

    async def delete_by_id(self, act_id: int) -> bool:
        res = await self.select_by_act_id(act_id)
        if res is not None:
            await self.update_is_delete(act_id, True)
            return True
        return False

    async def create_activity(self, **value) -> Activity:
        return await self.insert_into(Activity(**value))

    async def update_model(self, act_id: int, **value) -> bool:
        res = await self.select_by_act_id(act_id)
        if res is not None:
            await self.update_one(act_id, **value)
            return True
        return False

    async def update_title(self, title: str, act_id: int) -> bool:
        return await self.update_model(act_id, title=title)

    async def update_summary(self, summary: str, act_id: int) -> bool:
        return await self.update_model(act_id, summary=summary)

    async def update_content(self, content: str, act_id: int) -> bool:
        return await self.update_model(act_id, content=content)

    async def update_start_time(self, start_time: datetime, act_id: int) -> bool:
        return await self.update_model(act_id, start_time=start_time)

    async def update_end_time(self, end_time: datetime, act_id: int) -> bool:
        return await self.update_model(act_id, end_time=end_time)

    async def update_register_start(self, register_start: datetime | None, act_id: int) -> bool:
        return await self.update_model(act_id, register_start=register_start)

    async def update_register_deadline(self, register_deadline: datetime | None, act_id: int) -> bool:
        return await self.update_model(act_id, register_deadline=register_deadline)

    async def update_capacity(self, capacity: int | None, act_id: int) -> bool:
        return await self.update_model(act_id, capacity=capacity)

    async def update_view_count(self, act_id: int) -> None:
        await self.db.execute(update(Activity)
                              .where(Activity.id == act_id, Activity.is_delete.is_(False))
                              .values(view_count=Activity.view_count + 1))

    async def update_is_delete(self, act_id: int, delete: bool) -> bool:
        return await self.update_model(act_id, is_delete=delete)
