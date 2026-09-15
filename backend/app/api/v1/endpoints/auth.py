"""路由层只做一件事——从依赖注入拿 operator，从 body 拿参数，转发给 service，再包装响应。
路由里不出现 if/else 权限判断、不出现字符串比对。"""
# /auth/register  /auth/login
# 写接口，收参数调用service层函数，回响应
from fastapi import APIRouter, Depends
from app.core.response import SuccessResponse
from app.schemas.auth import RegisterIn, TokenOut, LoginIn
from app.services import auth
from app.core.exceptions import BizException
from app.repositories.user import UserRepository
from app.core.deps import d_urepo


router = APIRouter(prefix='/auth', tags=['认证'])


@router.post('/register', response_model=SuccessResponse, summary='注册')
async def register(body: RegisterIn,
                   urepo: UserRepository = Depends(d_urepo)):
    if not await auth.register(body.username, body.password,
                               body.email, body.stu_number, body.name, urepo):
        raise BizException('注册失败')
    return SuccessResponse(message='注册成功')


@router.post('/login', response_model=SuccessResponse, summary='登录')
async def login(body: LoginIn,
                urepo: UserRepository = Depends(d_urepo)):
    token = await auth.login(body.username, body.password, urepo)
    return SuccessResponse(message='登录成功', data=TokenOut(access_token=token))
