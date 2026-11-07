from app.core.database import AsyncSessionLocal
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import decode_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional
from app.core.exceptions import UserNotLogInError
from app.repositories.user import UserRepository
from app.repositories.activity import ActivityRepository
from app.repositories.organization import OrganizationRepository
from app.repositories.message_center import MsgCenterRepository


# sql操作依赖session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        else:
            await session.commit()
        finally:
            await session.close()


def d_urepo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def d_arepo(db: AsyncSession = Depends(get_db)) -> ActivityRepository:
    return ActivityRepository(db)


def d_orepo(db: AsyncSession = Depends(get_db)) -> OrganizationRepository:
    return OrganizationRepository(db)


def m_urepo(db: AsyncSession = Depends(get_db)) -> MsgCenterRepository:
    return MsgCenterRepository(db)


bearer = HTTPBearer(auto_error=False)  # 空的时候不报错


async def get_current_user(urepo: UserRepository = Depends(d_urepo),
                           cred: Optional[HTTPAuthorizationCredentials] = Depends(bearer)) -> User:
    """当解析Depends(bearer)时会自动执行bearer也就是HTTPBearer类的实例，
    这个类里面会自动读取request寻找token"""
    # 解析token获取username，查询数据库返回User
    if cred is None:
        raise UserNotLogInError('当前用户未登录')
    token = cred.credentials
    try:
        payload = decode_token(token)
        username = payload.get('sub')
    except Exception:
        raise UserNotLogInError('token无效')
    user = await urepo.select_one_by_username(username)
    if user is None:
        raise UserNotLogInError('当前用户不存在')
    return user
