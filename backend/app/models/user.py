# User 模型：映射 db_user 表
from sqlalchemy import String, Enum
from app.models.enums import Jurisdiction
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(25),
        nullable=False
    )
    stu_number: Mapped[int] = mapped_column(
        String(12),
        unique=True,
        nullable=False
    )
    email: Mapped[str | None] = mapped_column(
        String(256),
        unique=True,
        nullable=True
    )
    pwd_hash: Mapped[str] = mapped_column(
        String(256),
        nullable=False
    )
    jurisdiction: Mapped[Jurisdiction] = mapped_column(
        Enum(Jurisdiction),
        default=Jurisdiction.user,
        nullable=False
    )
