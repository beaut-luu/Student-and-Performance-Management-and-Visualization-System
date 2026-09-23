from app.models.organization import Organization
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, db: AsyncSession):
        super().__init__(Organization, db)

    async def select_by_organization_id(self, org_id: int) -> Organization | None:
        return await self.select_one(Organization.id == org_id)

    async def update_model(self, org_id: int, **value) -> bool:
        res = await self.select_by_organization_id(org_id)
        if res is not None:
            await self.update_one(org_id, **value)
            return True
        return False

    async def update_name(self, name: str, org_id: int) -> bool:
        return await self.update_model(org_id, name=name)

    async def update_logo(self, logo: str, org_id: int) -> bool:
        return await self.update_model(org_id, logo=logo)

    async def update_description(self, description: str, org_id: int) -> bool:
        return await self.update_model(org_id, description=description)

    async def update_contact(self, contact: str, org_id: int) -> bool:
        return await self.update_model(org_id, contact=contact)

    async def update_owner_stu_num(self, owner_stu_num: int, org_id: int) -> bool:
        return await self.update_model(org_id, owner_stu_num=owner_stu_num)

    async def update_is_delete(self, is_delete: bool, org_id: int) -> bool:
        return await self.update_model(org_id, is_delete=is_delete)
