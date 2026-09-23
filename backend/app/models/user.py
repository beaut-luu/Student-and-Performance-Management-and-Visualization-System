# User 模型：映射 db_user 表
from sqlalchemy import String, Enum, Boolean, BIGINT
from app.models.enums import Jurisdiction
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:  # 只在类型检查时执行
    from app.models.activity import Activity
    from app.models.activity_register import ActivityRegistration
    from app.models.organization import Organization
    from app.models.chatgroup import ChatGroup
    from app.models.org_member import OrgMember
    from app.models.chat_member import ChatGroupMember
    from app.models.chat_message import ChatMessage


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(25),
        nullable=False
    )
    stu_number: Mapped[int] = mapped_column(
        BIGINT(),
        unique=True,
        nullable=False
    )
    email: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True
    )
    pwd_hash: Mapped[str] = mapped_column(
        String(256),
        nullable=False
    )
    jurisdiction: Mapped[Jurisdiction] = mapped_column(
        Enum(Jurisdiction),
        default=Jurisdiction.user,
        nullable=False
    )
    is_delete: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False
    )
    # 级联策略：用户删除时只清理"附属关系"(成员资格/报名记录)，活动、组织、群、消息一律保留
    create_activities: Mapped[list["Activity"]] = relationship(foreign_keys="[Activity.creator_stu_num]",
                                                               lazy="raise",
                                                               back_populates="creator")  # type: ignore
    org_owner: Mapped[list["Organization"]] = relationship(foreign_keys="[Organization.owner_stu_num]",
                                                           lazy="raise",
                                                           back_populates="owner")  # type: ignore
    org_member: Mapped[list["OrgMember"]] = relationship(foreign_keys="[OrgMember.member_stu_num]",
                                                         lazy="raise",
                                                         cascade="all, delete-orphan",
                                                         back_populates="member")
    act_register: Mapped[list["ActivityRegistration"]] = relationship(foreign_keys="[ActivityRegistration.register_stu_num]",
                                                                      lazy="raise",
                                                                      cascade="all, delete-orphan",
                                                                      back_populates="register")
    act_reviewer: Mapped[list["ActivityRegistration"]] = relationship(foreign_keys="[ActivityRegistration.review_stu_num]",
                                                                      lazy="raise",
                                                                      back_populates="reviewer")
    chat_owner: Mapped[list["ChatGroup"]] = relationship(foreign_keys="[ChatGroup.owner_stu_num]",
                                                         lazy="raise",
                                                         back_populates="owner")  # type: ignore
    chat_member: Mapped[list["ChatGroupMember"]] = relationship(foreign_keys="[ChatGroupMember.user_stu_num]",
                                                                lazy="raise",
                                                                cascade="all, delete-orphan",
                                                                back_populates="user")  # type: ignore
    chat_message: Mapped[list["ChatMessage"]] = relationship(foreign_keys="[ChatMessage.sender_stu_num]",
                                                             lazy="raise",
                                                             back_populates="sender")  # type: ignore
