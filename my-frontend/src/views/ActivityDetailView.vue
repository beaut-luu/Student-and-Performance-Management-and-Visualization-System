<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useActivityStore } from '@/stores/activity'

const route = useRoute()
const router = useRouter()
const activity = useActivityStore()

const loading = ref(true)
const error = ref('')
const signupNotice = ref('')

const actId = computed(() => Number(route.params.id))
const detail = computed(() => activity.byId[actId.value] || null)

const pad = (n) => String(n).padStart(2, '0')

function fmt(value) {
  if (!value) return '—'
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return String(value)
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

// 同一段活动时间压缩展示：2026-11-23 09:00 ~ 13:00
const timeRange = computed(() => {
  const a = detail.value
  if (!a) return ''
  const s = new Date(a.start_time)
  const e = new Date(a.end_time)
  if (Number.isNaN(s.getTime()) || Number.isNaN(e.getTime())) return fmt(a.start_time)
  if (s.toDateString() === e.toDateString()) {
    return `${fmt(a.start_time)} ~ ${pad(e.getHours())}:${pad(e.getMinutes())}`
  }
  return `${fmt(a.start_time)} ~ ${fmt(a.end_time)}`
})

// 报名状态（由时间推导，仅作展示）
const signup = computed(() => {
  const a = detail.value
  if (!a) return null
  const now = Date.now()
  if (a.register_start && now < new Date(a.register_start).getTime()) {
    return { text: '报名未开始', tone: 'wait' }
  }
  if (a.register_deadline && now > new Date(a.register_deadline).getTime()) {
    return { text: '报名已截止', tone: 'over' }
  }
  return { text: '报名进行中', tone: 'on' }
})

// ActivityOut 的全部字段，按语义分组，全部以纯文本展示
const groups = computed(() => {
  const a = detail.value
  if (!a) return []
  return [
    {
      title: '基本信息',
      rows: [
        { label: '活动ID', value: a.id },
        { label: '活动分类', value: a.category },
        { label: '活动地点', value: a.location },
        { label: '活动概述', value: a.summary, wide: true },
        { label: '活动详情', value: a.content, wide: true },
      ],
    },
    {
      title: '发布信息',
      rows: [
        {
          label: '发布方',
          value: a.org_name,
          to: { name: 'organizationProfile', params: { actId: a.id } },
          tip: '查看社团主页',
        },
        { label: '发布方ID', value: a.org_id },
        {
          label: '创建者',
          value: a.creator_name,
          to: { name: 'userProfile', params: { stuNum: a.creator_stu_num } },
          tip: '查看创建者主页',
        },
        { label: '创建者学号', value: a.creator_stu_num },
      ],
    },
    {
      title: '时间安排',
      rows: [
        { label: '活动开始', value: fmt(a.start_time) },
        { label: '活动结束', value: fmt(a.end_time) },
        { label: '报名开始', value: fmt(a.register_start) },
        { label: '报名截止', value: fmt(a.register_deadline) },
      ],
    },
    {
      title: '报名设置',
      rows: [
        { label: '报名名额', value: a.capacity ?? '不限' },
        { label: '已报名人数', value: a.register_count },
        { label: '报名审核', value: a.need_approval ? '需要审核' : '无需审核' },
        { label: '签到', value: a.checkin ? '开启' : '未开启' },
      ],
    },
  ]
})

function go(to) {
  if (to) router.push(to)
}

function goOrg() {
  go({ name: 'organizationProfile', params: { actId: actId.value } })
}

function goCreator() {
  if (detail.value) go({ name: 'userProfile', params: { stuNum: detail.value.creator_stu_num } })
}

function onSignup() {
  signupNotice.value = '报名功能正在开发中，暂未开放'
}

onMounted(async () => {
  try {
    await activity.loadActivityById(actId.value)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="page-wrap">
    <header class="bar">
      <button class="back" type="button" @click="router.push({ name: 'activityList' })">返回列表</button>
      <h1>活动详情</h1>
    </header>

    <main class="content">
      <p v-if="loading" class="muted">加载中...</p>
      <p v-else-if="error" class="error">{{ error }}</p>
      <p v-else-if="!detail" class="muted">未找到该活动</p>

      <div v-else class="sheet">
        <section class="hero">
          <div class="chips">
            <span class="chip cat">{{ detail.category }}</span>
            <span v-if="signup" class="chip" :class="signup.tone">{{ signup.text }}</span>
          </div>
          <h2 class="act-title">{{ detail.title }}</h2>
          <p class="hero-meta">
            由
            <span class="link" title="查看社团主页" @click="goOrg">{{ detail.org_name }}</span>
            主办 ·
            <span class="link" title="查看创建者主页" @click="goCreator">{{ detail.creator_name }}</span>
            发布
            <i class="sep">|</i>
            {{ timeRange }}
          </p>
        </section>

        <section v-for="group in groups" :key="group.title" class="card">
          <h3 class="card-title">{{ group.title }}</h3>
          <div class="rows">
            <div
              v-for="row in group.rows"
              :key="row.label"
              class="row"
              :class="{ wide: row.wide }"
            >
              <span class="label">{{ row.label }}</span>
              <span
                v-if="row.to"
                class="value link"
                :title="row.tip"
                @click="go(row.to)"
              >{{ row.value }}<i class="go">›</i></span>
              <span v-else class="value">{{ row.value }}</span>
            </div>
          </div>
        </section>

        <div class="actions">
          <button class="signup" type="button" @click="onSignup">报名</button>
          <p v-if="signupNotice" class="notice">{{ signupNotice }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.page-wrap {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(180deg, #f4f6fb 0%, #f7f8fb 240px);
}
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

.content { flex: 1; display: flex; justify-content: center; padding: 26px 24px 48px; }
.sheet { width: 100%; max-width: 760px; height: fit-content; }

/* 头部：分类/报名状态 + 标题 + 主办方 */
.hero {
  padding: 24px 28px 22px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 14px rgba(28, 44, 88, 0.07);
}
.chips { display: flex; gap: 8px; margin-bottom: 12px; }
.chip {
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  line-height: 18px;
}
.chip.cat { background: #eef3ff; color: #4a7dff; }
.chip.on { background: #e8f7ef; color: #22a06b; }
.chip.wait { background: #fff5e6; color: #d98a00; }
.chip.over { background: #f2f3f7; color: #8b93a3; }

.act-title { margin: 0 0 10px; font-size: 22px; line-height: 1.35; letter-spacing: 0.3px; }
.hero-meta { margin: 0; font-size: 13px; color: #7b8496; line-height: 1.7; }
.hero-meta .sep { font-style: normal; color: #d9dde6; margin: 0 6px; }

/* 信息卡片 */
.card {
  margin-top: 16px;
  padding: 18px 28px 20px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 14px rgba(28, 44, 88, 0.06);
}
.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 12px;
  font-size: 14px;
  font-weight: 600;
  color: #2c2c2c;
}
.card-title::before {
  content: '';
  width: 3px;
  height: 14px;
  border-radius: 2px;
  background: #4a7dff;
}
.rows { display: grid; grid-template-columns: 1fr 1fr; gap: 2px 28px; }
.row { display: flex; gap: 12px; padding: 8px 0; border-bottom: 1px solid #f4f5f9; }
.row.wide { grid-column: 1 / -1; flex-direction: column; gap: 6px; }
.label { width: 76px; flex: none; font-size: 13px; color: #9aa1ae; }
.row.wide .label { width: auto; }
.value { font-size: 14px; color: #2c2c2c; line-height: 1.7; word-break: break-word; }
.row.wide .value {
  display: block;
  padding: 10px 14px;
  background: #fafbfe;
  border-radius: 8px;
  white-space: pre-wrap;
}

/* 可点击文本：蓝色 + 虚线下划线 + 悬停提示，区别于普通文本 */
.link {
  color: #4a7dff;
  cursor: pointer;
  border-bottom: 1px dashed #9dbbff;
  transition: color 0.15s, border-color 0.15s;
}
.link:hover { color: #2f63e6; border-bottom-color: #2f63e6; border-bottom-style: solid; }
.link .go { margin-left: 2px; font-style: normal; opacity: 0.75; }

.actions {
  margin-top: 22px;
  padding: 22px 28px 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
/* 橙色方形报名按钮（方角，中等大小） */
.signup {
  width: 168px;
  height: 52px;
  padding: 0;
  border-radius: 4px;
  background: #f08c1a;
  color: #fff;
  font-size: 17px;
  font-weight: 600;
  letter-spacing: 2px;
}
.signup:hover { background: #e07f10; }
.notice { margin: 0; font-size: 13px; color: #9aa1ae; }

.muted { color: #888; font-size: 14px; }
.error { color: #e34d4d; font-size: 14px; }
</style>
