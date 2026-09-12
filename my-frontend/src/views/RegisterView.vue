<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/auth'

const router = useRouter()

const form = ref({ username: '', password: '', confirm: '' })
const error = ref('')
const loading = ref(false)

async function onSubmit() {
  error.value = ''
  if (!form.value.username) {
    error.value = '用户名不能为空'
    return
  }
  if (!form.value.password) {
    error.value = '密码不能为空'
    return
  }
  if (form.value.password.length < 6) {
    error.value = '密码至少6位'
    return
  }
  if (form.value.password !== form.value.confirm) {
    error.value = '两次输入的密码不一致'
    return
  }
  loading.value = true
  try {
    await register({ username: form.value.username, password: form.value.password })
    router.push({ name: 'login', query: { msg: '注册成功，请登录' } })
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
      <h2>注册</h2>
      <label>
        用户名
        <input v-model.trim="form.username" type="text" placeholder="请输入用户名" required />
      </label>
      <label>
        密码（至少6位）
        <input v-model="form.password" type="password" placeholder="请输入密码" required />
      </label>
      <label>
        确认密码
        <input v-model="form.confirm" type="password" placeholder="请再次输入密码" required />
      </label>
      <p v-if="error" class="error">{{ error }}</p>
      <button type="submit" :disabled="loading">{{ loading ? '注册中...' : '注册' }}</button>
      <p class="tip">已有账号？<router-link to="/login">去登录</router-link></p>
    </form>
  </div>
</template>
