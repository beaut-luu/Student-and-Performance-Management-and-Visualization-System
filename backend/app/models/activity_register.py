from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Boolean, JSON, Enum, ForeignKey, UniqueConstraint
from datetime import datetime
from app.models.enums import ActivityRegistrationStatus
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.user import User
    from app.models.activity import Activity


class ActivityRegistration(Base):
    __tablename__ = 'activity_registration'

    id: Mapped[int] = mapped_column(  # id
        primary_key=True,
        autoincrement=True,
        index=True
    )
    activity_id: Mapped[int] = mapped_column(  # 报名活动id
        ForeignKey("activity.id"),
        nullable=False
    )
    activity: Mapped["Activity"] = relationship(foreign_keys=[activity_id],
                                                lazy="raise",
                                                back_populates="act_register")
    register_stu_num: Mapped[int] = mapped_column(  # 报名人学号
        ForeignKey("user.stu_number"),
        nullable=False
    )
    register: Mapped["User"] = relationship(foreign_keys=[register_stu_num],
                                            lazy="raise",
                                            back_populates="act_register")
    status: Mapped[ActivityRegistrationStatus] = mapped_column(  # 报名人状态
        Enum(ActivityRegistrationStatus),
        nullable=False,
        default=ActivityRegistrationStatus.pending
    )
    register_data: Mapped[dict] = mapped_column(  # 报名人信息
        JSON(),
        nullable=False
    )
    apply_time: Mapped[datetime] = mapped_column(  # 申请时间
        DateTime(),
        nullable=False
    )
    review_time: Mapped[datetime | None] = mapped_column(  # 审核时间
        DateTime(),
        nullable=True
    )
    review_stu_num: Mapped[int | None] = mapped_column(  # 审核人学号
        ForeignKey("user.stu_number"),
        nullable=True
    )
    reviewer: Mapped["User"] = relationship(foreign_keys=[review_stu_num],
                                            lazy="raise",
                                            back_populates="act_reviewer")
    checkin_time: Mapped[datetime | None] = mapped_column(  # 签到时间
        DateTime(),
        nullable=True
    )
    is_delete: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False
    )

    __table_args__ = (
        UniqueConstraint('activity_id', 'register_stu_num', name='uq_act_register'),
    )
