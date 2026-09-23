from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, Boolean, JSON, Enum, Index, ForeignKey
from datetime import datetime
from app.models.enums import ActivityStatus
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.user import User
    from app.models.activity_register import ActivityRegistration


class Activity(Base):
    __tablename__ = 'activity'

    # 操作权限/操作人
    id: Mapped[int] = mapped_column(  # 活动id
        primary_key=True,
        autoincrement=True
    )
    org_id: Mapped[int] = mapped_column(  # 发布方
        ForeignKey("organizations.id"),
        nullable=False,
        index=True
    )
    org: Mapped["Organization"] = relationship(foreign_keys=[org_id],
                                               lazy="raise",
                                               back_populates="activity")  # type: ignore
    creator_stu_num: Mapped[int] = mapped_column(  # 实际操作者
        ForeignKey("user.stu_number"),
        nullable=False,
        index=True
    )
    creator: Mapped["User"] = relationship(foreign_keys=[creator_stu_num],
                                           lazy="raise",
                                           back_populates="create_activities")  # type: ignore

    # 活动介绍
    title: Mapped[str] = mapped_column(  # 活动标题
        String(50),
        nullable=False
    )
    summary: Mapped[str] = mapped_column(  # 活动内容概括
        String(50),
        nullable=False
    )
    content: Mapped[str] = mapped_column(  # 活动内容详情
        Text(),
        nullable=False
    )
    category: Mapped[str] = mapped_column(  # 活动分类
        String(10),
        nullable=False,
        index=True
    )
    location: Mapped[str] = mapped_column(  # 活动地址
        String(50),
        nullable=False
    )
    start_time: Mapped[datetime] = mapped_column(  # 活动开始时间
        DateTime(),
        nullable=False
    )
    end_time: Mapped[datetime] = mapped_column(  # 活动结束时间
        DateTime(),
        nullable=False
    )

    # 报名规则
    register_start: Mapped[datetime | None] = mapped_column(  # 报名起始时间
        DateTime(),
        nullable=True
    )
    register_deadline: Mapped[datetime | None] = mapped_column(  # 报名截至时间
        DateTime(),
        nullable=True
    )
    capacity: Mapped[int | None] = mapped_column(  # 名额上限
        nullable=True
    )
    need_approval: Mapped[bool] = mapped_column(  # 是否需要审核
        Boolean(),
        nullable=False
    )

    # 报名表(JSON)
    fields: Mapped[dict] = mapped_column(  # 报名表自定义模板
        JSON(),
        nullable=False
    )

    checkin: Mapped[bool] = mapped_column(  # 是否开启签到
        Boolean(),
        nullable=False
    )

    status: Mapped[ActivityStatus] = mapped_column(  # 活动状态
        Enum(ActivityStatus),
        nullable=False,
        default=ActivityStatus.draft
    )

    view_count: Mapped[int] = mapped_column(  # 浏览量
        nullable=False,
        default=0
    )
    register_count: Mapped[int] = mapped_column(  # 报名人数
        nullable=False,
        default=0
    )
    is_delete: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False
    )

    __table_args__ = (
        Index('idx_activity_register_time', 'register_start', 'register_deadline'),
        Index('idx_activity_time', 'start_time', 'end_time')
    )
    # 活动删除 → 连带删除其报名记录(报名离开活动无独立意义)
    act_register: Mapped[list["ActivityRegistration"]] = relationship(foreign_keys="[ActivityRegistration.activity_id]",
                                                                      lazy="raise",
                                                                      cascade="all, delete-orphan",
                                                                      back_populates="activity")
