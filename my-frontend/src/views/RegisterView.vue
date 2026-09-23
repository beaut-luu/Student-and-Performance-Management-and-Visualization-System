<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/auth'

const router = useRouter()

const form = ref({
  username: '',
  name: '',
  password: '',
  confirm: '',
  stu_number: '',
  email: '',
})
const error = ref('')
const loading = ref(false)

function validate() {
  if (!form.value.username) return '用户名不能为空'
  if (form.value.username.length > 64) return '用户名不能超过64个字符'
  if (!form.value.name) return '真实姓名不能为空'
  if (form.value.name.length > 25) return '真实姓名不能超过25个字符'
  if (!form.value.password) return '密码不能为空'
  if (form.value.password.length < 6) return '密码至少6位'
  if (form.value.password !== form.value.confirm) return '两次输入的密码不一致'
  if (!/^\d{12}$/.test(form.value.stu_number)) return '请输入12位数字学号'
  if (form.value.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    return '请输入正确的邮箱'
  }
  return ''
}

async function onSubmit() {
  error.value = validate()
  if (error.value) return
  loading.value = true
  try {
    const payload = {
      username: form.value.username,
      name: form.value.name,
      password: form.value.password,
      stu_number: Number(form.value.stu_number),
    }
    // 邮箱为空时直接不传该字段，让后端使用默认值（后端不接受显式 null）
    if (form.value.email) payload.email = form.value.email
    await register(payload)
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
    <form class="card" style="width: 380px" @submit.prevent="onSubmit">
      <h2>注册</h2>
      <label>
        用户名
        <input v-model.trim="form.username" type="text" placeholder="用于登录，最少1个字符" required />
      </label>
      <label>
        真实姓名
        <input v-model.trim="form.name" type="text" placeholder="请输入真实姓名，仅用于验证身份" required />
      </label>
      <label>
        学号
        <input v-model.trim="form.stu_number" type="text" inputmode="numeric" placeholder="请输入12位学号" required />
      </label>
      <label>
        密码（至少6位）
        <input v-model="form.password" type="password" placeholder="请输入密码" required />
      </label>
      <label>
        确认密码
        <input v-model="form.confirm" type="password" placeholder="请再次输入密码" required />
      </label>
      <label>
        邮箱（可选）
        <input v-model.trim="form.email" type="email" placeholder="请输入正确的邮箱" />
      </label>
      <p v-if="error" class="error">{{ error }}</p>
      <button type="submit" :disabled="loading">{{ loading ? '注册中...' : '注册' }}</button>
      <p class="tip">已有账号？<router-link to="/login">去登录</router-link></p>
    </form>
  </div>
</template>
