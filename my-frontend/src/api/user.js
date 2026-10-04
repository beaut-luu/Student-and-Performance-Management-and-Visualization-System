import request from './request'

export function getMe() {
  return request.get('/users/me')
}

// 我的信息（含所属社团与角色）
export function getMyInfo() {
  return request.get('/users/me/my-info')
}

export function changeUsername(newName) {
  return request.put('/users/me/username', { new_name: newName })
}

export function changePassword(oldPwd, newPwd) {
  return request.put('/users/me/password', { old_pwd: oldPwd, new_pwd: newPwd })
}

export function changeJurisdiction(payload) {
  return request.put('/users/me/jurisdiction', payload)
}
