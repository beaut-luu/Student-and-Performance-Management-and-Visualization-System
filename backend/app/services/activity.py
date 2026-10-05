from app.models.activity import Activity
from app.repositories.activity import ActivityRepository
from app.models.user import User
from app.models.organization import Organization
from app.repositories.organization import OrganizationRepository
from app.repositories.user import UserRepository
from app.core.exceptions import PermissionDeniedError, UserNotFoundError
from app.models.enums import OrganizationRole, ActivityStatus


#  这个函数对应活动的发布按钮
async def create_activity(user: User, arepo: ActivityRepository, urepo: UserRepository, org_id: int, **value) -> Activity:
    org_and_role = await urepo.select_my_org_and_role(user.stu_number)
    for i in org_and_role:
        if i[0].id == org_id:
            status = ActivityStatus.published if i[1] in (OrganizationRole.manager, OrganizationRole.owner) else ActivityStatus.pending_review
            return await arepo.create_activity(status=status,
                                               creator_stu_num=user.stu_number,
                                               org_id=org_id,
                                               **value)
    else:
        raise PermissionDeniedError('未查询到相关权限,暂时无法发布活动')


# 用户点击 发布活动 按钮进行权限判断同时返回下拉框数据源
async def get_user_org(user: User, urepo: UserRepository) -> list[tuple[str, str, int]]:
    org_and_role = await urepo.select_my_org_and_role(user.stu_number)
    if not org_and_role:
        raise PermissionDeniedError('非社团成员无权发布活动')
    org_list = []
    for i in org_and_role:
        org_list.append((i[0].name, i[0].id, i[1]))
    return org_list


async def get_activities_list(arepo: ActivityRepository, page: int) -> dict:
    activities = await arepo.get_activities(page)
    count = await arepo.get_activities_count()
    return {'activities': activities, 'count': count}


async def get_creator_profile(urepo: UserRepository, stu_num: int) -> User | None:
    return await urepo.select_my_info(stu_num)


async def get_organization(arepo: ActivityRepository, act_id: int) -> Organization:
    return await arepo.get_organization(act_id)
