// 社团角色 → 页面展示的称谓（与后端 OrganizationRole 枚举对应）
export const ORG_ROLE_LABEL = {
  owner: '会长',
  manager: '部长',
  member: '成员',
}

// org_name=学生会 + role=owner → “担任学生会会长”
export function formatOrgRole(orgName, role) {
  return `担任${orgName}${ORG_ROLE_LABEL[role] || role}`
}
