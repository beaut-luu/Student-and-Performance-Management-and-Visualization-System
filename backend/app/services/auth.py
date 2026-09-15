# register() / login()→签发JWT / 用户名查重
# 只做用户认证(登录态)，不处理用户数据
from app.repositories.user import UserRepository
from app.core.exceptions import UsernameDuplicatedError, InvalidCredentialsError
from app.core.security import trans_hash, verify_hash, create_access_token


async def register(username: str, password: str,
                   email: str | None, stu_number: str,
                   name: str,
                   urepo: UserRepository) -> bool:
    if await duplicate_checking_username(username, urepo):
        raise UsernameDuplicatedError('该用户名已被使用')
    elif await duplicate_checking_email(email, urepo):
        raise UsernameDuplicatedError('该邮箱已被使用')
    elif await duplicate_checking_stu_num(stu_number, urepo):
        raise UsernameDuplicatedError('该学号已注册')
    pwd_hash = trans_hash(password)
    if await urepo.insert_user(username, pwd_hash, email, stu_number, name):
        return True
    return False


async def login(username: str, password: str, urepo: UserRepository) -> str:
    user = await urepo.select_one_by_username(username)
    if user is None or not verify_hash(password, user.pwd_hash):
        raise InvalidCredentialsError('用户名不存在或密码错误')
    token = create_access_token(user.username, user.jurisdiction)
    return token


async def duplicate_checking_username(username: str, urepo: UserRepository) -> bool:
    res = await urepo.select_one_by_username(username)
    if res is not None:
        return True
    return False


async def duplicate_checking_email(email: str | None, urepo: UserRepository) -> bool:
    if email is None:
        pass
    res = await urepo.select_one_by_email(email)
    if res is not None:
        return True
    return False


async def duplicate_checking_stu_num(stu_num: str, urepo: UserRepository) -> bool:
    res = await urepo.select_one_by_stu_num(stu_num)
    if res is not None:
        return True
    return False
