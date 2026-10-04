import { ref } from 'vue'
import { defineStore } from 'pinia'
import { getMyOrg, getActivityList } from '@/api/activity'

// 后端列表接口固定每页 20 条
export const ACTIVITY_PAGE_SIZE = 20

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
  // 本次会话中刚创建的活动，用于“我的活动”展示
  const lastCreated = ref(null)

  // 活动列表：byId 作为活动主页面的数据来源（后端暂无单条详情接口）
  const list = ref([])
  const count = ref(0)
  const page = ref(1)
  const byId = ref({})

  async function fetchOrgOptions() {
    const options = normalizeOrgOptions(await getMyOrg())
    orgOptions.value = options
    return options
  }

  function extract(res) {
    const data = res?.data || {}
    return { items: data.activities || [], total: data.count || 0 }
  }

  async function fetchActivityPage(targetPage = 1) {
    const { items, total } = extract(await getActivityList(targetPage))
    items.forEach((item) => {
      byId.value[item.id] = item
    })
    list.value = items
    count.value = total
    page.value = targetPage
    return { items, total }
  }

  // 活动主页面兜底：列表里没有该活动时（例如直接刷新详情页），逐页向后找
  async function loadActivityById(id) {
    if (byId.value[id]) return byId.value[id]
    const first = extract(await getActivityList(1))
    first.items.forEach((item) => {
      byId.value[item.id] = item
    })
    const totalPages = Math.ceil(first.total / ACTIVITY_PAGE_SIZE)
    for (let p = 2; p <= totalPages && !byId.value[id]; p++) {
      const next = extract(await getActivityList(p))
      next.items.forEach((item) => {
        byId.value[item.id] = item
      })
    }
    return byId.value[id] || null
  }

  return {
    orgOptions,
    lastCreated,
    list,
    count,
    page,
    byId,
    fetchOrgOptions,
    fetchActivityPage,
    loadActivityById,
  }
})
