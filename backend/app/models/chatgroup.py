from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, JSON, DateTime, Index, Boolean, ForeignKey
from datetime import datetime
from app.models.base import Base
from app.models.enums import GroupJoinMode, GroupStatus
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.user import User
    from app.models.chat_member import ChatGroupMember
    from app.models.chat_message import ChatMessage


DEFAULT_MAX_MEMBERS = 200


class ChatGroup(Base):
    __tablename__ = 'chat_group'

    id: Mapped[int] = mapped_column(  # 群id
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(  # 群名称
        String(50),
        nullable=False
    )
    avatar: Mapped[str | None] = mapped_column(  # 群头像
        String(256),
        nullable=True
    )
    description: Mapped[str | None] = mapped_column(  # 群简介
        String(255),
        nullable=True
    )
    category: Mapped[str] = mapped_column(  # 群分类(游戏/旅游/爱好…)
        String(20),
        nullable=False,
        index=True
    )
    owner_stu_num: Mapped[int] = mapped_column(  # 群主user.stu_number
        ForeignKey("user.stu_number"),
        nullable=False
    )
    owner: Mapped["User"] = relationship(foreign_keys=[owner_stu_num],
                                         lazy="raise",
                                         back_populates="chat_owner")  # type: ignore
    tags: Mapped[list | None] = mapped_column(  # 标签
        JSON(),
        nullable=True
    )
    join_mode: Mapped[GroupJoinMode] = mapped_column(  # 入群方式
        Enum(GroupJoinMode),
        nullable=False,
        default=GroupJoinMode.public
    )
    max_members: Mapped[int] = mapped_column(  # 人数上限
        nullable=False,
        default=DEFAULT_MAX_MEMBERS
    )
    invite_code: Mapped[str | None] = mapped_column(  # 邀请码(私密群)
        String(32),
        unique=True,
        nullable=True
    )
    member_count: Mapped[int] = mapped_column(  # 成员数(冗余)
        nullable=False,
        default=0
    )
    message_count: Mapped[int] = mapped_column(  # 消息数(冗余)
        nullable=False,
        default=0
    )
    status: Mapped[GroupStatus] = mapped_column(  # 群状态
        Enum(GroupStatus),
        nullable=False,
        default=GroupStatus.normal
    )
    last_active_time: Mapped[datetime | None] = mapped_column(  # 最后活跃时间(清理僵尸群)
        DateTime(),
        nullable=True
    )
    is_delete: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False
    )

    __table_args__ = (
        Index('idx_chat_group_owner_status', 'owner_stu_num', 'status'),
        Index('idx_chat_group_cleanup', 'status', 'last_active_time')
    )
    # 群解散 → 连带删除成员关系与聊天记录
    member: Mapped[list["ChatGroupMember"]] = relationship(foreign_keys="[ChatGroupMember.group_id]",
                                                           lazy="raise",
                                                           cascade="all, delete-orphan",
                                                           back_populates="group")
    message: Mapped[list["ChatMessage"]] = relationship(foreign_keys="[ChatMessage.group_id]",
                                                        lazy="raise",
                                                        cascade="all, delete-orphan",
                                                        back_populates="group")
