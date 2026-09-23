# RegisterIn / LoginIn / TokenOut
# 注册登录用户输入字段校验
from pydantic import BaseModel, Field, EmailStr, BeforeValidator
from typing import Annotated


def empty_str_to_none(val: str):
    if val.strip() == '':
        return None
    return val


EmptyToNone = Annotated[EmailStr | None, BeforeValidator(empty_str_to_none)]


class RegisterIn(BaseModel):
    username: str = Field(..., min_length=1, max_length=64, description='昵称最少一个字符')
    name: str = Field(..., min_length=1, max_length=25, description='请输入真实姓名,仅用于验证身份')
    password: str = Field(..., min_length=6, max_length=128, description='密码最少6位')
    stu_number: int = Field(..., le=1000000000000, me=99999999999,  description='请输入12位学号,仅用于验证身份')
    email: EmptyToNone = Field(default=None, description="请输入正确的邮箱")


class LoginIn(BaseModel):
    username: str = Field(..., min_length=1, max_length=64, description='用户名')
    password: str = Field(..., min_length=6, description='密码')


class TokenOut(BaseModel):
    access_token: str = Field(..., description='JWT令牌')
    token_type: str = Field(default="bearer", description='JWT令牌类型')
