from datetime import datetime
from app.models.activity_register import ActivityRegistration
from app.models.enums import ActivityRegistrationStatus
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ActivityRegisterRepository(BaseRepository[ActivityRegistration]):
    def __init__(self, db: AsyncSession):
        super().__init__(ActivityRegistration, db)

    async def select_by_register_id(self, register_id: int) -> ActivityRegistration | None:
        return await self.select_one(ActivityRegistration.id == register_id)

    async def update_model(self, register_id: int, **value) -> bool:
        res = await self.select_by_register_id(register_id)
        if res is not None:
            await self.update_one(register_id, **value)
            return True
        return False

    async def update_status(self, status: ActivityRegistrationStatus, register_id: int) -> bool:
        return await self.update_model(register_id, status=status)

    async def update_register_data(self, register_data: dict, register_id: int) -> bool:
        return await self.update_model(register_id, register_data=register_data)

    async def update_review_stu_num(self, review_stu_num: int | None, register_id: int) -> bool:
        return await self.update_model(register_id, review_stu_num=review_stu_num)

    async def update_review_time(self, review_time: datetime | None, register_id: int) -> bool:
        return await self.update_model(register_id, review_time=review_time)

    async def update_checkin_time(self, checkin_time: datetime | None, register_id: int) -> bool:
        return await self.update_model(register_id, checkin_time=checkin_time)

    async def update_is_delete(self, is_delete: bool, register_id: int) -> bool:
        return await self.update_model(register_id, is_delete=is_delete)
