<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCreatorProfile } from '@/api/activity'
import { formatOrgRole } from '@/constants/organization'
import UserAvatar from '@/components/UserAvatar.vue'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref('')
const profile = ref(null)

const stuNum = computed(() => route.params.stuNum)
const orgTexts = computed(() =>
  (profile.value?.org_member || []).map((item) => formatOrgRole(item.org_name, item.role)),
)

onMounted(async () => {
  try {
    const res = await getCreatorProfile(stuNum.value)
    profile.value = res?.data || null
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
      <h1>创建者主页</h1>
    </header>

    <main class="content">
      <p v-if="loading" class="muted">加载中...</p>
      <p v-else-if="error" class="error">{{ error }}</p>
      <p v-else-if="!profile" class="muted">未找到该用户</p>

      <section v-else class="card">
        <div class="head">
          <UserAvatar :name="profile.name || profile.username" :size="56" />
          <div class="head-text">
            <h2>{{ profile.name }}</h2>
            <p>@{{ profile.username }}</p>
          </div>
        </div>

        <div class="rows">
          <div class="row"><span class="label">用户名</span><span class="value">{{ profile.username }}</span></div>
          <div class="row"><span class="label">姓名</span><span class="value">{{ profile.name }}</span></div>
          <div class="row"><span class="label">学号</span><span class="value">{{ profile.stu_number }}</span></div>
          <div class="row wide">
            <span class="label">所属社团</span>
            <span class="value">
              <span v-for="text in orgTexts" :key="text" class="org-line">{{ text }}</span>
              <span v-if="!orgTexts.length">暂未加入社团</span>
            </span>
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
.head-text h2 { margin: 0 0 4px; font-size: 20px; }
.head-text p { margin: 0; font-size: 13px; color: #9aa1ae; }

.rows { display: grid; grid-template-columns: 1fr 1fr; gap: 2px 28px; margin-top: 14px; }
.row { display: flex; gap: 12px; padding: 9px 0; border-bottom: 1px solid #f4f5f9; }
.row.wide { grid-column: 1 / -1; }
.label { width: 76px; flex: none; font-size: 13px; color: #9aa1ae; }
.value { font-size: 14px; color: #2c2c2c; line-height: 1.7; word-break: break-word; }
.org-line { display: block; }
.org-line + .org-line { margin-top: 4px; }

.muted { color: #888; font-size: 14px; }
.error { color: #e34d4d; font-size: 14px; }
</style>
