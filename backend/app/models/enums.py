# Jurisdiction(权限枚举,迁移自 state.py;JWT 方案下舍弃 State)
from enum import IntEnum


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
