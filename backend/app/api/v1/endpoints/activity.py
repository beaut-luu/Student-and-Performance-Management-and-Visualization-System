from fastapi import Depends, APIRouter
from app.models.user import User
from app.services import activity
from app.core.deps import d_urepo, d_arepo, get_current_user
from app.repositories.user import UserRepository
from app.repositories.activity import ActivityRepository
from app.schemas.activity import ActivityIn, ActivityCreatedOut, OrgOptionOut
from app.core.response import SuccessResponse
from app.models.enums import ActivityStatus


router = APIRouter(prefix='/activity', tags=['活动创建'])


@router.get('/my-org', response_model=SuccessResponse, summary='获取当前用户的org_id及org_name,role')
async def get_org(user: User = Depends(get_current_user),
                  urepo: UserRepository = Depends(d_urepo)):
    org_list = await activity.get_user_org(user, urepo)
    return SuccessResponse(data=[OrgOptionOut(org_id=o[1], name=o[0]) for o in org_list])


@router.post('/create', response_model=SuccessResponse, summary='创建活动')
async def create_activity(body: ActivityIn, urepo: UserRepository = Depends(d_urepo),
                          arepo: ActivityRepository = Depends(d_arepo),
                          user: User = Depends(get_current_user)):
    res = await activity.create_activity(user, arepo, urepo, org_id=body.org_id,
                                         **body.model_dump(exclude={'org_id'}))
    return SuccessResponse(message='活动发布成功' if res.status == ActivityStatus.published else '已提交,等待审核',
                           data=ActivityCreatedOut.model_validate(res))
