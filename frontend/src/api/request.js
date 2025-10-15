import axios from 'axios'

const api = axios.create({
  baseURL: 'https://institute-chelsea-schedules-think.trycloudflare.com/api',
  timeout: 30000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    // 不在这里显示错误消息，让组件层处理
    return Promise.reject(error)
  }
)

export default api