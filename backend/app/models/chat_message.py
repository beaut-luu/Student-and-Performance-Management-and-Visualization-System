from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (String, Text, Enum, DateTime, BigInteger, UniqueConstraint,
                        Index, desc, func, Boolean, ForeignKey, BIGINT)
from datetime import datetime
from app.models.base import Base
from app.models.enums import ChatMessageType, ChatMessageStatus
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.chatgroup import ChatGroup
    from app.models.user import User


class ChatMessage(Base):
    __tablename__ = 'chat_message'

    id: Mapped[int] = mapped_column(  # 消息id(BIGINT自增,保证顺序)
        BigInteger(),
        primary_key=True,
        autoincrement=True
    )
    group_id: Mapped[int] = mapped_column(  # 群id
        ForeignKey("chat_group.id"),
        nullable=False
    )
    group: Mapped["ChatGroup"] = relationship(foreign_keys=[group_id],
                                              lazy="raise",
                                              back_populates="message")  # type: ignore
    sender_stu_num: Mapped[int] = mapped_column(  # 发送者user.stu_number
        BIGINT(),
        ForeignKey("user.stu_number"),
        nullable=False
    )
    sender: Mapped["User"] = relationship(foreign_keys=[sender_stu_num],
                                          lazy="raise",
                                          back_populates="chat_message")  # type: ignore
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
        ForeignKey("chat_message.id"),
        nullable=True
    )
    # 自引用关系不加级联：删除一条消息不应连带删除它的所有回复
    reply_to: Mapped["ChatMessage | None"] = relationship(foreign_keys=[reply_to_msg_id],
                                                          remote_side=[id],
                                                          lazy="raise",
                                                          back_populates="replies")
    replies: Mapped[list["ChatMessage"]] = relationship(foreign_keys=[reply_to_msg_id],
                                                        lazy="raise",
                                                        back_populates="reply_to")
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
    is_delete: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False
    )

    __table_args__ = (
        UniqueConstraint('sender_stu_num', 'client_msg_id', name='uq_message_client_id'),
        Index('idx_chat_message_group_id', 'group_id', desc('id'))
    )
