<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useActivityStore } from '@/stores/activity'
import { changeUsername, changePassword, changeJurisdiction, getMyInfo } from '@/api/user'
import { JURISDICTIONS, jurisdictionLabel } from '@/constants/jurisdiction'
import UserAvatar from '@/components/UserAvatar.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const activity = useActivityStore()

const MENU = [
  { key: 'info', label: '我的信息' },
  { key: 'username', label: '修改用户名' },
  { key: 'password', label: '修改密码' },
  { key: 'jurisdiction', label: '修改权限' },
  { key: 'activities', label: '我的活动' },
]

// 社团角色 → 页面展示的称谓（与后端 OrganizationRole 枚举对应）
const ORG_ROLE_LABEL = {
  owner: '会长',
  manager: '部长',
  member: '成员',
}

const activeTab = ref('info')
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

// 我的信息
const myInfo = ref(null)
const infoError = ref('')

// 社团字段只展示文本，如 org_name=学生会 + role=owner → “担任学生会会长”
const orgTexts = computed(() =>
  (myInfo.value?.org_member || []).map(
    (item) => `担任${item.org_name}${ORG_ROLE_LABEL[item.role] || item.role}`,
  ),
)

async function loadMyInfo() {
  infoError.value = ''
  try {
    const res = await getMyInfo()
    myInfo.value = res?.data || null
  } catch (e) {
    infoError.value = e.message
  }
}

// “我的活动”下的二级选项：我参与的活动 / 我组织的活动
const ACTIVITY_SUBS = [
  { value: 'joined', label: '我参与的活动' },
  { value: 'organized', label: '我组织的活动' },
]
// “我组织的活动”下的三级状态选项，取值对应后端 ActivityStatus
const STATUS_TABS = [
  { value: 'published', label: '审核通过' },
  { value: 'pending_review', label: '待审核' },
  { value: 'reject', label: '审核未通过' },
]

const subTab = ref('joined')
const statusTab = ref('published')
const statusLabel = computed(
  () => STATUS_TABS.find((item) => item.value === statusTab.value)?.label || '',
)

// 列表接口尚未接入，这里只展示本次会话中刚创建的活动
const organizedActivities = computed(() =>
  activity.lastCreated?.status === statusTab.value ? [activity.lastCreated] : [],
)

function applyQuery() {
  const { tab, sub, status } = route.query
  if (typeof tab === 'string' && MENU.some((item) => item.key === tab)) activeTab.value = tab
  if (typeof sub === 'string' && ACTIVITY_SUBS.some((item) => item.value === sub)) subTab.value = sub
  if (typeof status === 'string' && STATUS_TABS.some((item) => item.value === status)) {
    statusTab.value = status
  }
}

onMounted(async () => {
  applyQuery()
  // 让地址栏始终反映当前选中的功能，保持可分享/可刷新
  syncQuery()
  loadMyInfo()
  try {
    await auth.fetchMe()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

watch(() => route.query, applyQuery)

function syncQuery() {
  const query = { tab: activeTab.value }
  if (activeTab.value === 'activities') {
    query.sub = subTab.value
    query.status = statusTab.value
  }
  // 同步到地址栏，方便“我的活动”这类深层入口被直接跳转过来
  router.replace({ name: 'profile', query })
}

function selectMenu(key) {
  activeTab.value = key
  syncQuery()
}

function selectSub(value) {
  subTab.value = value
  syncQuery()
}

function selectStatus(value) {
  statusTab.value = value
  syncQuery()
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
      <div class="actions">
        <button class="back" type="button" @click="router.push({ name: 'home' })">返回主页</button>
        <button class="logout" type="button" @click="logout">退出登录</button>
      </div>
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

          <div v-else-if="activeTab === 'info'" class="info">
            <h2>我的信息</h2>
            <p v-if="infoError" class="error">{{ infoError }}</p>
            <p v-else-if="!myInfo" class="muted">加载中...</p>
            <dl v-else class="info-list">
              <div><dt>用户名</dt><dd>{{ myInfo.username }}</dd></div>
              <div><dt>真实姓名</dt><dd>{{ myInfo.name }}</dd></div>
              <div><dt>身份</dt><dd>{{ jurisdictionLabel(myInfo.jurisdiction) }}</dd></div>
              <div><dt>学号</dt><dd>{{ myInfo.stu_number }}</dd></div>
              <div><dt>邮箱</dt><dd>{{ myInfo.email || '未填写' }}</dd></div>
              <div>
                <dt>社团</dt>
                <dd>
                  <span v-for="text in orgTexts" :key="text" class="org-line">{{ text }}</span>
                  <span v-if="!orgTexts.length" class="muted">暂未加入社团</span>
                </dd>
              </div>
            </dl>
          </div>

          <div v-else class="activities">
            <div class="sub-tabs">
              <button
                v-for="item in ACTIVITY_SUBS"
                :key="item.value"
                type="button"
                class="sub-tab"
                :class="{ on: subTab === item.value }"
                @click="selectSub(item.value)"
              >
                {{ item.label }}
              </button>
            </div>

            <template v-if="subTab === 'organized'">
              <div class="status-tabs">
                <button
                  v-for="item in STATUS_TABS"
                  :key="item.value"
                  type="button"
                  class="status-tab"
                  :class="{ on: statusTab === item.value }"
                  @click="selectStatus(item.value)"
                >
                  {{ item.label }}
                </button>
              </div>
              <ul v-if="organizedActivities.length" class="act-list">
                <li v-for="item in organizedActivities" :key="item.id">
                  <b>{{ item.title }}</b>
                  <span class="muted">{{ item.location }}</span>
                  <em :class="statusTab">{{ statusLabel }}</em>
                </li>
              </ul>
              <p v-else class="muted">暂无{{ statusLabel }}的活动</p>
            </template>

            <p v-else class="muted">暂无参与的活动</p>
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
.actions { margin-left: auto; display: flex; gap: 10px; }
.back, .logout {
  padding: 7px 14px;
  font-size: 13px;
  background: #8a94a6;
}
.back { background: #eef2ff; color: #4a7dff; }

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

/* 我的信息：纯文本展示 */
.info { display: flex; flex-direction: column; gap: 14px; max-width: 520px; }
.info h2 { margin: 0; font-size: 16px; }
.info-list {
  margin: 0;
  padding: 4px 18px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}
.info-list > div { display: flex; gap: 16px; padding: 13px 0; border-bottom: 1px solid #f1f2f6; }
.info-list > div:last-child { border-bottom: none; }
.info-list dt { width: 72px; flex: none; color: #999; font-size: 14px; }
.info-list dd { margin: 0; color: #2c2c2c; font-size: 14px; word-break: break-all; }
.org-line { display: block; }
.org-line + .org-line { margin-top: 4px; }

/* 我的活动：二级“我参与/我组织” + 三级审核状态下拉 */
.sub-tabs { display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 1px solid #eceef3; }
.sub-tab {
  padding: 8px 14px;
  background: transparent;
  color: #666;
  font-size: 14px;
  border-radius: 8px 8px 0 0;
}
.sub-tab:hover { background: #f6f8ff; }
.sub-tab.on { color: #4a7dff; font-weight: 600; box-shadow: inset 0 -2px 0 #4a7dff; }

.status-tabs { display: flex; gap: 8px; margin-bottom: 16px; }
.status-tab {
  padding: 6px 14px;
  background: #f2f3f7;
  color: #666;
  font-size: 13px;
  border-radius: 999px;
}
.status-tab:hover { background: #e8ebf5; }
.status-tab.on { background: #4a7dff; color: #fff; }

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
.act-list em { margin-left: auto; font-style: normal; font-size: 12px; color: #666; }
.act-list em.published { color: #22a06b; }
.act-list em.pending_review { color: #d98a00; }
.act-list em.reject { color: #e34d4d; }
</style>
