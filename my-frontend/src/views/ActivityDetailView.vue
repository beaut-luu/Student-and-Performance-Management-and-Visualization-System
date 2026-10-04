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

function fmt(value) {
  if (!value) return '—'
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return String(value)
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

// ActivityOut 的全部字段，按语义分组，全部以纯文本展示
const groups = computed(() => {
  const a = detail.value
  if (!a) return []
  return [
    {
      title: '基本信息',
      rows: [
        ['活动ID', a.id],
        ['活动标题', a.title],
        ['活动分类', a.category],
        ['活动概述', a.summary],
        ['活动详情', a.content],
        ['活动地点', a.location],
      ],
    },
    {
      title: '发布信息',
      rows: [
        ['发布方', a.org_name],
        ['发布方ID', a.org_id],
        ['创建者', a.creator_name],
        ['创建者学号', a.creator_stu_num],
      ],
    },
    {
      title: '时间安排',
      rows: [
        ['活动开始', fmt(a.start_time)],
        ['活动结束', fmt(a.end_time)],
        ['报名开始', fmt(a.register_start)],
        ['报名截止', fmt(a.register_deadline)],
      ],
    },
    {
      title: '报名设置',
      rows: [
        ['报名名额', a.capacity ?? '不限'],
        ['已报名人数', a.register_count],
        ['报名审核', a.need_approval ? '需要审核' : '无需审核'],
        ['签到', a.checkin ? '开启' : '未开启'],
      ],
    },
  ]
})

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

      <section v-else class="sheet">
        <h2 class="act-title">{{ detail.title }}</h2>

        <div v-for="group in groups" :key="group.title" class="group">
          <h3>{{ group.title }}</h3>
          <dl>
            <div v-for="row in group.rows" :key="row[0]" class="row">
              <dt>{{ row[0] }}</dt>
              <dd>{{ row[1] }}</dd>
            </div>
          </dl>
        </div>

        <div class="actions">
          <button class="signup" type="button" @click="onSignup">报名</button>
          <p v-if="signupNotice" class="notice">{{ signupNotice }}</p>
        </div>
      </section>
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

.content { flex: 1; display: flex; justify-content: center; padding: 28px 24px 48px; }
.sheet {
  width: 100%;
  max-width: 760px;
  background: #fff;
  border-radius: 12px;
  padding: 28px 30px 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.07);
  height: fit-content;
}
.act-title { margin: 0 0 20px; font-size: 21px; line-height: 1.4; }

.group + .group { margin-top: 22px; }
.group h3 {
  margin: 0 0 8px;
  font-size: 13px;
  font-weight: 600;
  color: #4a7dff;
  letter-spacing: 0.5px;
}
dl { margin: 0; }
.row { display: flex; gap: 16px; padding: 9px 0; border-bottom: 1px solid #f2f3f7; }
.row:last-child { border-bottom: none; }
dt { width: 88px; flex: none; font-size: 13px; color: #9aa1ae; }
dd { margin: 0; font-size: 14px; color: #2c2c2c; line-height: 1.6; word-break: break-word; white-space: pre-wrap; }

.actions {
  margin-top: 28px;
  padding-top: 24px;
  border-top: 1px solid #f2f3f7;
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
