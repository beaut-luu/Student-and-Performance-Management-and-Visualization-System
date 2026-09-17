from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.core.security import trans_hash
from app.core.exceptions import BizException
from app.core.deps import get_db
from app.models.user import User


class DataSeed:
    def __init__(self, db: AsyncSession, urepo=UserRepository):
        self.urepo = urepo(db)

    async def user_seed(self):
        if await self.urepo.select_one_by_username("admin"):
            return
        if not await self.urepo.insert_user("admin", trans_hash('123456'),
                                            None, "123456789XXX", "admin"):
            raise BizException('data seed插入失败')
        if not await self.urepo.update_jurisdiction("admin", "admin"):
            raise BizException('data seed权限初始化失败')


async def data_seed_init():
    async for session in get_db():
        seed_init = DataSeed(session)
        await seed_init.user_seed()
