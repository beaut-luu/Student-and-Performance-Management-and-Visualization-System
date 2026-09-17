from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Boolean, JSON, Enum, Index
from datetime import datetime
from app.models.enums import ActivityStatus


class Activity(Base):
    __tablename__ = 'activity'

    # 操作权限/操作人
    id: Mapped[int] = mapped_column(  # 活动id
        primary_key=True,
        autoincrement=True
    )
    org_id: Mapped[int | None] = mapped_column(  # 发布方
        nullable=True,
        index=True
    )
    creator_stu_num: Mapped[str] = mapped_column(  # 实际操作者
        String(12),
        nullable=False,
        index=True
    )

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
    fields: Mapped[dict | None] = mapped_column(  # 报名表自定义模板
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
        default=ActivityStatus.published
    )

    view_count: Mapped[int] = mapped_column(  # 浏览量
        nullable=False,
        default=0
    )
    register_count: Mapped[int] = mapped_column(  # 报名人数
        nullable=False,
        default=0
    )

    __table_args__ = (
        Index('idx_activity_register_time', 'register_start', 'register_deadline'),
        Index('idx_activity_time', 'start_time', 'end_time')
    )
























