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
  return request.get('/activity/activities-list', { params: { page } })
}
