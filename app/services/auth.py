# register() / login()→签发JWT / 用户名查重
# 只做用户认证(登录态)，不处理用户数据
from app.repositories.user import UserRepository
from app.core.exceptions import UsernameDuplicatedError, InvalidCredentialsError
from app.core.security import trans_hash, verify_hash, create_access_token


async def register(username: str, password: str, urepo: UserRepository) -> bool:
    if await duplicate_checking(username, urepo):
        raise UsernameDuplicatedError('用户名重复')
    pwd_hash = trans_hash(password)
    if await urepo.insert_user(username, pwd_hash):
        return True
    return False


async def login(username: str, password: str, urepo: UserRepository) -> str:
    user = await urepo.select_one_by_username(username)
    if user is None or not verify_hash(password, user.pwd_hash):
        raise InvalidCredentialsError('用户名不存在或密码错误')
    token = create_access_token(user.username, user.jurisdiction)
    return token


async def duplicate_checking(username: str, urepo: UserRepository) -> bool:
    res = await urepo.select_one_by_username(username)
    if res is not None:
        return True
    return False
