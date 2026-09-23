from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Boolean, BIGINT
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.user import User
    from app.models.activity import Activity
    from app.models.org_member import OrgMember


class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    logo: Mapped[str] = mapped_column(  # logo的url
        String(256)
    )
    description: Mapped[str] = mapped_column(
        String(400),
        nullable=False
    )
    contact: Mapped[str] = mapped_column(  # 社团联系方式
        String(64),
        nullable=False
    )
    is_delete: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False
    )
    owner_stu_num: Mapped[int] = mapped_column(
        BIGINT(),
        ForeignKey("user.stu_number"),
        nullable=False
    )
    owner: Mapped["User"] = relationship(foreign_keys=[owner_stu_num],
                                         lazy="raise",
                                         back_populates="org_owner")  # type: ignore
    # 组织解散 → 连带删除其名下活动与成员关系(活动离开组织无独立意义)
    activity: Mapped[list["Activity"]] = relationship(foreign_keys="[Activity.org_id]",
                                                      lazy="raise",
                                                      cascade="all, delete-orphan",
                                                      back_populates="org")  # type: ignore
    member: Mapped[list["OrgMember"]] = relationship(foreign_keys="[OrgMember.org_id]",
                                                     lazy="raise",
                                                     cascade="all, delete-orphan",
                                                     back_populates="org")
