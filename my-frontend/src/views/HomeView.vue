<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useActivityStore } from '@/stores/activity'
import { jurisdictionLabel } from '@/constants/jurisdiction'
import UserAvatar from '@/components/UserAvatar.vue'

const router = useRouter()
const auth = useAuthStore()
const activity = useActivityStore()

const loading = ref(true)
const checking = ref(false)
const notice = ref('')
const tabNotice = ref('')

// 主页上方的功能入口，目前只有“活动”页面已完成
const NAV_TABS = [
  { key: 'campus', label: '校园生活' },
  { key: 'activity', label: '活动' },
  { key: 'market', label: '跳蚤市场' },
  { key: 'chat', label: '群聊' },
]

onMounted(async () => {
  try {
    await auth.fetchMe()
  } catch (e) {
    notice.value = e.message
  } finally {
    loading.value = false
  }
})

function onTabClick(item) {
  if (item.key === 'activity') {
    router.push({ name: 'activityList' })
    return
  }
  tabNotice.value = `「${item.label}」页面开发中，敬请期待`
}

function goProfile() {
  router.push({ name: 'profile' })
}

async function onCreateActivity() {
  notice.value = ''
  checking.value = true
  try {
    // 先拉取当前操作者的社团，拿到 org_id / org_name 后才允许进入创建页
    const options = await activity.fetchOrgOptions()
    if (!options.length) {
      notice.value = '非社团成员无法创建活动'
      return
    }
    router.push({ name: 'activityCreate' })
  } catch (e) {
    notice.value = e.status === 403 ? '非社团成员无法创建活动' : e.message
  } finally {
    checking.value = false
  }
}
</script>

<template>
  <div class="home">
    <header class="bar">
      <span class="brand">学生管理系统</span>
      <button class="user-chip" type="button" @click="goProfile">
        <UserAvatar :name="auth.user?.username || ''" :size="36" />
        <span class="chip-text">
          <b>{{ auth.user?.username || '未登录' }}</b>
          <small>{{ jurisdictionLabel(auth.user?.jurisdiction) }}</small>
        </span>
      </button>
    </header>

    <nav class="tabs">
      <button
        v-for="item in NAV_TABS"
        :key="item.key"
        type="button"
        class="tab"
        @click="onTabClick(item)"
      >
        {{ item.label }}
      </button>
    </nav>
    <p class="tab-notice" :class="{ show: !!tabNotice }">{{ tabNotice }}</p>

    <main class="stage">
      <p v-if="loading" class="hint">加载中...</p>

      <div v-else class="create-block">
        <p class="notice" :class="{ show: !!notice }">{{ notice }}</p>
        <button class="plus" type="button" :disabled="checking" @click="onCreateActivity">
          {{ checking ? '' : '+' }}
        </button>
        <span class="plus-label">创建活动</span>
      </div>
    </main>
  </div>
</template>

<style scoped>
.home { min-height: 100vh; display: flex; flex-direction: column; }
.bar {
  display: flex;
  align-items: center;
  padding: 12px 24px;
  background: #fff;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.06);
}
.brand { font-weight: 600; }
.user-chip {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px 6px 6px;
  background: transparent;
  border-radius: 999px;
  color: inherit;
  cursor: pointer;
}
.user-chip:hover { background: #f2f5ff; }
.chip-text { display: flex; flex-direction: column; align-items: flex-start; line-height: 1.25; }
.chip-text b { font-size: 14px; color: #2c2c2c; font-weight: 600; }
.chip-text small { font-size: 12px; color: #4a7dff; }

/* 上方居中的功能入口 */
.tabs {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  padding: 22px 24px 0;
}
.tab {
  padding: 9px 22px;
  background: #fff;
  color: #4b5468;
  font-size: 14px;
  border: 1px solid #e3e6ee;
  border-radius: 999px;
}
.tab:hover { border-color: #4a7dff; color: #4a7dff; }
.tab-notice {
  min-height: 18px;
  margin: 8px 0 0;
  text-align: center;
  font-size: 13px;
  color: #9aa1ae;
  opacity: 0;
  transition: opacity 0.2s;
}
.tab-notice.show { opacity: 1; }

.stage {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  padding: 24px 24px 72px;
}
.hint { margin: auto; color: #888; font-size: 14px; }

.create-block { display: flex; flex-direction: column; align-items: center; gap: 10px; }
.notice {
  min-height: 20px;
  margin: 0;
  font-size: 13px;
  color: #e34d4d;
  opacity: 0;
  transition: opacity 0.2s;
}
.notice.show { opacity: 1; }
.plus {
  width: 64px;
  height: 64px;
  padding: 0;
  border-radius: 50%;
  background: #4a7dff;
  color: #fff;
  font-size: 34px;
  line-height: 1;
  font-weight: 300;
  box-shadow: 0 6px 16px rgba(74, 125, 255, 0.35);
}
.plus:hover:not(:disabled) { background: #3a6cf0; }
.plus:disabled { opacity: 0.6; }
.plus-label { font-size: 14px; color: #555; }
</style>
