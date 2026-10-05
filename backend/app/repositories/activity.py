from datetime import datetime
from sqlalchemy import update, select, func, Row
from sqlalchemy.orm import selectinload

from app.models.activity import Activity
from app.models.user import User
from app.models.organization import Organization
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from app.models.enums import ActivityStatus


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

    async def get_organization(self, act_id: int) -> Organization | None:
        stmt = (select(Activity)
                .where(Activity.id == act_id, Activity.is_delete.is_(False))
                .options(selectinload(Activity.org.and_(Organization.is_delete.is_(False)))
                         .selectinload(Organization.owner.and_(User.is_delete.is_(False)))))
        res = await self.db.execute(stmt)
        res = res.scalar_one_or_none()
        return res.org

    async def get_activities(self, page: int) -> Sequence[Row[tuple[Activity, str, str]]]:
        offset = (page - 1) * 20
        stmt = (select(Activity, User.name.label('creator_name'), Organization.name.label('org_name'))
                .join(User, Activity.creator_stu_num == User.stu_number)
                .join(Organization, Activity.org_id == Organization.id)
                .where(Activity.status == ActivityStatus.published,
                       Activity.is_delete.is_(False),
                       Activity.end_time > func.now(),
                       User.is_delete.is_(False),
                       Organization.is_delete.is_(False))
                .order_by(Activity.start_time.desc())
                .limit(20)
                .offset(offset)
                )
        res = await self.db.execute(stmt)
        return res.all()

    async def get_activities_count(self) -> int:
        stmt = (select(func.count())
                .select_from(Activity)
                .join(User, Activity.creator_stu_num == User.stu_number)
                .join(Organization, Activity.org_id == Organization.id)
                .where(Activity.status == ActivityStatus.published,
                       Activity.is_delete.is_(False),
                       Activity.end_time > func.now(),
                       User.is_delete.is_(False),
                       Organization.is_delete.is_(False))
                )
        res = await self.db.execute(stmt)
        return res.scalar_one()

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
