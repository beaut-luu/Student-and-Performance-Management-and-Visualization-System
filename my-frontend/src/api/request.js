import axios from 'axios'

const request = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  timeout: 10000,
})

request.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const resp = error.response
    if (resp && resp.status === 401) {
      localStorage.removeItem('token')
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    let message = '请求失败，请稍后重试'
    const data = resp?.data
    if (data?.message) {
      message = data.message
    } else if (resp?.status === 422 && Array.isArray(data?.detail) && data.detail.length) {
      // FastAPI/Pydantic 参数校验错误：提取第一个字段的错误信息
      message = data.detail[0].msg || message
    }
    const err = new Error(message)
    // 保留状态码，便于调用方区分 403（权限不足）等场景
    err.status = resp?.status
    return Promise.reject(err)
  },
)

export default request
