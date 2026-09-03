# async engine + async_sessionmaker + get_db() 依赖（替代手写连接池）
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# 创建mysql连接链接
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/stu?charset=utf8"

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=5
)


# sql操作依赖session
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 传入异步引擎
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
