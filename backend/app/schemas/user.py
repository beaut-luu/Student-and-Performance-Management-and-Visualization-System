# UserOut / ChangePwdIn / ChangeNameIn / ChangeJurIn
# 改密码改用户名改权限用户输入字段校验,例如old_password,new_password分别校验
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class UserOut(BaseModel):
    """model_config是父类BaseModel的一个参数,默认from_attributes=False,表示只能从字典
    里面读取信息,改为True以后允许从任意对象的属性读取值,并将传入对象的属性赋值给此对象的属性
    自动把 SQLAlchemy ORM 实例 → 序列化为 UserOut 的结构"""
    model_config = ConfigDict(from_attributes=True)

    username: str
    jurisdiction: int = Field(description="1=管理员,0=用户")


class ChangePwdIn(BaseModel):
    old_pwd: str = Field(..., min_length=6, max_length=128, description='原密码')
    new_pwd: str = Field(..., min_length=6, max_length=128, description='新密码')


class ChangeNameIn(BaseModel):
    new_name: str = Field(..., min_length=1, max_length=64, description='新用户名')


class ChangeJurIn(BaseModel):
    target_username: str = Field(..., min_length=1, max_length=64, description='你想为谁修改权限')
    jur: int = Field(..., ge=0, le=1, description='权限码只能为0或1')
    # TODO 去除admin密钥
    admin_secret: Optional[str] = Field(default=None, description='非管理员操作时填写')
