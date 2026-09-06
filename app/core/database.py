# async engine + async_sessionmaker + get_db() 依赖（替代手写连接池）
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings


# 创建mysql连接链接
ASYNC_DATABASE_URL = settings.database_url

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=5
)


AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 传入异步引擎
    class_=AsyncSession,
    expire_on_commit=False
)
