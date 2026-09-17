from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Enum, DateTime, BigInteger, UniqueConstraint, Index, desc, func
from datetime import datetime
from app.models.base import Base
from app.models.enums import ChatMessageType, ChatMessageStatus


class ChatMessage(Base):
    __tablename__ = 'chat_message'

    id: Mapped[int] = mapped_column(  # 消息id(BIGINT自增,保证顺序)
        BigInteger(),
        primary_key=True,
        autoincrement=True
    )
    group_id: Mapped[int] = mapped_column(  # 群id
        nullable=False
    )
    sender_id: Mapped[int] = mapped_column(  # 发送者user.id
        nullable=False
    )
    type: Mapped[ChatMessageType] = mapped_column(  # 消息类型
        Enum(ChatMessageType),
        nullable=False,
        default=ChatMessageType.text
    )
    content: Mapped[str] = mapped_column(  # 消息内容
        Text(),
        nullable=False
    )
    reply_to_msg_id: Mapped[int | None] = mapped_column(  # 引用回复的消息id
        BigInteger(),
        nullable=True
    )
    client_msg_id: Mapped[str] = mapped_column(  # 前端生成,幂等去重
        String(64),
        nullable=False
    )
    status: Mapped[ChatMessageStatus] = mapped_column(  # 消息状态
        Enum(ChatMessageStatus),
        nullable=False,
        default=ChatMessageStatus.normal
    )
    create_time: Mapped[datetime] = mapped_column(  # 发送时间
        DateTime(),
        nullable=False,
        default=func.now()
    )

    __table_args__ = (
        UniqueConstraint('sender_id', 'client_msg_id', name='uq_message_client_id'),
        Index('idx_chat_message_group_id', 'group_id', desc('id'))
    )
