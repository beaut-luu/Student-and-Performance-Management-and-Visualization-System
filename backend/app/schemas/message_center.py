from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class MsgOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(..., max_length=31, description='消息标题')
    msg: str = Field(..., max_length=201, description='消息本体')
    create_time: datetime = Field(..., description='消息发送时间')


class MsgListOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    msg_list: list[MsgOut] = Field(..., description='未读消息列表')


class MsgIdsIn(BaseModel):
    msg_id_list: list[int] = Field(..., description='更新已读状态的消息id列表')
