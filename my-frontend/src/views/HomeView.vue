<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { changeUsername, changePassword, changeJurisdiction } from '@/api/user'

const router = useRouter()
const auth = useAuthStore()

// 权限取值与后端 Jurisdiction 枚举保持一致
const JURISDICTIONS = [
  { value: 'admin', label: '管理员' },
  { value: 'user', label: '普通用户' },
  { value: 'student', label: '学生' },
  { value: 'org', label: '组织' },
]

const loading = ref(true)
const error = ref('')
const isAdmin = computed(() => auth.user?.jurisdiction === 'admin')
const roleLabel = computed(
  () => JURISDICTIONS.find((item) => item.value === auth.user?.jurisdiction)?.label || '未知',
)

const unameForm = ref({ newName: '' })
const unameMsg = ref('')

const pwdForm = ref({ oldPwd: '', newPwd: '' })
const pwdMsg = ref('')
const pwdOk = ref(false)

const jurForm = ref({ targetUsername: '', jur: 'user' })
const jurMsg = ref('')
const jurOk = ref(false)

onMounted(async () => {
  try {
    await auth.fetchMe()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

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
  <div class="home">
    <header class="bar">
      <span class="brand">学生管理系统</span>
      <span v-if="auth.user" class="who">
        {{ auth.user.username }}
        <em>{{ roleLabel }}</em>
      </span>
      <button class="logout" @click="logout">退出登录</button>
    </header>

    <main class="content">
      <p v-if="loading">加载中...</p>
      <p v-else-if="error" class="error">{{ error }}</p>

      <div v-else class="grid">
        <section class="card">
          <h3>修改用户名</h3>
          <label>
            新用户名
            <input v-model.trim="unameForm.newName" type="text" placeholder="请输入新用户名" />
          </label>
          <button @click="onChangeUsername">保存</button>
          <p v-if="unameMsg" class="error">{{ unameMsg }}</p>
          <p class="hint">修改成功后需使用新用户名重新登录</p>
        </section>

        <section class="card">
          <h3>修改密码</h3>
          <label>
            原密码
            <input v-model="pwdForm.oldPwd" type="password" placeholder="请输入原密码" />
          </label>
          <label>
            新密码（至少6位）
            <input v-model="pwdForm.newPwd" type="password" placeholder="请输入新密码" />
          </label>
          <button @click="onChangePassword">保存</button>
          <p v-if="pwdMsg" :class="pwdOk ? 'success' : 'error'">{{ pwdMsg }}</p>
        </section>

        <section v-if="isAdmin" class="card">
          <h3>修改用户权限</h3>
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
          <button @click="onChangeJurisdiction">保存</button>
          <p v-if="jurMsg" :class="jurOk ? 'success' : 'error'">{{ jurMsg }}</p>
        </section>
      </div>
    </main>
  </div>
</template>

<style scoped>
.home { min-height: 100vh; display: flex; flex-direction: column; }
.bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 24px;
  background: #fff;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.06);
}
.brand { font-weight: 600; }
.who { margin-left: auto; font-size: 14px; color: #555; }
.who em { margin-left: 6px; font-style: normal; color: #4a7dff; }
.logout { padding: 6px 12px; font-size: 13px; background: #8a94a6; }
.content { padding: 24px; }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  max-width: 1000px;
}
.grid .card { width: auto; }
.hint { font-size: 12px; color: #999; margin: 0; }
</style>
