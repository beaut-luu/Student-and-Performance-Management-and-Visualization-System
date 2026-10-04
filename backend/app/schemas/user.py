from pydantic import BaseModel, Field, ConfigDict


class UserOut(BaseModel):
    """model_config是父类BaseModel的一个参数,默认from_attributes=False,表示只能从字典
    里面读取信息,改为True以后允许从任意对象的属性读取值,并将传入对象的属性赋值给此对象的属性
    自动把 SQLAlchemy ORM 实例 → 序列化为 UserOut 的结构"""
    model_config = ConfigDict(from_attributes=True)

    username: str
    jurisdiction: str = Field(..., description='权限')


class OrgMember(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    org_name: str
    role: str


class UserInfoOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    username: str
    name: str
    jurisdiction: str
    stu_number: int
    email: str | None
    org_member: list[OrgMember] | None


class ChangePwdIn(BaseModel):
    old_pwd: str = Field(..., min_length=6, max_length=128, description='原密码')
    new_pwd: str = Field(..., min_length=6, max_length=128, description='新密码')


class ChangeNameIn(BaseModel):
    new_name: str = Field(..., min_length=1, max_length=64, description='新用户名')


class ChangeJurIn(BaseModel):
    target_username: str = Field(..., min_length=1, max_length=64, description='你想为谁修改权限')
    jur: str = Field(..., description='权限')
