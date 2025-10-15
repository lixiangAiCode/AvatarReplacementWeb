<template>
  <div class="result-preview">
    <!-- 检测结果展示 -->
    <div v-if="appStore.detectedAvatars && appStore.detectedAvatars.length > 0 && appStore.sessionStatus !== 'completed' && appStore.sessionStatus !== 'processing'" class="detected-avatars">
      <!-- 检测结果标题 -->
      <el-card class="detection-summary">
        <div class="summary-content">
          <el-icon class="summary-icon"><Search /></el-icon>
          <div class="summary-text">
            <h3 class="summary-title">{{ $t('process.completed') }}</h3>
            <p class="summary-message">
              {{ $t('process.avatarsFound', { count: appStore.detectedAvatars.length }) }}
            </p>
          </div>
        </div>
      </el-card>

      <!-- 检测结果预览图 -->
      <el-card v-if="appStore.previewImage" class="preview-card">
        <template #header>
          <div class="card-header">
            <el-icon><PictureRounded /></el-icon>
            <span>{{ $t('results.original') }}</span>
          </div>
        </template>
        
        <div class="preview-container">
          <div class="preview-image-wrapper">
            <img 
              :src="`data:image/png;base64,${appStore.previewImage}`"
              :alt="$t('results.original')"
              class="detection-preview-image"
            />
          </div>
          <div class="preview-legend">
            <div class="legend-item">
              <div class="legend-box detection-box"></div>
              <span v-if="$i18n.locale === 'en'">Detected Similar Avatars</span>
              <span v-else>检测到的相似头像</span>
            </div>
            <div class="legend-item">
              <div class="legend-number">1</div>
              <span v-if="$i18n.locale === 'en'">Avatar Number</span>
              <span v-else>头像编号</span>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 操作按钮 -->
      <div class="action-section">
        <el-button
          type="primary"
          size="large"
          :loading="processing"
          @click="confirmReplacement"
          class="confirm-btn"
        >
          <el-icon><Check /></el-icon>
          {{ processing ? $t('process.title') : $t('process.startProcessing') }}
        </el-button>
        <el-button
          size="large"
          @click="goBackToTemplate"
          :disabled="processing"
        >
          <el-icon><ArrowLeft /></el-icon>
          {{ $t('template.title') }}
        </el-button>
      </div>
    </div>

    <!-- 处理中状态 -->
    <div v-else-if="appStore.sessionStatus === 'processing'" class="processing-status">
      <el-card class="status-card">
        <div class="status-content">
          <el-icon class="processing-icon"><Loading /></el-icon>
          <h3 class="status-title">{{ $t('process.title') }}</h3>
          <p class="status-message">{{ appStore.message }}</p>
          <el-progress
            :percentage="appStore.progress"
            :stroke-width="8"
            class="status-progress"
          />
        </div>
      </el-card>
    </div>

    <!-- 处理完成 -->
    <div v-else-if="appStore.sessionStatus === 'completed'" class="result-content">
      <!-- 成功状态 -->
      <el-card class="success-card">
        <div class="success-header">
          <el-icon class="success-icon"><SuccessFilled /></el-icon>
          <div class="success-text">
            <h3 class="success-title">{{ $t('process.completed') }}!</h3>
            <p class="success-message">{{ getCompletionMessage() }}</p>
          </div>
        </div>
      </el-card>

      <!-- 结果展示 -->
      <el-card class="result-card">
        <template #header>
          <div class="card-header">
            <el-icon><PictureRounded /></el-icon>
            <span>{{ $t('results.processed') }}</span>
          </div>
        </template>

        <div class="result-display">
          <!-- 原图对比 -->
          <div class="comparison-section">
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="image-container">
                  <div class="image-title">{{ $t('results.original') }}</div>
                  <div class="image-wrapper">
                    <img
                      :src="appStore.chatImage"
                      :alt="$t('results.original')"
                      class="preview-image"
                    />
                  </div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="image-container">
                  <div class="image-title">{{ $t('results.processed') }}</div>
                  <div class="image-wrapper">
                    <img
                      :src="resultImageUrl"
                      :alt="$t('results.processed')"
                      class="preview-image"
                      @load="handleResultImageLoad"
                    />
                  </div>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>
      </el-card>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button
          type="primary"
          size="large"
          :icon="Download"
          @click="downloadResult"
          class="download-btn"
        >
          {{ $t('results.downloadProcessed') }}
        </el-button>
        <el-button
          size="large"
          :icon="View"
          @click="previewResult"
        >
          {{ $t('results.view') }}
        </el-button>
      </div>
    </div>

    <!-- 处理失败 -->
    <div v-else-if="appStore.sessionStatus === 'error'" class="error-content">
      <el-card class="error-card">
        <div class="error-content-inner">
          <el-icon class="error-icon"><CircleCloseFilled /></el-icon>
          <h3 class="error-title">{{ $t('process.failed') }}</h3>
          <p class="error-message">{{ appStore.message }}</p>
          <el-button type="primary" @click="goBackToTemplate">
            <el-icon><RefreshLeft /></el-icon>
            {{ $t('common.reset') }}
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <el-empty
        image="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
        :description="$t('steps.uploadImages')"
      />
    </div>

    <!-- 全屏预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      :title="$t('results.view')"
      :width="'90%'"
      center
      destroy-on-close
    >
      <div class="fullscreen-preview">
        <img
          :src="resultImageUrl"
          :alt="$t('results.processed')"
          class="fullscreen-image"
        />
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { useAppStore } from '../stores/app'
import { startProcessing, getDownloadUrl } from '../api/upload'
import {
  Search,
  PictureRounded,
  Check,
  ArrowLeft,
  Loading,
  SuccessFilled,
  Download,
  View,
  CircleCloseFilled,
  RefreshLeft
} from '@element-plus/icons-vue'

const { t } = useI18n()
const emit = defineEmits(['confirm-replace'])
const appStore = useAppStore()

// 处理状态
const processing = ref(false)

// 对话框状态
const previewDialogVisible = ref(false)


const resultImageUrl = computed(() => {
  if (appStore.sessionStatus === 'completed' && appStore.resultImage) {
    // 使用base64图片数据
    return `data:image/png;base64,${appStore.resultImage}`
  }
  return ''
})

// 获取完成消息
const getCompletionMessage = () => {
  if (appStore.sessionStatus === 'completed') {
    // 如果有检测到的头像数量信息，显示替换数量
    if (appStore.detectedAvatars && appStore.detectedAvatars.length > 0) {
      return t('process.avatarsReplaced', { count: appStore.detectedAvatars.length })
    }
    return t('process.completed')
  }
  return appStore.message || ''
}

// 方法
const confirmReplacement = async () => {
  if (!appStore.detectedAvatars || appStore.detectedAvatars.length === 0) return

  processing.value = true
  // 设置处理状态
  appStore.sessionStatus = 'processing'
  appStore.progress = 0
  appStore.message = t('process.replacing')

  try {
    // 自动选择所有检测到的头像进行替换
    const allAvatarIds = appStore.detectedAvatars.map(avatar => avatar.id)
    
    // 调用start接口并等待处理完成
    const response = await startProcessing(appStore.sessionId, {
      selected_avatars: allAvatarIds,
      threshold: 0.8,
      right_ratio: 0.6
    })

    // 处理返回的结果
    const result = response.data || response
    if (result.success && result.result_base64) {
      // 直接设置处理结果
      appStore.resultImage = result.result_base64
      appStore.sessionStatus = 'completed'
      appStore.progress = 100
      appStore.message = result.message
      
      // 触发确认替换事件，通知父组件更新页面状态
      emit('confirm-replace')
      
      ElMessage.success(t('process.completed') + '!')
    } else {
      throw new Error(result.message || t('errors.processingFailed'))
    }
  } catch (error) {
    appStore.sessionStatus = 'error'
    appStore.message = t('errors.processingFailed')
    
    // 即使出错也要触发事件，让父组件知道处理完成了
    emit('confirm-replace')
    
    ElMessage.error(t('errors.processingFailed'))
  } finally {
    processing.value = false
  }
}

const goBackToTemplate = () => {
  // 触发回到模板选择步骤
  appStore.detectedAvatars = []
  appStore.previewImage = ''
  appStore.sessionStatus = 'idle'
  // 这里可以通过emit通知父组件或者直接操作步骤
}

const handleResultImageLoad = () => {
  // 图片加载完成逻辑
}

const downloadResult = () => {
  if (appStore.resultImage) {
    try {
      // 使用base64数据进行下载
      const byteCharacters = atob(appStore.resultImage)
      const byteNumbers = new Array(byteCharacters.length)
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i)
      }
      const byteArray = new Uint8Array(byteNumbers)
      const blob = new Blob([byteArray], { type: 'image/png' })
      
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `chat_avatar_replaced_${Date.now()}.png`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      // 清理创建的URL对象
      URL.revokeObjectURL(link.href)
      
      ElMessage.success(t('common.success') + '!')
    } catch (error) {
      console.error('Download failed:', error)
      ElMessage.error(t('common.error'))
    }
  } else {
    ElMessage.warning(t('errors.missingFiles'))
  }
}

const previewResult = () => {
  previewDialogVisible.value = true
}
</script>

<style scoped>
.result-preview {
  padding: 20px;
}

/* 检测结果样式 */
.detection-summary {
  margin-bottom: 20px;
  border: none;
  background: linear-gradient(135deg, #409eff 0%, #53a7ff 100%);
  color: white;
}

.summary-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}

.summary-icon {
  font-size: 32px;
}

.summary-title {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 600;
}

.summary-message {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}

/* 预览图片 */
.preview-card {
  margin-bottom: 20px;
  border: none;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.preview-container {
  text-align: center;
}

.preview-image-wrapper {
  margin-bottom: 16px;
  border-radius: 8px;
  overflow: hidden;
  display: inline-block;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.detection-preview-image {
  max-width: 100%;
  max-height: 500px;
  object-fit: contain;
  display: block;
}

.preview-legend {
  display: flex;
  justify-content: center;
  gap: 24px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.legend-box {
  width: 16px;
  height: 16px;
  border-radius: 2px;
}

.detection-box {
  background: #00ff00;
  border: 2px solid #00cc00;
}

.legend-number {
  width: 20px;
  height: 20px;
  background: #00ff00;
  color: white;
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
}

/* 操作按钮 */
.action-section {
  text-align: center;
}

.confirm-btn {
  font-size: 16px;
  font-weight: 600;
  margin-right: 16px;
}

/* 处理中状态 */
.processing-status {
  text-align: center;
}

.status-card {
  max-width: 600px;
  margin: 0 auto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.status-content {
  padding: 40px 20px;
}

.processing-icon {
  font-size: 48px;
  margin-bottom: 20px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.status-title {
  margin: 0 0 12px 0;
  font-size: 24px;
  font-weight: 600;
}

.status-message {
  margin: 0 0 24px 0;
  font-size: 16px;
  opacity: 0.9;
}

.status-progress {
  max-width: 400px;
  margin: 0 auto;
}

/* 成功状态 */
.success-card {
  margin-bottom: 20px;
  border: none;
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  color: white;
}

.success-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}

.success-icon {
  font-size: 32px;
}

.success-title {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 600;
}

.success-message {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}

/* 结果展示 */
.result-card {
  margin-bottom: 20px;
  border: none;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.comparison-section {
  margin-bottom: 30px;
}

.image-container {
  text-align: center;
}

.image-title {
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #606266;
}

.image-wrapper {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.preview-image {
  width: 100%;
  height: auto;
  display: block;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.download-btn {
  font-size: 16px;
  font-weight: 600;
}

/* 错误状态 */
.error-card {
  border: none;
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
  color: white;
}

.error-content-inner {
  text-align: center;
  padding: 40px 20px;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.error-title {
  margin: 0 0 12px 0;
  font-size: 24px;
  font-weight: 600;
}

.error-message {
  margin: 0 0 24px 0;
  font-size: 16px;
  opacity: 0.9;
}

/* 全屏预览 */
.fullscreen-preview {
  text-align: center;
}

.fullscreen-image {
  max-width: 100%;
  max-height: 70vh;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

/* 响应式 */
@media (max-width: 768px) {
  .avatars-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
  }

  .action-buttons .el-button {
    width: 200px;
  }
}
</style>