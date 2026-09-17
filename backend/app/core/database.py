# async engine + async_sessionmaker + get_db() 依赖（替代手写连接池）
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from app.models.base import Base
import app.models  # noqa: F401


# 创建mysql连接链接
ASYNC_DATABASE_URL = settings.database_url

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=5
)


async def create_table():
    """Base.metadata里面装有所有Base的子类的信息"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 传入异步引擎
    class_=AsyncSession,
    expire_on_commit=False
)
