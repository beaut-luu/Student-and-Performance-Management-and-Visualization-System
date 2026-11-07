from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, BIGINT, ForeignKey, Boolean, func, Enum
from datetime import datetime
from typing import TYPE_CHECKING
from app.models.enums import MsgTypeStatus


if TYPE_CHECKING:
    from app.models.user import User


class MsgCenter(Base):
    __tablename__ = 'message_center'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    stu_num: Mapped[int | None] = mapped_column(
        BIGINT(),
        nullable=True,
        index=True
    )

    org_id: Mapped[int | None] = mapped_column(
        nullable=True,
        default=None
    )

    type: Mapped[MsgTypeStatus] = mapped_column(
        Enum(),
        nullable=False,
        default=MsgTypeStatus.all
    )

    title: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    msg: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    create_time: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        index=True,
        default=func.now()
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False
    )
