import { defineStore } from 'pinia'
import { ref } from 'vue'
import { createSession, getSessionStatus } from '../api/session'

export const useAppStore = defineStore('app', () => {
  // 会话信息
  const sessionId = ref(null)
  const sessionStatus = ref('idle')
  const progress = ref(0)
  const message = ref('')

  // 上传的文件
  const chatImage = ref(null)
  const newAvatar = ref(null)

  // 模板区域
  const templateBbox = ref(null)

  // 处理结果
  const result = ref(null)
  const resultUrl = ref(null)

  // 创建新会话
  const initSession = async () => {
    try {
      const response = await createSession()
      sessionId.value = response.session_id
      sessionStatus.value = 'created'
      message.value = '会话创建成功'
      return true
    } catch (error) {
      console.error('创建会话失败:', error)
      return false
    }
  }

  // 更新会话状态
  const updateStatus = async () => {
    if (!sessionId.value) return

    try {
      const status = await getSessionStatus(sessionId.value)
      sessionStatus.value = status.status
      progress.value = status.progress
      message.value = status.message
    } catch (error) {
      console.error('获取状态失败:', error)
    }
  }

  // 重置状态
  const resetState = () => {
    sessionId.value = null
    sessionStatus.value = 'idle'
    progress.value = 0
    message.value = ''
    chatImage.value = null
    newAvatar.value = null
    templateBbox.value = null
    result.value = null
    resultUrl.value = null
  }

  return {
    // 状态
    sessionId,
    sessionStatus,
    progress,
    message,
    chatImage,
    newAvatar,
    templateBbox,
    result,
    resultUrl,

    // 方法
    initSession,
    updateStatus,
    resetState
  }
})