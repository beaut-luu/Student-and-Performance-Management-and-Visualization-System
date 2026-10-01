<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useActivityStore } from '@/stores/activity'
import { changeUsername, changePassword, changeJurisdiction } from '@/api/user'
import { JURISDICTIONS, jurisdictionLabel } from '@/constants/jurisdiction'
import UserAvatar from '@/components/UserAvatar.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const activity = useActivityStore()

const MENU = [
  { key: 'username', label: '修改用户名' },
  { key: 'password', label: '修改密码' },
  { key: 'jurisdiction', label: '修改权限' },
  { key: 'activities', label: '我的活动' },
]

const activeTab = ref('username')
const loading = ref(true)
const error = ref('')
const isAdmin = computed(() => auth.user?.jurisdiction === 'admin')

const unameForm = ref({ newName: '' })
const unameMsg = ref('')

const pwdForm = ref({ oldPwd: '', newPwd: '' })
const pwdMsg = ref('')
const pwdOk = ref(false)

const jurForm = ref({ targetUsername: '', jur: 'user' })
const jurMsg = ref('')
const jurOk = ref(false)

// “我的活动”当前只接入“我组织的活动 -> 待审核活动”这一条路径
const pendingActivities = computed(() =>
  activity.lastCreated?.status === 'pending_review' ? [activity.lastCreated] : [],
)

function applyQueryTab() {
  const tab = route.query.tab
  if (typeof tab === 'string' && MENU.some((item) => item.key === tab)) activeTab.value = tab
}

onMounted(async () => {
  applyQueryTab()
  try {
    await auth.fetchMe()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

watch(() => route.query.tab, applyQueryTab)

function selectMenu(key) {
  activeTab.value = key
  // 同步到地址栏，方便“我的活动”这类深层入口被直接跳转过来
  router.replace({ name: 'profile', query: { ...route.query, tab: key } })
}

function logout() {
  auth.logout()
  router.push('/login')
}

async function onChangeUsername() {
  unameMsg.value = ''
  if (!unameForm.value.newName) {
    unameMsg.value = '请输入新用户名'
    return
  }
  try {
    await changeUsername(unameForm.value.newName)
    // 改名后旧 token 里的用户名已失效，需要重新登录
    auth.logout()
    router.push({ name: 'login', query: { msg: '用户名修改成功，请使用新用户名重新登录' } })
  } catch (e) {
    unameMsg.value = e.message
  }
}

async function onChangePassword() {
  pwdMsg.value = ''
  pwdOk.value = false
  if (!pwdForm.value.oldPwd || pwdForm.value.newPwd.length < 6) {
    pwdMsg.value = '请输入原密码，新密码至少6位'
    return
  }
  try {
    await changePassword(pwdForm.value.oldPwd, pwdForm.value.newPwd)
    pwdOk.value = true
    pwdMsg.value = '密码修改成功'
    pwdForm.value = { oldPwd: '', newPwd: '' }
  } catch (e) {
    pwdMsg.value = e.message
  }
}

async function onChangeJurisdiction() {
  jurMsg.value = ''
  jurOk.value = false
  if (!jurForm.value.targetUsername) {
    jurMsg.value = '请输入目标用户名'
    return
  }
  try {
    await changeJurisdiction({
      target_username: jurForm.value.targetUsername,
      jur: jurForm.value.jur,
    })
    jurOk.value = true
    jurMsg.value = '权限修改成功'
  } catch (e) {
    jurMsg.value = e.message
  }
}
</script>

<template>
  <div class="profile">
    <header class="top">
      <UserAvatar :name="auth.user?.username || ''" :size="56" />
      <div class="info">
        <h1>{{ auth.user?.username || '未登录' }}</h1>
        <p>
          <span class="tag">{{ jurisdictionLabel(auth.user?.jurisdiction) }}</span>
          <span class="muted">身份 / 权限信息来自 /users/me</span>
        </p>
      </div>
      <button class="logout" type="button" @click="logout">退出登录</button>
    </header>

    <div class="body">
      <nav class="menu">
        <button
          v-for="item in MENU"
          :key="item.key"
          type="button"
          class="menu-item"
          :class="{ on: activeTab === item.key }"
          @click="selectMenu(item.key)"
        >
          {{ item.label }}
        </button>
      </nav>

      <section class="pane">
        <p v-if="loading" class="muted">加载中...</p>
        <p v-else-if="error" class="error">{{ error }}</p>

        <template v-else>
          <div v-if="activeTab === 'username'" class="form">
            <h2>修改用户名</h2>
            <label>
              新用户名
              <input v-model.trim="unameForm.newName" type="text" placeholder="请输入新用户名" />
            </label>
            <p class="hint">修改成功后需使用新用户名重新登录</p>
            <p v-if="unameMsg" class="error">{{ unameMsg }}</p>
            <button class="submit" type="button" @click="onChangeUsername">保存</button>
          </div>

          <div v-else-if="activeTab === 'password'" class="form">
            <h2>修改密码</h2>
            <label>
              原密码
              <input v-model="pwdForm.oldPwd" type="password" placeholder="请输入原密码" />
            </label>
            <label>
              新密码（至少6位）
              <input v-model="pwdForm.newPwd" type="password" placeholder="请输入新密码" />
            </label>
            <p v-if="pwdMsg" :class="pwdOk ? 'success' : 'error'">{{ pwdMsg }}</p>
            <button class="submit" type="button" @click="onChangePassword">保存</button>
          </div>

          <div v-else-if="activeTab === 'jurisdiction'" class="form">
            <h2>修改权限</h2>
            <template v-if="isAdmin">
              <label>
                目标用户名
                <input v-model.trim="jurForm.targetUsername" type="text" placeholder="要修改谁" />
              </label>
              <label>
                权限
                <select v-model="jurForm.jur">
                  <option v-for="item in JURISDICTIONS" :key="item.value" :value="item.value">
                    {{ item.label }}
                  </option>
                </select>
              </label>
              <p v-if="jurMsg" :class="jurOk ? 'success' : 'error'">{{ jurMsg }}</p>
              <button class="submit" type="button" @click="onChangeJurisdiction">保存</button>
            </template>
            <p v-else class="muted">仅管理员可以修改他人权限</p>
          </div>

          <div v-else class="activities">
            <p class="crumbs">我的活动 <i>›</i> 我组织的活动 <i>›</i> 待审核活动</p>
            <ul v-if="pendingActivities.length" class="act-list">
              <li v-for="item in pendingActivities" :key="item.id">
                <b>{{ item.title }}</b>
                <span class="muted">{{ item.location }}</span>
                <em>待审核</em>
              </li>
            </ul>
            <p v-else class="muted">暂无待审核活动</p>
          </div>
        </template>
      </section>
    </div>
  </div>
</template>

<style scoped>
.profile { height: 100vh; display: flex; flex-direction: column; background: #f5f6fa; }

/* 上部分：约占 1/7 */
.top {
  height: 14.3%;
  min-height: 88px;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 0 24px;
  background: #fff;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.06);
}
.info { display: flex; flex-direction: column; gap: 6px; }
.info h1 { margin: 0; font-size: 18px; }
.info p { margin: 0; display: flex; align-items: center; gap: 10px; font-size: 13px; }
.tag { padding: 2px 8px; border-radius: 999px; background: #eef2ff; color: #4a7dff; }
.muted { color: #999; font-size: 13px; margin: 0; }
.logout {
  margin-left: auto;
  padding: 7px 14px;
  font-size: 13px;
  background: #8a94a6;
}

/* 下部分：约占 6/7，再分左右 */
.body { flex: 1; display: flex; min-height: 0; }
.menu {
  width: 16.7%;
  min-width: 140px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 16px 12px;
  background: #fff;
  border-right: 1px solid #eceef3;
}
.menu-item {
  padding: 10px 12px;
  background: transparent;
  color: #444;
  font-size: 14px;
  text-align: left;
  border-radius: 8px;
}
.menu-item:hover { background: #f2f5ff; }
.menu-item.on { background: #eef2ff; color: #4a7dff; font-weight: 600; }

.pane { flex: 1; min-width: 0; overflow-y: auto; padding: 24px; }
.form { display: flex; flex-direction: column; gap: 12px; max-width: 420px; }
.form h2 { margin: 0 0 4px; font-size: 16px; }
.hint { margin: 0; font-size: 12px; color: #999; }
.submit { width: 120px; }
.error { color: #e34d4d; font-size: 13px; margin: 0; }
.success { color: #22a06b; font-size: 13px; margin: 0; }

.crumbs { margin: 0 0 14px; font-size: 13px; color: #666; }
.crumbs i { margin: 0 6px; color: #bbb; font-style: normal; }
.act-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 10px; }
.act-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}
.act-list em { margin-left: auto; font-style: normal; font-size: 12px; color: #d98a00; }
</style>
