// 权限取值与后端 Jurisdiction 枚举保持一致
export const JURISDICTIONS = [
  { value: 'admin', label: '管理员' },
  { value: 'user', label: '普通用户' },
  { value: 'student', label: '学生' },
  { value: 'org', label: '组织' },
]

export function jurisdictionLabel(value) {
  return JURISDICTIONS.find((item) => item.value === value)?.label || '未知'
}
