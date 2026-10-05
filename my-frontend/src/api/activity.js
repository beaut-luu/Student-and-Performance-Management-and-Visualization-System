import request from './request'

// 创建活动前调用，获取当前操作者所属社团（org_id / org_name）
export function getMyOrg() {
  return request.get('/activity/my-org')
}

// 创建活动
export function createActivity(data) {
  return request.post('/activity/create', data)
}

// 活动列表（后端固定每页 20 条）
export function getActivityList(page = 1) {
  return request.get('/activity/list', { params: { page } })
}

// 活动创建者信息主页
export function getCreatorProfile(stuNum) {
  return request.get('/activity/creator', { params: { stu_num: stuNum } })
}

// 活动所属社团信息主页（后端按活动 id 查询）
export function getOrganizationProfile(actId) {
  return request.get('/activity/organization', { params: { act_id: actId } })
}
