<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useActivityStore, ACTIVITY_PAGE_SIZE } from '@/stores/activity'

const router = useRouter()
const activity = useActivityStore()

const loading = ref(true)
const error = ref('')

const totalPages = computed(() =>
  Math.max(1, Math.ceil((activity.count || 0) / ACTIVITY_PAGE_SIZE)),
)

// 页码窗口：首页/末页 + 当前页左右各 2 页，中间用省略号
const pageNumbers = computed(() => {
  const total = totalPages.value
  const cur = activity.page
  const result = []
  for (let p = 1; p <= total; p++) {
    if (p === 1 || p === total || Math.abs(p - cur) <= 2) result.push(p)
    else if (result[result.length - 1] !== '...') result.push('...')
  }
  return result
})

async function load(targetPage) {
  error.value = ''
  try {
    await activity.fetchActivityPage(targetPage)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function goPage(targetPage) {
  if (targetPage < 1 || targetPage > totalPages.value || targetPage === activity.page) return
  loading.value = true
  load(targetPage)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function goDetail(id) {
  router.push({ name: 'activityDetail', params: { id } })
}

onMounted(() => {
  // 从详情页返回时保留原来所在的页码
  load(activity.page || 1)
})
</script>

<template>
  <div class="page-wrap">
    <header class="bar">
      <button class="back" type="button" @click="router.push({ name: 'home' })">返回主页</button>
      <h1>活动</h1>
    </header>

    <main class="content">
      <p v-if="loading" class="muted">加载中...</p>
      <p v-else-if="error" class="error">{{ error }}</p>

      <template v-else>
        <p v-if="!activity.list.length" class="muted empty">暂无进行中的活动</p>

        <ul v-else class="act-rows">
          <li v-for="item in activity.list" :key="item.id" class="act-row" @click="goDetail(item.id)">
            <div class="row-text">
              <p class="meta">
                <span class="org">{{ item.org_name }}</span>
                <i>·</i>
                <span class="creator">{{ item.creator_name }}</span>
              </p>
              <h3 class="title">{{ item.title }}</h3>
            </div>
            <span class="chevron">›</span>
          </li>
        </ul>

        <nav v-if="activity.count" class="pager">
          <span class="total">共 {{ activity.count }} 个活动</span>
          <button class="pg" type="button" :disabled="activity.page <= 1" @click="goPage(activity.page - 1)">
            上一页
          </button>
          <template v-for="(p, index) in pageNumbers" :key="`${p}-${index}`">
            <span v-if="p === '...'" class="dots">…</span>
            <button
              v-else
              class="pg num"
              :class="{ on: p === activity.page }"
              type="button"
              @click="goPage(p)"
            >
              {{ p }}
            </button>
          </template>
          <button
            class="pg"
            type="button"
            :disabled="activity.page >= totalPages"
            @click="goPage(activity.page + 1)"
          >
            下一页
          </button>
          <span class="total">第 {{ activity.page }} / {{ totalPages }} 页</span>
        </nav>
      </template>
    </main>
  </div>
</template>

<style scoped>
.page-wrap { min-height: 100vh; display: flex; flex-direction: column; }
.bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 24px;
  background: #fff;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.06);
}
.bar h1 { margin: 0; font-size: 17px; font-weight: 600; }
.back { padding: 6px 12px; font-size: 13px; background: #8a94a6; }

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 28px 24px 40px;
}

/* 长条：长度约 1080px，高度 74px（≈ 1/15） */
.act-rows {
  list-style: none;
  width: 100%;
  max-width: 1080px;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.act-row {
  height: 74px;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 0 22px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: box-shadow 0.18s, transform 0.18s;
}
.act-row:hover { box-shadow: 0 4px 14px rgba(74, 125, 255, 0.16); transform: translateY(-1px); }
.row-text { min-width: 0; display: flex; flex-direction: column; gap: 5px; }
.meta { margin: 0; font-size: 13px; color: #8b93a3; display: flex; align-items: center; gap: 6px; }
.meta i { font-style: normal; color: #ccd0d8; }
.org { color: #4a7dff; }
.title {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  color: #2c2c2c;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.chevron { margin-left: auto; color: #c8ccd4; font-size: 22px; line-height: 1; }

.empty { margin-top: 60px; }

/* 分页 */
.pager {
  width: 100%;
  max-width: 1080px;
  margin-top: 28px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.total { font-size: 13px; color: #8b93a3; }
.pager .total:last-child { margin-left: auto; }
.pg {
  min-width: 36px;
  padding: 6px 12px;
  font-size: 13px;
  background: #fff;
  color: #4b5468;
  border: 1px solid #e3e6ee;
  border-radius: 6px;
}
.pg:hover:not(:disabled) { border-color: #4a7dff; color: #4a7dff; }
.pg:disabled { opacity: 0.45; cursor: not-allowed; }
.pg.num { padding: 6px 10px; }
.pg.on { background: #4a7dff; border-color: #4a7dff; color: #fff; }
.dots { color: #b6bcc8; padding: 0 2px; }

.muted { color: #888; font-size: 14px; }
.error { color: #e34d4d; font-size: 14px; }
</style>
