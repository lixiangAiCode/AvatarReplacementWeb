import api from './request'

// 创建会话
export const createSession = () => {
  return api.post('/session/create')
}

// 获取会话状态
export const getSessionStatus = (sessionId) => {
  return api.get(`/session/${sessionId}/status`)
}

// 删除会话
export const deleteSession = (sessionId) => {
  return api.delete(`/session/${sessionId}`)
}