<template>
  <div class="parameter-panel">
    <el-row :gutter="20">
      <!-- 参数控制区 -->
      <el-col :span="12">
        <div class="parameter-section">
          <h4 class="section-title">
            <el-icon><Setting /></el-icon>
            处理参数
          </h4>

          <!-- 匹配阈值 -->
          <div class="parameter-item">
            <label class="parameter-label">匹配阈值</label>
            <div class="slider-container">
              <el-slider
                v-model="config.threshold"
                :min="0.5"
                :max="1.0"
                :step="0.05"
                show-input
                :input-size="'small'"
              />
            </div>
            <div class="parameter-desc">
              阈值越高匹配越严格，推荐值：0.8
            </div>
          </div>

          <!-- 右侧筛选比例 -->
          <div class="parameter-item">
            <label class="parameter-label">右侧筛选比例</label>
            <div class="slider-container">
              <el-slider
                v-model="config.right_ratio"
                :min="0.3"
                :max="0.8"
                :step="0.05"
                show-input
                :input-size="'small'"
              />
            </div>
            <div class="parameter-desc">
              只处理图片右侧区域的头像，当前：右侧 {{ Math.round((1 - config.right_ratio) * 100) }}%
            </div>
          </div>
        </div>
      </el-col>

      <!-- 预设配置区 -->
      <el-col :span="12">
        <div class="preset-section">
          <h4 class="section-title">
            <el-icon><Document /></el-icon>
            预设配置
          </h4>

          <div class="preset-buttons">
            <el-button
              v-for="preset in presets"
              :key="preset.name"
              :type="isCurrentPreset(preset) ? 'primary' : 'default'"
              @click="applyPreset(preset)"
              class="preset-btn"
            >
              {{ preset.name }}
            </el-button>
          </div>

          <div class="preset-description">
            <el-alert
              :title="currentPresetDesc"
              type="info"
              :closable="false"
              show-icon
            />
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 处理预览 -->
    <div class="preview-section">
      <h4 class="section-title">
        <el-icon><View /></el-icon>
        预期效果说明
      </h4>
      <el-card class="preview-card">
        <div class="preview-content">
          <div class="preview-item">
            <div class="preview-icon">
              <el-icon><Search /></el-icon>
            </div>
            <div class="preview-text">
              <strong>模板匹配：</strong>
              在聊天截图中查找与选定模板相似的头像（相似度 ≥ {{ (config.threshold * 100).toFixed(0) }}%）
            </div>
          </div>
          <div class="preview-item">
            <div class="preview-icon">
              <el-icon><Filter /></el-icon>
            </div>
            <div class="preview-text">
              <strong>区域筛选：</strong>
              只处理聊天窗口右侧 {{ Math.round((1 - config.right_ratio) * 100) }}% 区域的头像（通常是发送方）
            </div>
          </div>
          <div class="preview-item">
            <div class="preview-icon">
              <el-icon><Refresh /></el-icon>
            </div>
            <div class="preview-text">
              <strong>智能替换：</strong>
              自动调整新头像尺寸，保持圆角效果，无缝融入聊天界面
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 开始处理按钮 -->
    <div class="action-section">
      <el-button
        type="primary"
        size="large"
        :loading="processing"
        @click="startProcess"
        :disabled="!canProcess"
        class="process-btn"
      >
        <el-icon><VideoPlay /></el-icon>
        开始处理
      </el-button>
      <div v-if="!canProcess" class="process-tip">
        请先完成前面的步骤
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useAppStore } from '../stores/app'
import { startProcessing } from '../api/upload'
import {
  Setting,
  Document,
  View,
  Search,
  Filter,
  Refresh,
  VideoPlay
} from '@element-plus/icons-vue'

const emit = defineEmits(['start-process'])
const appStore = useAppStore()

// 处理参数配置
const config = reactive({
  threshold: 0.8,
  right_ratio: 0.6
})

const processing = ref(false)

// 预设配置
const presets = [
  {
    name: '推荐设置',
    threshold: 0.8,
    right_ratio: 0.6,
    desc: '平衡准确性和召回率，适合大多数聊天截图'
  },
  {
    name: '严格匹配',
    threshold: 0.9,
    right_ratio: 0.65,
    desc: '高精度匹配，减少误检但可能漏检相似头像'
  },
  {
    name: '宽松匹配',
    threshold: 0.7,
    right_ratio: 0.55,
    desc: '宽松匹配，检测更多头像但可能有误检'
  },
  {
    name: '全面检测',
    threshold: 0.75,
    right_ratio: 0.5,
    desc: '检测范围更广，适合头像分布不规律的截图'
  }
]

// 当前预设描述
const currentPresetDesc = computed(() => {
  const preset = presets.find(p => isCurrentPreset(p))
  return preset ? preset.desc : '自定义配置'
})

// 判断是否可以开始处理
const canProcess = computed(() => {
  return appStore.sessionId &&
         appStore.chatImage &&
         appStore.newAvatar &&
         appStore.templateBbox
})

// 判断是否是当前预设
const isCurrentPreset = (preset) => {
  return Math.abs(config.threshold - preset.threshold) < 0.01 &&
         Math.abs(config.right_ratio - preset.right_ratio) < 0.01
}

// 应用预设
const applyPreset = (preset) => {
  config.threshold = preset.threshold
  config.right_ratio = preset.right_ratio
  ElMessage.success(`已应用 "${preset.name}" 配置`)
}

// 开始处理
const startProcess = async () => {
  if (!canProcess.value) return

  processing.value = true

  try {
    await startProcessing(appStore.sessionId, {
      threshold: config.threshold,
      right_ratio: config.right_ratio
    })

    emit('start-process')
    ElMessage.success('开始处理头像替换')

  } catch (error) {
    ElMessage.error('启动处理失败')
  } finally {
    processing.value = false
  }
}
</script>

<style scoped>
.parameter-panel {
  padding: 20px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.parameter-section,
.preset-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  height: 100%;
}

.parameter-item {
  margin-bottom: 24px;
}

.parameter-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #303133;
}

.slider-container {
  margin-bottom: 6px;
}

.parameter-desc {
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
}

.preset-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.preset-btn {
  width: 100%;
}

.preset-description {
  margin-top: 16px;
}

.preview-section {
  margin-top: 30px;
}

.preview-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.preview-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.preview-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.preview-icon {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  background: #e1f3ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #409eff;
}

.preview-text {
  flex: 1;
  font-size: 14px;
  line-height: 1.5;
  color: #606266;
}

.preview-text strong {
  color: #303133;
}

.action-section {
  margin-top: 30px;
  text-align: center;
}

.process-btn {
  width: 200px;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
}

.process-tip {
  margin-top: 12px;
  font-size: 14px;
  color: #909399;
}

:deep(.el-slider__input) {
  width: 80px;
}

:deep(.el-alert) {
  padding: 12px 16px;
}

:deep(.el-alert__content) {
  font-size: 13px;
}
</style>