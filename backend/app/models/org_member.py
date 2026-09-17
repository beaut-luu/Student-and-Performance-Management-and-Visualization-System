from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UniqueConstraint, Enum
from app.models.base import Base
from app.models.enums import OrganizationRole


class OrgMember(Base):
    __tablename__ = "organization_member"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    org_id: Mapped[int] = mapped_column(
        nullable=False
    )
    member_stu_num: Mapped[str] = mapped_column(
        String(12),
        nullable=False,
        index=True
    )
    role: Mapped[OrganizationRole] = mapped_column(
        Enum(OrganizationRole),
        default=OrganizationRole.member
    )
    __table_args__ = (
        UniqueConstraint("org_id", "member_stu_num", name='uq_org_member'),
    )
