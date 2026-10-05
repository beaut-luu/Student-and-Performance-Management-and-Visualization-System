<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getOrganizationProfile } from '@/api/activity'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref('')
const org = ref(null)

const actId = computed(() => route.params.actId)
// 后端没有社团头像时（logo 为空）用名称首字符兜底
const initial = computed(() => (org.value?.name ? org.value.name.trim().charAt(0) : '社'))

function goOwner() {
  const stuNum = org.value?.owner?.stu_number
  if (stuNum == null) return
  router.push({ name: 'userProfile', params: { stuNum } })
}

onMounted(async () => {
  try {
    const res = await getOrganizationProfile(actId.value)
    org.value = res?.data || null
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
      <button class="back" type="button" @click="router.back()">返回</button>
      <h1>社团主页</h1>
    </header>

    <main class="content">
      <p v-if="loading" class="muted">加载中...</p>
      <p v-else-if="error" class="error">{{ error }}</p>
      <p v-else-if="!org" class="muted">未找到该社团</p>

      <section v-else class="card">
        <div class="head">
          <img v-if="org.logo" class="logo" :src="org.logo" :alt="org.name" />
          <span v-else class="logo placeholder">{{ initial }}</span>
          <div class="head-text">
            <h2>{{ org.name }}</h2>
            <p>社团主页</p>
          </div>
        </div>

        <div class="rows">
          <div class="row wide">
            <span class="label">社团描述</span>
            <span class="value box">{{ org.description }}</span>
          </div>
          <div class="row"><span class="label">联系方式</span><span class="value">{{ org.contact }}</span></div>
          <div class="row">
            <span class="label">会长</span>
            <span v-if="org.owner" class="value link" title="查看会长主页" @click="goOwner">
              {{ org.owner.name }}<i class="go">›</i>
            </span>
            <span v-else class="value">—</span>
          </div>
          <div v-if="org.owner" class="row">
            <span class="label">会长学号</span><span class="value">{{ org.owner.stu_number }}</span>
          </div>
        </div>
      </section>
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
.card {
  width: 100%;
  max-width: 640px;
  height: fit-content;
  padding: 24px 28px 26px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 14px rgba(28, 44, 88, 0.07);
}
.head { display: flex; align-items: center; gap: 16px; padding-bottom: 18px; border-bottom: 1px solid #f4f5f9; }
.logo { width: 56px; height: 56px; border-radius: 12px; object-fit: cover; flex: none; }
.logo.placeholder {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #4a7dff;
  color: #fff;
  font-size: 24px;
  font-weight: 600;
}
.head-text h2 { margin: 0 0 4px; font-size: 20px; }
.head-text p { margin: 0; font-size: 13px; color: #9aa1ae; }

.rows { display: grid; grid-template-columns: 1fr 1fr; gap: 2px 28px; margin-top: 14px; }
.row { display: flex; gap: 12px; padding: 9px 0; border-bottom: 1px solid #f4f5f9; }
.row.wide { grid-column: 1 / -1; flex-direction: column; gap: 6px; }
.label { width: 76px; flex: none; font-size: 13px; color: #9aa1ae; }
.row.wide .label { width: auto; }
.value { font-size: 14px; color: #2c2c2c; line-height: 1.7; word-break: break-word; }
.value.box {
  display: block;
  padding: 10px 14px;
  background: #fafbfe;
  border-radius: 8px;
  white-space: pre-wrap;
}

/* 可点击文本：与活动详情页保持一致 */
.link { color: #4a7dff; cursor: pointer; border-bottom: 1px dashed #9dbbff; transition: color 0.15s, border-color 0.15s; }
.link:hover { color: #2f63e6; border-bottom-color: #2f63e6; border-bottom-style: solid; }
.link .go { margin-left: 2px; font-style: normal; opacity: 0.75; }

.muted { color: #888; font-size: 14px; }
.error { color: #e34d4d; font-size: 14px; }
</style>
