from sqlalchemy import select, Row
from sqlalchemy.orm import selectinload

from app.models.enums import OrganizationRole
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from typing import Optional, Sequence
from app.models.org_member import OrgMember
from app.models.organization import Organization


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def select_one_by_username(self, username: str) -> Optional[User]:
        return await self.select_one(User.username == username, User.is_delete.is_(False))

    async def select_one_by_email(self, email: str) -> Optional[User]:
        return await self.select_one(User.email == email, User.is_delete.is_(False))

    async def select_one_by_stu_num(self, stu_num: int) -> Optional[User]:
        return await self.select_one(User.stu_number == stu_num, User.is_delete.is_(False))

# 当select(A模型, B.字段),查询返回多列、多个来源(模型实例+单独字段),execute()返回的每一行就是Row
    async def select_my_org_and_role(self, stu_num: int) -> Sequence[Row[tuple[Organization, OrganizationRole]]]:
        stmt = (
            select(Organization, OrgMember.role)
            .join(OrgMember, Organization.id == OrgMember.org_id)
            .where(OrgMember.member_stu_num == stu_num,
                   OrgMember.is_delete.is_(False), Organization.is_delete.is_(False))
        )
        res = await self.db.execute(stmt)
        return res.all()

    async def select_my_info(self, stu_num: int) -> User:
        stmt = (select(User)
                .where(User.stu_number == stu_num, User.is_delete.is_(False))
                .options(selectinload(User.org_member.and_(OrgMember.is_delete.is_(False))))
                )
        res = await self.db.execute(stmt)
        return res.scalar_one()

    async def delete_by_username(self, username: str) -> bool:
        res = await self.select_one_by_username(username)
        if res is not None:
            await self.delete_one(res)
            return True
        return False

    async def update_model(self, old_username: str, **values) -> bool:
        res = await self.select_one_by_username(old_username)
        if res is not None:
            await self.update_one(res.id, **values)
            return True
        return False

    async def update_pwdhash(self, username: str, newpwdhash: str) -> bool:
        return await self.update_model(username, pwd_hash=newpwdhash)

    async def update_jurisdiction(self, username: str, jur: str) -> bool:
        return await self.update_model(username, jurisdiction=jur)

    async def update_username(self, username: str, newname: str) -> bool:
        return await self.update_model(username, username=newname)

    async def update_email(self, username: str, email: str) -> bool:
        return await self.update_model(username, email=email)

    async def insert_user(self, username: str, pwd_hash: str,
                          email: str | None, stu_number: int,
                          name: str) -> User:
        user_dict = {'username': username, 'pwd_hash': pwd_hash, 'email': email, 'stu_number': stu_number, 'name': name}
        return await self.insert_into(User(**user_dict))
