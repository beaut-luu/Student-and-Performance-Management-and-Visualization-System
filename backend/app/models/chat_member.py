from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum, DateTime, Boolean, BigInteger, UniqueConstraint, Index, func
from datetime import datetime
from app.models.base import Base
from app.models.enums import GroupRole


class ChatGroupMember(Base):
    __tablename__ = 'chat_group_member'

    id: Mapped[int] = mapped_column(  # 主键
        primary_key=True,
        autoincrement=True
    )
    group_id: Mapped[int] = mapped_column(  # 群id
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(  # 成员user.id
        nullable=False
    )
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

    __table_args__ = (
        UniqueConstraint('group_id', 'user_id', name='uq_group_member'),
        Index('idx_group_member_user_pinned', 'user_id', 'is_pinned')
    )
