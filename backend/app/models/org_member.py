from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint, Enum, ForeignKey, Boolean, BIGINT
from app.models.base import Base
from app.models.enums import OrganizationRole
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.user import User


class OrgMember(Base):
    __tablename__ = "organization_member"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    org_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False
    )
    org: Mapped["Organization"] = relationship(foreign_keys=[org_id],
                                               lazy="raise",
                                               back_populates="member")
    member_stu_num: Mapped[int] = mapped_column(
        BIGINT(),
        ForeignKey("user.stu_number"),
        nullable=False,
        index=True
    )
    member: Mapped["User"] = relationship(foreign_keys=[member_stu_num],
                                          lazy="raise",
                                          back_populates="org_member")
    role: Mapped[OrganizationRole] = mapped_column(
        Enum(OrganizationRole),
        default=OrganizationRole.member,
        nullable=False
    )
    is_delete: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False
    )
    __table_args__ = (
        UniqueConstraint("org_id", "member_stu_num", name='uq_org_member'),
    )
