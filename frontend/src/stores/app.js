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

  // 检测到的相似头像
  const detectedAvatars = ref([])

  // 预览图片（带检测框标注）
  const previewImage = ref('')

  // 处理结果
  const result = ref(null)
  const resultUrl = ref(null)
  const resultImage = ref('')

  // 创建新会话
  const initSession = async () => {
    try {
      const response = await createSession()
      
      // 确保正确提取响应数据
      const data = response.data || response
      sessionId.value = data.session_id
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
      const response = await getSessionStatus(sessionId.value)
      
      // 确保正确提取响应数据
      const status = response.data || response
      sessionStatus.value = status.status
      progress.value = status.progress
      message.value = status.message
      
      // 如果有结果图片，保存到状态
      if (status.result_base64) {
        resultImage.value = status.result_base64
      }
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
    detectedAvatars.value = []
    previewImage.value = ''
    result.value = null
    resultUrl.value = null
    resultImage.value = ''
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
    detectedAvatars,
    previewImage,
    result,
    resultUrl,
    resultImage,

    // 方法
    initSession,
    updateStatus,
    resetState
  }
})