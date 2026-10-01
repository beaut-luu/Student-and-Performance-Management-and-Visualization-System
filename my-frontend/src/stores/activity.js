import { ref } from 'vue'
import { defineStore } from 'pinia'
import { getMyOrg } from '@/api/activity'

// 后端约定返回社团列表 [{ org_id, name }]（可能被包在 data 中），这里统一成 { org_id, name, role }
function normalizeOrgOptions(res) {
  const raw = Array.isArray(res?.data) ? res.data : res
  if (!Array.isArray(raw)) return []
  return raw
    .map((item) => ({
      org_id: item?.org_id ?? item?.id,
      name: item?.name ?? item?.org_name,
      role: item?.role,
    }))
    .filter((item) => item.org_id != null && item.name)
}

export const useActivityStore = defineStore('activity', () => {
  // 点击“创建活动”时拉取到的社团下拉数据源：展示 name，提交 org_id
  const orgOptions = ref([])
  // 本次会话中刚创建的活动，用于“待审核活动 / 活动详情”展示
  const lastCreated = ref(null)

  async function fetchOrgOptions() {
    const options = normalizeOrgOptions(await getMyOrg())
    orgOptions.value = options
    return options
  }

  return { orgOptions, lastCreated, fetchOrgOptions }
})
