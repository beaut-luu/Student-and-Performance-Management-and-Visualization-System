from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Organization(Base):
    __tablename__ = "Organizations"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    logo: Mapped[str] = mapped_column(  # logo的url
        String(256)
    )
    description: Mapped[str] = mapped_column(
        String(400),
        nullable=False
    )
    contact: Mapped[str] = mapped_column(  # 社团联系方式
        String(64),
        nullable=False
    )
    owner_stu_number: Mapped[str] = mapped_column(
        String(12),
        nullable=False
    )
