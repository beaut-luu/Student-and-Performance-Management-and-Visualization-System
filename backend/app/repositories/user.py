# UserRepository：user专用 查询/插入/更新权限/改密/删除
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from typing import Optional


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def select_one_by_username(self, username: str) -> Optional[User]:
        return await self.select_one(User.username == username)

    async def select_one_by_email(self, email: str) -> Optional[User]:
        return await self.select_one(User.email == email)

    async def select_one_by_stu_num(self, stu_num: str) -> Optional[User]:
        return await self.select_one(User.stu_number == stu_num)

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
                          email: str | None, stu_number: str,
                          name: str) -> bool:
        user_dict = {'username': username, 'pwd_hash': pwd_hash, 'email': email, 'stu_number': stu_number, 'name': name}
        user = User(**user_dict)
        await self.insert_into(user)
        res = await self.select_one_by_username(username)
        if res is not None:
            return True
        return False

