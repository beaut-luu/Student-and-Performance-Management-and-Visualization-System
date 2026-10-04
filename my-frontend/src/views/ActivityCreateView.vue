<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useActivityStore } from '@/stores/activity'
import { createActivity } from '@/api/activity'

const router = useRouter()
const activity = useActivityStore()

const FIELD_TYPES = [
  { value: 'text', label: '文本' },
  { value: 'number', label: '数字' },
  { value: 'date', label: '日期' },
  { value: 'textarea', label: '多行文本' },
]

const loading = ref(true)
const submitting = ref(false)
const loadError = ref('')
const error = ref('')
const notice = ref('')

const form = ref({
  org_id: '',
  title: '',
  summary: '',
  content: '',
  category: '',
  location: '',
  register_start: '',
  start_time: '',
  end_time: '',
  register_deadline: '',
  capacity: '',
  need_approval: true,
  checkin: false,
})

// 报名表自定义字段：界面上一行一个“字段名 + 类型”，提交时转成 { 字段名: 类型 }
const fieldRows = ref([])

onMounted(async () => {
  try {
    // 正常情况下主页已拉取过，这里兜底处理直接访问 / 刷新页面的情况
    if (!activity.orgOptions.length) await activity.fetchOrgOptions()
    if (activity.orgOptions.length) form.value.org_id = activity.orgOptions[0].org_id
  } catch (e) {
    loadError.value = e.status === 403 ? '非社团成员无法创建活动' : e.message
  } finally {
    loading.value = false
  }
})

function addFieldRow() {
  fieldRows.value.push({ label: '', type: 'text' })
}

function removeFieldRow(index) {
  fieldRows.value.splice(index, 1)
}

function validate() {
  const f = form.value
  if (!f.org_id) return '请选择活动承包组织'
  if (!f.title) return '请输入活动标题'
  if (f.title.length > 50) return '活动标题不能超过50个字'
  if (!f.summary) return '请输入活动概述'
  if (f.summary.length > 50) return '活动概述不能超过50个字'
  if (!f.content) return '请输入活动内容详情'
  if (f.content.length > 400) return '活动内容详情不能超过400个字'
  if (!f.category) return '请输入活动分类'
  if (f.category.length > 10) return '活动分类不能超过10个字'
  if (!f.location) return '请输入活动地点'
  if (f.location.length > 50) return '活动地点不能超过50个字'
  if (!f.register_start || !f.start_time || !f.end_time || !f.register_deadline) {
    return '请完整填写报名与活动时间'
  }
  // 与后端 ActivityIn.checkin_time 校验顺序保持一致
  if (new Date(f.register_start) <= new Date()) return '活动报名开始时间不能是过去的时间'
  if (new Date(f.start_time) <= new Date(f.register_start)) {
    return '活动开始时间必须晚于活动报名开始时间'
  }
  if (new Date(f.end_time) <= new Date(f.start_time)) {
    return '活动结束时间必须晚于活动开始时间'
  }
  // 与后端 ActivityIn.checkin_time 校验保持一致：报名截止时间必须早于活动结束时间
  if (new Date(f.register_deadline) >= new Date(f.end_time)) {
    return '活动报名截止时间不能晚于活动结束时间'
  }
  if (f.capacity !== '' && (!Number.isInteger(Number(f.capacity)) || Number(f.capacity) <= 0)) {
    return '报名名额需为正整数，或留空表示不限'
  }
  return ''
}

async function onSubmit() {
  error.value = ''
  notice.value = ''
  const invalid = validate()
  if (invalid) {
    error.value = invalid
    return
  }
  const f = form.value
  const payload = {
    org_id: Number(f.org_id),
    title: f.title,
    summary: f.summary,
    content: f.content,
    category: f.category,
    location: f.location,
    register_start: f.register_start,
    start_time: f.start_time,
    end_time: f.end_time,
    register_deadline: f.register_deadline,
    capacity: f.capacity === '' ? null : Number(f.capacity),
    need_approval: f.need_approval,
    fields: Object.fromEntries(
      fieldRows.value.filter((row) => row.label.trim()).map((row) => [row.label.trim(), row.type]),
    ),
    checkin: f.checkin,
  }

  submitting.value = true
  try {
    const res = await createActivity(payload)
    const created = res?.data || {}
    activity.lastCreated = {
      id: created.id,
      status: created.status,
      title: payload.title,
      summary: payload.summary,
      location: payload.location,
      start_time: payload.start_time,
      end_time: payload.end_time,
    }
    if (created.status === 'pending_review') {
      // 我的 -> 我的活动 -> 我组织的活动 -> 待审核活动
      router.push({
        name: 'profile',
        query: { tab: 'activities', sub: 'organized', status: 'pending_review' },
      })
    } else if (created.status === 'published') {
      router.push({ name: 'activityDetail', params: { id: created.id } })
    } else {
      notice.value = res?.message || '活动已创建'
    }
  } catch (e) {
    error.value = e.message
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="page-wrap">
    <header class="bar">
      <button class="back" type="button" @click="router.push({ name: 'home' })">返回主页</button>
      <h1>创建活动</h1>
    </header>

    <main class="content">
      <p v-if="loading" class="muted">加载中...</p>

      <div v-else-if="loadError" class="panel">
        <p class="error">{{ loadError }}</p>
        <button class="back2" type="button" @click="router.push({ name: 'home' })">返回主页</button>
      </div>

      <form v-else class="form" @submit.prevent="onSubmit">
        <h2>基本信息</h2>
        <label>
          活动承包组织
          <select v-model="form.org_id">
            <option v-for="item in activity.orgOptions" :key="item.org_id" :value="item.org_id">
              {{ item.name }}
            </option>
          </select>
        </label>
        <div class="row">
          <label>
            活动标题（≤50字）
            <input v-model.trim="form.title" type="text" placeholder="请输入活动标题" />
          </label>
          <label>
            活动分类（≤10字）
            <input v-model.trim="form.category" type="text" placeholder="如：文体、学术" />
          </label>
        </div>
        <label>
          活动概述（≤50字）
          <input v-model.trim="form.summary" type="text" placeholder="一句话介绍活动" />
        </label>
        <label>
          活动地点（≤50字）
          <input v-model.trim="form.location" type="text" placeholder="请输入活动地点" />
        </label>
        <label>
          活动内容详情（≤400字）
          <textarea v-model.trim="form.content" rows="5" placeholder="请描述活动详情"></textarea>
        </label>

        <h2>时间安排</h2>
        <p class="hint">时间要求：报名开始 &lt; 活动开始 &lt; 活动结束，且报名截止时间须早于活动结束时间</p>
        <div class="row">
          <label>
            报名开始时间
            <input v-model="form.register_start" type="datetime-local" />
          </label>
          <label>
            报名截止时间
            <input v-model="form.register_deadline" type="datetime-local" />
          </label>
        </div>
        <div class="row">
          <label>
            活动开始时间
            <input v-model="form.start_time" type="datetime-local" />
          </label>
          <label>
            活动结束时间
            <input v-model="form.end_time" type="datetime-local" />
          </label>
        </div>

        <h2>报名设置</h2>
        <label>
          报名名额（留空表示不限）
          <input v-model="form.capacity" type="number" min="1" placeholder="如：50" />
        </label>
        <div class="checks">
          <label class="check">
            <input v-model="form.need_approval" type="checkbox" />
            报名需要审核
          </label>
          <label class="check">
            <input v-model="form.checkin" type="checkbox" />
            开启签到
          </label>
        </div>

        <h2>报名表字段</h2>
        <div v-for="(row, index) in fieldRows" :key="index" class="field-row">
          <input v-model.trim="row.label" type="text" placeholder="字段名，如：联系方式" />
          <select v-model="row.type">
            <option v-for="type in FIELD_TYPES" :key="type.value" :value="type.value">
              {{ type.label }}
            </option>
          </select>
          <button class="del" type="button" @click="removeFieldRow(index)">删除</button>
        </div>
        <button class="add" type="button" @click="addFieldRow">+ 添加字段</button>

        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="notice" class="success">{{ notice }}</p>
        <button class="submit" type="submit" :disabled="submitting">
          {{ submitting ? '提交中...' : '提交活动' }}
        </button>
      </form>
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
.back, .back2 {
  padding: 6px 12px;
  font-size: 13px;
  background: #8a94a6;
}
.back2 { width: 120px; }

.content { padding: 24px; display: flex; justify-content: center; }
.form {
  width: 100%;
  max-width: 760px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  background: #fff;
  border-radius: 10px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}
.form h2 {
  margin: 6px 0 0;
  font-size: 15px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eef0f5;
}
.row { display: flex; gap: 16px; }
.row > label { flex: 1; min-width: 0; }
textarea {
  padding: 9px 10px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  resize: vertical;
}
textarea:focus { border-color: #4a7dff; }
.checks { display: flex; gap: 24px; }
.check { flex-direction: row; align-items: center; gap: 8px; }
.check input { width: 16px; height: 16px; }

.field-row { display: flex; gap: 10px; align-items: center; }
.field-row input { flex: 1; min-width: 0; }
.field-row select { width: 130px; }
.del { padding: 8px 12px; font-size: 13px; background: #f0f1f5; color: #777; }
.add { padding: 8px 12px; font-size: 13px; background: #eef2ff; color: #4a7dff; }

.hint { margin: 0; font-size: 12px; color: #999; }
.muted { color: #888; font-size: 14px; }
.error { color: #e34d4d; font-size: 13px; margin: 0; }
.success { color: #22a06b; font-size: 13px; margin: 0; }
.submit { margin-top: 8px; }
.panel {
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  background: #fff;
  border-radius: 10px;
  padding: 28px 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}
</style>
