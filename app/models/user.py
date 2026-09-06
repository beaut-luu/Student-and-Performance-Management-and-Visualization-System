# User 模型：映射 db_user 表
from sqlalchemy import String
from app.models.enums import Jurisdiction
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "db_user"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False
    )
    pwd_hash: Mapped[str] = mapped_column(
        String(256),
        nullable=False
    )
    jurisdiction: Mapped[int] = mapped_column(
        TINYINT(1),
        default=Jurisdiction.USER.value,
        nullable=False
    )
