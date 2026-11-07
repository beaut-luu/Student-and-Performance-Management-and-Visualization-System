from fastapi import APIRouter, Depends
from app.core.response import SuccessResponse
from app.models.user import User
from app.repositories.message_center import MsgCenterRepository
from app.core.deps import m_urepo, get_current_user
from app.services import message_center
from app.schemas.message_center import MsgListOut, MsgIdsIn


router = APIRouter(prefix='/msg-center', tags=['信息中心'])


@router.get('/message', response_model=SuccessResponse, summary='获取未读消息')
async def get_unread_msg(mrepo: MsgCenterRepository = Depends(m_urepo),
                         user: User = Depends(get_current_user)):
    res = await message_center.get_unread_msg(mrepo, user.stu_number)
    return SuccessResponse(data=MsgListOut(msg_list=res))


@router.put('/message/update', response_model=SuccessResponse, summary='更新消息已读状态')
async def update_unread_msg(body: MsgIdsIn,
                            msg_id: list[int],
                            mrepo: MsgCenterRepository = Depends(m_urepo),
                            user: User = Depends(get_current_user)):
    await message_center.update_msg(mrepo, body.msg_id_list, user.stu_number)
    return SuccessResponse
