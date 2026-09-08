# RegisterIn / LoginIn / TokenOut
# 注册登录用户输入字段校验
from pydantic import BaseModel, Field


class RegisterIn(BaseModel):
    username: str = Field(..., min_length=1, max_length=64, description='用户名最少一个字符')
    password: str = Field(..., min_length=6, max_length=128, description='密码最少6位')


class LoginIn(BaseModel):
    username: str = Field(..., min_length=1, max_length=64, description='用户名')
    password: str = Field(..., min_length=1, description='密码')


class TokenOut(BaseModel):
    access_token: str = Field(..., description='JWT令牌')
    token_type: str = Field(default="bearer", description='JWT令牌类型')
