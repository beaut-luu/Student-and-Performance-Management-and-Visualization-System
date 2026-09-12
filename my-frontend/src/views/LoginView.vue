<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const form = ref({ username: '', password: '' })
const error = ref('')
const notice = ref('')
const loading = ref(false)

onMounted(() => {
  if (route.query.msg) {
    notice.value = route.query.msg
    router.replace({ name: 'login' })
  }
})

async function onSubmit() {
  error.value = ''
  loading.value = true
  try {
    await auth.login({ username: form.value.username, password: form.value.password })
    router.push('/')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">
    <form class="card" style="width: 360px" @submit.prevent="onSubmit">
      <h2>登录</h2>
      <p v-if="notice" class="success">{{ notice }}</p>
      <label>
        用户名
        <input v-model.trim="form.username" type="text" placeholder="请输入用户名" required />
      </label>
      <label>
        密码
        <input v-model="form.password" type="password" placeholder="请输入密码" required />
      </label>
      <p v-if="error" class="error">{{ error }}</p>
      <button type="submit" :disabled="loading">{{ loading ? '登录中...' : '登录' }}</button>
      <p class="tip">还没有账号？<router-link to="/register">去注册</router-link></p>
    </form>
  </div>
</template>
