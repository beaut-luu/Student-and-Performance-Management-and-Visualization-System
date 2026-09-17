from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, JSON, DateTime, UniqueConstraint, func
from app.models.base import Base
from app.models.enums import ActivityRegistrationStatus
from datetime import datetime


class ActivityRegistration(Base):
    __tablename__ = 'activity_registration'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True
    )
    activity_id: Mapped[int] = mapped_column(
        nullable=False
    )
    register_stu_num: Mapped[str] = mapped_column(
        String(12),
        nullable=False
    )
    status: Mapped[ActivityRegistrationStatus] = mapped_column(
        Enum(ActivityRegistrationStatus),
        nullable=False,
        default=ActivityRegistrationStatus.pending
    )
    register_data: Mapped[dict] = mapped_column(
        JSON(),
        nullable=False
    )
    apply_time: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False
    )
    review_time: Mapped[datetime | None] = mapped_column(
        DateTime(),
        nullable=True
    )
    review_stu_num: Mapped[str | None] = mapped_column(
        String(12),
        nullable=True
    )
    checkin_time: Mapped[datetime | None] = mapped_column(
        DateTime(),
        nullable=True,
        default=func.now()
    )

    __table_args__ = (
        UniqueConstraint('activity_id', 'register_stu_num', name='uq_act_register'),
    )














