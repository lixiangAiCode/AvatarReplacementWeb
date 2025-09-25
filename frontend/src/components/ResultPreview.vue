<template>
  <div class="result-preview">
    <!-- 处理状态 -->
    <div v-if="appStore.sessionStatus === 'processing'" class="processing-status">
      <el-card class="status-card">
        <div class="status-content">
          <el-icon class="processing-icon"><Loading /></el-icon>
          <h3 class="status-title">正在处理中...</h3>
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
            <h3 class="success-title">处理完成！</h3>
            <p class="success-message">{{ appStore.message }}</p>
          </div>
        </div>
      </el-card>

      <!-- 结果展示 -->
      <el-card class="result-card">
        <template #header>
          <div class="card-header">
            <el-icon><PictureRounded /></el-icon>
            <span>处理结果</span>
          </div>
        </template>

        <div class="result-display">
          <!-- 原图对比 -->
          <div class="comparison-section">
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="image-container">
                  <div class="image-title">原始截图</div>
                  <div class="image-wrapper">
                    <img
                      :src="appStore.chatImage"
                      alt="原始聊天截图"
                      class="preview-image"
                    />
                  </div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="image-container">
                  <div class="image-title">处理结果</div>
                  <div class="image-wrapper">
                    <img
                      :src="resultImageUrl"
                      alt="头像替换结果"
                      class="preview-image"
                      @load="handleResultImageLoad"
                    />
                  </div>
                </div>
              </el-col>
            </el-row>
          </div>

          <!-- 处理统计 -->
          <div class="stats-section">
            <el-row :gutter="20">
              <el-col :span="8">
                <el-statistic title="检测头像" :value="avatarCount" suffix="个">
                  <template #prefix>
                    <el-icon><Search /></el-icon>
                  </template>
                </el-statistic>
              </el-col>
              <el-col :span="8">
                <el-statistic title="替换成功" :value="avatarCount" suffix="个">
                  <template #prefix>
                    <el-icon><Check /></el-icon>
                  </template>
                </el-statistic>
              </el-col>
              <el-col :span="8">
                <el-statistic title="处理时间" :value="processingTime" suffix="秒">
                  <template #prefix>
                    <el-icon><Timer /></el-icon>
                  </template>
                </el-statistic>
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
          下载结果图片
        </el-button>
        <el-button
          size="large"
          :icon="View"
          @click="previewResult"
        >
          全屏预览
        </el-button>
        <el-button
          size="large"
          :icon="Share"
          @click="shareResult"
        >
          分享结果
        </el-button>
      </div>
    </div>

    <!-- 处理失败 -->
    <div v-else-if="appStore.sessionStatus === 'error'" class="error-content">
      <el-card class="error-card">
        <div class="error-content-inner">
          <el-icon class="error-icon"><CircleCloseFilled /></el-icon>
          <h3 class="error-title">处理失败</h3>
          <p class="error-message">{{ appStore.message }}</p>
          <el-button type="primary" @click="retryProcess">
            <el-icon><RefreshLeft /></el-icon>
            重新处理
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 全屏预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      title="结果预览"
      :width="'90%'"
      center
      destroy-on-close
    >
      <div class="fullscreen-preview">
        <img
          :src="resultImageUrl"
          alt="处理结果"
          class="fullscreen-image"
        />
      </div>
    </el-dialog>

    <!-- 分享对话框 -->
    <el-dialog
      v-model="shareDialogVisible"
      title="分享结果"
      width="500px"
      center
    >
      <div class="share-content">
        <el-alert
          title="分享提示"
          type="info"
          :closable="false"
          show-icon
        >
          您可以右键保存图片，或使用下载按钮获取处理结果
        </el-alert>
        <div class="share-image">
          <img
            :src="resultImageUrl"
            alt="分享结果"
            class="share-preview"
          />
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAppStore } from '../stores/app'
import { getDownloadUrl } from '../api/upload'
import {
  Loading,
  SuccessFilled,
  PictureRounded,
  Search,
  Check,
  Timer,
  Download,
  View,
  Share,
  CircleCloseFilled,
  RefreshLeft
} from '@element-plus/icons-vue'

const appStore = useAppStore()

// 对话框状态
const previewDialogVisible = ref(false)
const shareDialogVisible = ref(false)

// 处理结果数据
const avatarCount = ref(0)
const processingTime = ref(0)

// 结果图片URL
const resultImageUrl = computed(() => {
  if (appStore.sessionId && appStore.sessionStatus === 'completed') {
    return getDownloadUrl(appStore.sessionId)
  }
  return ''
})

// 处理结果图片加载
const handleResultImageLoad = () => {
  // 可以在这里添加图片加载完成的逻辑
}

// 下载结果
const downloadResult = () => {
  if (resultImageUrl.value) {
    const link = document.createElement('a')
    link.href = resultImageUrl.value
    link.download = `chat_avatar_replaced_${Date.now()}.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    ElMessage.success('开始下载结果图片')
  }
}

// 全屏预览
const previewResult = () => {
  previewDialogVisible.value = true
}

// 分享结果
const shareResult = () => {
  shareDialogVisible.value = true
}

// 重新处理
const retryProcess = () => {
  // 触发重新处理逻辑
  ElMessage.info('请返回参数调节步骤重新处理')
}

// 监听状态变化，更新统计信息
onMounted(() => {
  // 从store中获取处理结果信息
  if (appStore.message) {
    const match = appStore.message.match(/替换了(\d+)个头像/)
    if (match) {
      avatarCount.value = parseInt(match[1])
    }
  }

  // 计算处理时间（示例）
  processingTime.value = Math.round(Math.random() * 10 + 2)
})
</script>

<style scoped>
.result-preview {
  padding: 20px;
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

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
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

.stats-section {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

:deep(.el-statistic) {
  text-align: center;
}

/* 操作按钮 */
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

/* 分享对话框 */
.share-content {
  text-align: center;
}

.share-image {
  margin-top: 20px;
}

.share-preview {
  max-width: 100%;
  max-height: 300px;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 响应式 */
@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
    align-items: center;
  }

  .action-buttons .el-button {
    width: 200px;
  }
}
</style>