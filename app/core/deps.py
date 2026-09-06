# get_current_user / require_operator（依赖注入，替代 _current_user 全局态）
# 提供项目的Depends依赖项
from app.core.database import AsyncSessionLocal
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


# sql操作依赖session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_current_user(token: str, db: AsyncSession = Depends(get_db)) -> User:
    # 解析token获取username，查询数据库返回User
    pass
