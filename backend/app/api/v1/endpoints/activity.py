from fastapi import Depends, APIRouter, Query
from app.core.exceptions import UserNotLogInError, OrganizationNotFoundError, UserNotFoundError
from app.models.user import User
from app.services import activity
from app.core.deps import d_urepo, d_arepo, get_current_user
from app.repositories.user import UserRepository
from app.repositories.activity import ActivityRepository
from app.schemas.activity import ActivityIn, ActivityCreatedOut, OrgOptionOut, ActivitiesListOut, ActivityOut, ActivityUserProfileOut, ActivityOrgProfileOut
from app.core.response import SuccessResponse
from app.models.enums import ActivityStatus


router = APIRouter(prefix='/activity', tags=['活动创建'])


@router.get('/my-org', response_model=SuccessResponse, summary='获取当前用户的org_id及org_name')
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


@router.get('/list', response_model=SuccessResponse, summary='活动列表')
async def get_activities(page: int = Query(1, ge=1),
                         arepo: ActivityRepository = Depends(d_arepo),
                         user: User = Depends(get_current_user)):
    if user is None:
        raise UserNotLogInError('当前用户未登录')
    res = await activity.get_activities_list(arepo, page)
    items = []
    for act, creator_name, org_name in res['activities']:
        item = {
            'creator_name': creator_name,
            'org_name': org_name,
            **{k: v for k, v in act.__dict__.items() if not k.startswith('_')}
        }
        items.append(ActivityOut.model_validate(item))
    return SuccessResponse(data=ActivitiesListOut(activities=items, count=res['count']))


@router.get('/creator', response_model=SuccessResponse, summary='获取creator信息主页')
async def get_profile_from_stu_num(stu_num: int,
                                   urepo: UserRepository = Depends(d_urepo),
                                   user: User = Depends(get_current_user)):
    if user is None:
        raise UserNotLogInError('当前用户未登录')
    res = await activity.get_creator_profile(urepo, stu_num)
    if res is None:
        raise UserNotFoundError('该用户不存在')
    return SuccessResponse(data=ActivityUserProfileOut.model_validate(res))


@router.get('/organization', response_model=SuccessResponse, summary='获取社团信息主页')
async def get_organization(act_id: int,
                           arepo: ActivityRepository = Depends(d_arepo),
                           user: User = Depends(get_current_user)):
    if user is None:
        raise UserNotLogInError('当前用户未登录')
    res = await activity.get_organization(arepo, act_id)
    if res is None:
        raise OrganizationNotFoundError('该社团不存在')
    return SuccessResponse(data=ActivityOrgProfileOut.model_validate(res))
