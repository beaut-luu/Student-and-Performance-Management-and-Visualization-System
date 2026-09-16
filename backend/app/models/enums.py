# Jurisdiction(权限枚举,迁移自 state.py;JWT 方案下舍弃 State)
from enum import IntEnum, Enum


class Jurisdiction(IntEnum):
    ADMIN = 0
    user = 1
    student = 2
    ORG = 3


class OrganizationRole(IntEnum):
    owner = 0
    manager = 1
    member = 2


class GroupRole(IntEnum):
    owner = 0
    admin = 1
    member = 2


class ActivityStatus(Enum):
    draft: 'draft'  # 草稿
    published: 'published'  # 公示期
    cancelled: 'cancelled'  # 已取消
    finished: 'finished'  # 已完成


class ActivityRegistrationStatus(Enum):
    approved: 'approved'  # 被录用
    cancelled: 'cancelled'  # 已取消
    rejected: 'rejected'  # 被驳回
    check_in: 'check_in'  # 审核阶段
