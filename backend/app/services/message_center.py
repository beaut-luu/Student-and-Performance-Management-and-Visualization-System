from typing import Sequence
from app.repositories.message_center import MsgCenterRepository
from app.repositories.message_center import MsgCenter


async def create_msg(mrepo: MsgCenterRepository, title: str, msg: str, **values) -> MsgCenter:
    return await mrepo.create_msg(title=title, msg=msg, **values)


async def update_msg(mrepo: MsgCenterRepository, msg_id: list[int], stu_num: int) -> None:
    return await mrepo.update_is_read_to_true(msg_id, stu_num)


async def get_unread_msg(mrepo: MsgCenterRepository, stu_num: int) -> Sequence[MsgCenter]:
    return await mrepo.select_unread_msg(stu_num)

