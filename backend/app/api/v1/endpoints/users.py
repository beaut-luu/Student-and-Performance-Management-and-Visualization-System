# /users/me 及改密改名改权限接口
# Depends(get_current_user)
from fastapi import APIRouter, Depends
from app.core.response import SuccessResponse
from app.models.user import User
from app.repositories.user import UserRepository
from app.core.deps import get_current_user, d_urepo
from app.schemas import user as sch_user
from app.services import user as ser_user
from app.core.exceptions import BizException


router = APIRouter(prefix='/users', tags=['用户'])


@router.get('/me', response_model=SuccessResponse, summary='获取当前用户状态')
async def get_me(me: User = Depends(get_current_user)):
    """model_validate是BaseModel自带的方法,将输入的内容(一般为字典,我开了from_attributes=True,
    所以可以传入orm对象)转化为你的输出模型(UserOut)"""
    return SuccessResponse(data=sch_user.UserOut.model_validate(me))


@router.put('/me/username', response_model=SuccessResponse, summary='修改用户名')
async def change_username(body: sch_user.ChangeNameIn,
                          urepo: UserRepository = Depends(d_urepo),
                          user: User = Depends(get_current_user)):
    if await ser_user.change_username(body.new_name, urepo, user):
        return SuccessResponse(message='用户名修改成功')
    raise BizException('用户名修改失败')


@router.put('/me/password', response_model=SuccessResponse, summary='修改密码')
async def change_pwd(body: sch_user.ChangePwdIn,
                     urepo: UserRepository = Depends(d_urepo),
                     user: User = Depends(get_current_user)):
    if await ser_user.change_pwd(body.old_pwd, body.new_pwd, user, urepo):
        return SuccessResponse(message='密码修改成功')
    raise BizException('密码修改失败')


@router.put('/me/jurisdiction', response_model=SuccessResponse, summary='修改权限')
async def change_jur(body: sch_user.ChangeJurIn,
                     urepo: UserRepository = Depends(d_urepo),
                     user: User = Depends(get_current_user)):
    if await ser_user.change_jurisdiction(body.jur, body.target_username, user, urepo):
        return SuccessResponse(message='权限修改成功')
    raise BizException('权限修改失败')
