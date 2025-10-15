<template>
  <div class="avatar-replace">
    <!-- 步骤导航 -->
    <el-card class="step-card">
      <el-steps :active="getCurrentStepIndex()" finish-status="success" align-center>
        <el-step :title="$t('steps.step1')" icon="Upload" />
        <el-step :title="$t('steps.step2')" icon="Crop" />
        <el-step :title="getStepTitle()" icon="SuccessFilled" />
      </el-steps>
    </el-card>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 步骤1: 图片上传 -->
      <el-card v-show="currentStep === 0" class="content-card">
        <template #header>
          <div class="card-header">
            <el-icon><Upload /></el-icon>
            <span>{{ $t('steps.uploadImages') }}</span>
          </div>
        </template>
        <ImageUpload @uploaded="handleImageUploaded" />
      </el-card>

      <!-- 步骤2: 模板选择 -->
      <el-card v-show="currentStep === 1" class="content-card">
        <template #header>
          <div class="card-header">
            <el-icon><Crop /></el-icon>
            <span>{{ $t('steps.selectTemplate') }}</span>
          </div>
        </template>
        <TemplateSelector
          v-if="appStore.chatImage"
          :chat-image="appStore.chatImage"
          @template-selected="handleTemplateSelected"
          @processing-complete="handleProcessingComplete"
        />
      </el-card>

      <!-- 步骤3: 确认替换 -->
      <el-card v-show="currentStep === 2" class="content-card">
        <template #header>
          <div class="card-header">
            <el-icon><SuccessFilled /></el-icon>
            <span>{{ getStepTitle() }}</span>
          </div>
        </template>
        <ResultPreview @confirm-replace="handleConfirmReplace" />
      </el-card>
    </div>

    <!-- 控制按钮 -->
    <div class="control-buttons">
      <el-button
        v-if="currentStep > 0"
        @click="prevStep"
        :icon="ArrowLeft"
      >
        {{ $t('common.previous') }}
      </el-button>

      <el-button
        v-if="currentStep < 2 && canNextStep"
        type="primary"
        @click="nextStep"
        :icon="ArrowRight"
      >
        {{ $t('common.next') }}
      </el-button>

      <el-button
        v-if="currentStep === 2 && appStore.sessionStatus !== 'completed'"
        type="success"
        @click="resetProcess"
        :icon="RefreshLeft"
      >
        {{ $t('common.reset') }}
      </el-button>
      
      <el-button
        v-if="appStore.sessionStatus === 'completed'"
        type="primary"
        @click="resetProcess"
        :icon="RefreshLeft"
      >
        {{ $t('results.newProcessing') }}
      </el-button>
    </div>

    <!-- 状态显示 -->
    <el-card v-if="appStore.sessionStatus !== 'idle'" class="status-card">
      <div class="status-content">
        <div class="status-text">
          <span>{{ getStatusMessage() }}</span>
        </div>
        <el-progress
          v-if="appStore.progress > 0"
          :percentage="appStore.progress"
          :status="appStore.sessionStatus === 'completed' ? 'success' : undefined"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { useAppStore } from '../stores/app'
import {
  Upload,
  Crop,
  Setting,
  SuccessFilled,
  ArrowLeft,
  ArrowRight,
  RefreshLeft
} from '@element-plus/icons-vue'

// 引入组件
import ImageUpload from '../components/ImageUpload.vue'
import TemplateSelector from '../components/TemplateSelector.vue'
import ResultPreview from '../components/ResultPreview.vue'

const { t } = useI18n()
const appStore = useAppStore()
const currentStep = ref(0)

// 判断是否可以进入下一步
const canNextStep = computed(() => {
  switch (currentStep.value) {
    case 0:
      return appStore.chatImage && appStore.newAvatar
    case 1:
      return appStore.detectedAvatars && appStore.detectedAvatars.length > 0
    default:
      return false
  }
})

// 处理图片上传完成
const handleImageUploaded = () => {
  ElMessage.success(t('upload.uploadSuccess'))
}

// 处理模板选择完成
const handleTemplateSelected = () => {
  ElMessage.success(t('process.detecting'))
}

// 处理检测完成
const handleProcessingComplete = (detectedAvatars) => {
  appStore.detectedAvatars = detectedAvatars
  currentStep.value = 2
  ElMessage.success(t('process.avatarsFound', { count: detectedAvatars.length }))
}

// 处理确认替换
const handleConfirmReplace = async () => {
  // ResultPreview组件会处理替换逻辑并更新store状态
  // 当替换完成或失败时，确保页面保持在步骤3显示结果
  
  // 确保当前步骤为第3步（显示结果页面）
  currentStep.value = 2
  
  // 如果处理完成，页面会自动显示替换后的图片
  // 如果处理失败，页面会显示错误信息
}

// 获取步骤标题
const getStepTitle = () => {
  if (appStore.sessionStatus === 'completed') {
    return t('process.completed')
  } else if (appStore.sessionStatus === 'processing') {
    return t('process.title')
  } else if (appStore.sessionStatus === 'error') {
    return t('process.failed')
  } else {
    return t('steps.processDownload')
  }
}

// 获取状态消息
const getStatusMessage = () => {
  if (appStore.sessionStatus === 'processing') {
    if (appStore.progress < 30) {
      return t('process.detecting')
    } else if (appStore.progress < 80) {
      return t('process.replacing')
    } else {
      return t('process.finishing')
    }
  } else if (appStore.sessionStatus === 'completed') {
    return t('process.completed')
  } else if (appStore.sessionStatus === 'error') {
    return t('errors.processingFailed')
  } else {
    return appStore.message || ''
  }
}

// 获取当前步骤索引（用于步骤导航显示）
const getCurrentStepIndex = () => {
  if (appStore.sessionStatus === 'completed') {
    return 3 // 显示为已完成的最后一步
  } else if (appStore.sessionStatus === 'processing') {
    return 2 // 显示为正在进行的第三步
  } else {
    return currentStep.value
  }
}

// 下一步
const nextStep = () => {
  if (canNextStep.value && currentStep.value < 2) {
    currentStep.value++
  }
}

// 上一步
const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// 重新开始
const resetProcess = () => {
  appStore.resetState()
  currentStep.value = 0
  appStore.initSession()
}

// 初始化
onMounted(async () => {
  await appStore.initSession()
})
</script>

<style scoped>
.avatar-replace {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.step-card {
  margin-bottom: 30px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: none;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.main-content {
  min-height: 400px;
  margin-bottom: 20px;
}

.content-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
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

.control-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 20px;
}

.status-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: none;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.status-content {
  text-align: center;
}

.status-text {
  margin-bottom: 16px;
  font-size: 14px;
  color: #606266;
}
</style>