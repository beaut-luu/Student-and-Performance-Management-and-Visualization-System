# 验旧密改密 / 改名 / 改权限(含 ADMIN_SECRET 校验)
from app.core.exceptions import OldPasswordError, SameOldNewPasswordError, UsernameDuplicatedError, \
    PermissionDeniedError, UserNotFoundError
from app.core.security import verify_hash, trans_hash
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.auth import duplicate_checking_username
from typing import Optional
from app.core.config import settings
from app.models.enums import Jurisdiction


async def change_pwd(old_pwd: str,
                     new_pwd: str,
                     user: User,
                     urepo: UserRepository) -> bool:
    if not verify_hash(old_pwd, user.pwd_hash):
        raise OldPasswordError('原密码错误')

    if old_pwd == new_pwd:
        raise SameOldNewPasswordError

    return await urepo.update_pwdhash(user.username, trans_hash(new_pwd))


async def change_username(new_name: str,
                          urepo: UserRepository,
                          user: User) -> bool:
    if await duplicate_checking_username(new_name, urepo):
        raise UsernameDuplicatedError('该用户名已存在')

    return await urepo.update_username(user.username, new_name)


async def change_jurisdiction(new_jur: str,
                              target_username: str,
                              user: User,
                              urepo: UserRepository) -> bool:
    if user.jurisdiction != Jurisdiction.admin:
        raise PermissionDeniedError('权限不足')
    if not await duplicate_checking_username(target_username, urepo):
        raise UserNotFoundError('该用户不存在')
    return await urepo.update_jurisdiction(target_username, new_jur)
