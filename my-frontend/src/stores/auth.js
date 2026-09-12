import { ref } from 'vue'
import { defineStore } from 'pinia'
import { login as loginApi } from '@/api/auth'
import { getMe } from '@/api/user'

const TOKEN_KEY = 'token'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || '')
  const user = ref(null)

  function setToken(value) {
    token.value = value
    if (value) localStorage.setItem(TOKEN_KEY, value)
    else localStorage.removeItem(TOKEN_KEY)
  }

  async function login(payload) {
    const res = await loginApi(payload)
    setToken(res.data.access_token)
    await fetchMe()
  }

  async function fetchMe() {
    const res = await getMe()
    user.value = res.data
    return res.data
  }

  function logout() {
    setToken('')
    user.value = null
  }

  return { token, user, login, fetchMe, logout }
})
