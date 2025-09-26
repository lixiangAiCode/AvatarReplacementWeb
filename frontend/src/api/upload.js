import api from './request'

// 上传聊天截图
export const uploadChatImage = (sessionId, file) => {
  const formData = new FormData()
  formData.append('file', file)

  return api.post(`/${sessionId}/upload/chat-image`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 上传新头像
export const uploadAvatar = (sessionId, file) => {
  const formData = new FormData()
  formData.append('file', file)

  return api.post(`/${sessionId}/upload/avatar`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 设置模板区域
export const setTemplate = (sessionId, bbox) => {
  return api.post(`/${sessionId}/template/set`, bbox)
}

// 开始处理（最终替换）
export const startProcessing = (sessionId, config = {}) => {
  return api.post(`/${sessionId}/process/start`, {
    selected_avatars: config.selected_avatars || [],
    threshold: config.threshold || 0.8,
    right_ratio: config.right_ratio || 0.6
  })
}

// 获取结果下载链接
export const getDownloadUrl = (sessionId) => {
  return `/api/${sessionId}/result/download`
}