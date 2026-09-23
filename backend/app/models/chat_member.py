from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, DateTime, Boolean, BigInteger, UniqueConstraint, Index, func, ForeignKey, BIGINT
from datetime import datetime
from app.models.base import Base
from app.models.enums import GroupRole
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.chatgroup import ChatGroup
    from app.models.user import User


class ChatGroupMember(Base):
    __tablename__ = 'chat_group_member'

    id: Mapped[int] = mapped_column(  # 主键
        primary_key=True,
        autoincrement=True
    )
    group_id: Mapped[int] = mapped_column(  # 群id
        ForeignKey("chat_group.id"),
        nullable=False
    )
    group: Mapped["ChatGroup"] = relationship(foreign_keys=[group_id],
                                              lazy="raise",
                                              back_populates="member")  # type: ignore
    user_stu_num: Mapped[int] = mapped_column(  # 成员user.stu_number
        BIGINT(),
        ForeignKey("user.stu_number"),
        nullable=False
    )
    user: Mapped["User"] = relationship(foreign_keys=[user_stu_num],
                                        lazy="raise",
                                        back_populates="chat_member")  # type: ignore
    role: Mapped[GroupRole] = mapped_column(  # 群内角色
        Enum(GroupRole),
        nullable=False,
        default=GroupRole.member
    )
    mute_until: Mapped[datetime | None] = mapped_column(  # 个人禁言到期时间
        DateTime(),
        nullable=True
    )
    last_read_msg_id: Mapped[int | None] = mapped_column(  # 最后已读消息id(未读数核心)
        BigInteger(),
        nullable=True
    )
    is_pinned: Mapped[bool] = mapped_column(  # 是否置顶
        Boolean(),
        nullable=False,
        default=False
    )
    join_time: Mapped[datetime] = mapped_column(  # 入群时间
        DateTime(),
        nullable=False,
        default=func.now()
    )
    is_delete: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False
    )

    __table_args__ = (
        UniqueConstraint('group_id', 'user_stu_num', name='uq_group_member'),
        Index('idx_group_member_user_pinned', 'user_stu_num', 'is_pinned')
    )
