# Jurisdiction(权限枚举,迁移自 state.py;JWT 方案下舍弃 State)
from enum import IntEnum


class Jurisdiction(IntEnum):
    ADMIN = 1
    USER = 0
