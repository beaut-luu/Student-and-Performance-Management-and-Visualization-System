# 泛型 AsyncRepository（get_by/insert/update/delete）
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base
from typing import Generic, Sequence, TypeVar, Optional

# 创建一个 类 型占位符，绑定这个类只能是Base的子类
ModelT = TypeVar("ModelT", bound=Base)  # 'TypeVar()' 的实参必须为字符串，且该字符串与被赋予该字符串的变量名称相同


# Generic[ModelT]表示告诉类内部这是一个 类 型占位符，等后面会传进来
class BaseRepository(Generic[ModelT]):
    # ModelT是实例,type[ModelT]则是一个 类 型
    # User()与User的区别
    def __init__(self, model: type[ModelT], db: AsyncSession):
        self.model = model
        self.db = db

    async def insert_into(self, orm_object: ModelT) -> None:
        self.db.add(orm_object)
        await self.db.commit()

    async def delete_one(self, orm_object: ModelT) -> None:
        await self.db.delete(orm_object)
        await self.db.commit()

    async def update_one(self, db_row_id: int, **values) -> None:
        await self.db.execute(update(self.model).where(self.model.id == db_row_id).values(**values))
        await self.db.commit()

    async def select_all(self) -> Sequence[ModelT]:
        res = await self.db.execute(select(self.model))
        return res.scalars().all()

    async def select_one(self, *where_sql) -> Optional[ModelT]:  # 3.9语法可以是None也可以是[]内的
        res = await self.db.execute(select(self.model).where(*where_sql))  # 加*将元组解包变为若干独立条件
        return res.scalar_one_or_none()

    async def select_many(self, *where_sql) -> Sequence[ModelT]:
        res = await self.db.execute(select(self.model).where(*where_sql))
        return res.scalars().all()
