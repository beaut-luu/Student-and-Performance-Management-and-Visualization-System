from app.models.org_member import OrgMember
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.enums import OrganizationRole


class OrganizationMemberRepository(BaseRepository[OrgMember]):
    def __init__(self, db: AsyncSession):
        super().__init__(OrgMember, db)

    async def select_by_org_member_id(self, org_member_id: int) -> OrgMember | None:
        return await self.select_one(OrgMember.id == org_member_id)

    async def update_model(self, org_member_id: int, **value) -> bool:
        res = await self.select_by_org_member_id(org_member_id)
        if res is not None:
            await self.update_one(org_member_id, **value)
            return True
        return False

    async def update_role(self, role: OrganizationRole, org_member_id: int) -> bool:
        return await self.update_model(org_member_id, role=role)

    async def update_is_delete(self, is_delete: bool, org_member_id: int) -> bool:
        return await self.update_model(org_member_id, is_delete=is_delete)
