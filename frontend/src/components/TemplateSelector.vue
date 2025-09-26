<template>
  <div class="template-selector">
    <div class="selector-header">
      <h4>请在聊天截图中框选一个头像作为模板</h4>
      <div class="controls">
        <el-button-group>
          <el-button :icon="ZoomIn" @click="zoomIn" size="small">放大</el-button>
          <el-button :icon="ZoomOut" @click="zoomOut" size="small">缩小</el-button>
          <el-button :icon="RefreshLeft" @click="resetView" size="small">重置</el-button>
        </el-button-group>
      </div>
    </div>

    <div class="canvas-container">
      <div
        ref="canvasContainer"
        class="canvas-wrapper"
        @mousedown="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="handleMouseUp"
        @wheel="handleWheel"
      >
        <canvas
          ref="canvas"
          class="selection-canvas"
          :width="canvasSize.width"
          :height="canvasSize.height"
        ></canvas>
      </div>
    </div>

    <div class="selector-footer">
      <div v-if="selection.isSelected" class="selection-info">
        <span>选中区域: {{ selection.width }} × {{ selection.height }} px</span>
      </div>
      <div class="footer-buttons">
        <el-button @click="clearSelection" :disabled="!selection.isSelected">
          <el-icon><Delete /></el-icon>
          清除选择
        </el-button>
        <el-button
          type="primary"
          @click="confirmSelection"
          :disabled="!selection.isSelected"
          :loading="processing"
        >
          <el-icon><Check /></el-icon>
          {{ processing ? '检测中...' : '确认模板' }}
        </el-button>
      </div>
    </div>

    <div class="usage-tips">
      <el-alert type="info" :closable="false">
        <template #title>
          <div class="tips-title">操作说明</div>
        </template>
        <ul class="tips-list">
          <li><strong>框选模板：</strong> 鼠标左键拖拽框选头像区域</li>
          <li><strong>缩放图片：</strong> 滚轮上下滚动或使用缩放按钮</li>
          <li><strong>移动图片：</strong> 右键拖拽移动图片位置</li>
          <li><strong>建议：</strong> 选择清晰完整的头像，避免包含过多背景</li>
        </ul>
      </el-alert>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { useAppStore } from '../stores/app'
import { setTemplate } from '../api/upload'
import {
  ZoomIn,
  ZoomOut,
  RefreshLeft,
  Delete,
  Check
} from '@element-plus/icons-vue'

const props = defineProps({
  chatImage: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['template-selected', 'processing-complete'])
const appStore = useAppStore()

// 处理状态
const processing = ref(false)

// DOM引用
const canvas = ref(null)
const canvasContainer = ref(null)

// Canvas状态
const canvasSize = reactive({
  width: 800,
  height: 600
})

// 图片状态
const image = reactive({
  element: null,
  loaded: false,
  scale: 1,
  offsetX: 0,
  offsetY: 0,
  originalWidth: 0,
  originalHeight: 0
})

// 选择框状态
const selection = reactive({
  isSelecting: false,
  isSelected: false,
  startX: 0,
  startY: 0,
  endX: 0,
  endY: 0,
  width: 0,
  height: 0
})

// 鼠标状态
const mouse = reactive({
  isDown: false,
  isDragging: false,
  button: 0,
  startX: 0,
  startY: 0,
  lastX: 0,
  lastY: 0
})

// 初始化
onMounted(async () => {
  await loadImage()
  setupCanvas()
})

// 加载图片
const loadImage = () => {
  return new Promise((resolve) => {
    const img = new Image()
    img.onload = () => {
      image.element = img
      image.loaded = true
      image.originalWidth = img.width
      image.originalHeight = img.height

      // 计算初始缩放和居中
      const containerWidth = canvasSize.width
      const containerHeight = canvasSize.height
      const scaleX = containerWidth / img.width
      const scaleY = containerHeight / img.height
      image.scale = Math.min(scaleX, scaleY) * 0.8

      image.offsetX = (containerWidth - img.width * image.scale) / 2
      image.offsetY = (containerHeight - img.height * image.scale) / 2

      resolve()
    }
    img.src = props.chatImage
  })
}

// 设置Canvas
const setupCanvas = () => {
  nextTick(() => {
    drawCanvas()
  })
}

// 绘制Canvas
const drawCanvas = () => {
  if (!canvas.value || !image.loaded) return

  const ctx = canvas.value.getContext('2d')
  ctx.clearRect(0, 0, canvasSize.width, canvasSize.height)

  // 绘制图片
  ctx.drawImage(
    image.element,
    image.offsetX,
    image.offsetY,
    image.originalWidth * image.scale,
    image.originalHeight * image.scale
  )

  // 绘制选择框
  if (selection.isSelecting || selection.isSelected) {
    ctx.strokeStyle = '#409EFF'
    ctx.lineWidth = 2
    ctx.setLineDash([5, 5])
    ctx.strokeRect(
      selection.startX,
      selection.startY,
      selection.endX - selection.startX,
      selection.endY - selection.startY
    )

    // 绘制选择框背景
    ctx.fillStyle = 'rgba(64, 158, 255, 0.1)'
    ctx.fillRect(
      selection.startX,
      selection.startY,
      selection.endX - selection.startX,
      selection.endY - selection.startY
    )
  }
}

// 鼠标事件处理
const handleMouseDown = (e) => {
  const rect = canvas.value.getBoundingClientRect()
  mouse.isDown = true
  mouse.button = e.button
  mouse.startX = e.clientX - rect.left
  mouse.startY = e.clientY - rect.top
  mouse.lastX = mouse.startX
  mouse.lastY = mouse.startY

  if (e.button === 0) {
    // 左键 - 开始选择
    selection.isSelecting = true
    selection.isSelected = false
    selection.startX = mouse.startX
    selection.startY = mouse.startY
    selection.endX = mouse.startX
    selection.endY = mouse.startY
  }
}

const handleMouseMove = (e) => {
  if (!mouse.isDown) return

  const rect = canvas.value.getBoundingClientRect()
  const currentX = e.clientX - rect.left
  const currentY = e.clientY - rect.top

  if (mouse.button === 0 && selection.isSelecting) {
    // 左键拖拽 - 更新选择框
    selection.endX = currentX
    selection.endY = currentY
    drawCanvas()
  } else if (mouse.button === 2) {
    // 右键拖拽 - 移动图片
    const deltaX = currentX - mouse.lastX
    const deltaY = currentY - mouse.lastY
    image.offsetX += deltaX
    image.offsetY += deltaY
    mouse.lastX = currentX
    mouse.lastY = currentY
    drawCanvas()
  }
}

const handleMouseUp = (e) => {
  if (mouse.button === 0 && selection.isSelecting) {
    // 完成选择
    selection.isSelecting = false
    selection.isSelected = true
    selection.width = Math.abs(selection.endX - selection.startX)
    selection.height = Math.abs(selection.endY - selection.startY)

    // 确保选择框是正方向的
    if (selection.endX < selection.startX) {
      [selection.startX, selection.endX] = [selection.endX, selection.startX]
    }
    if (selection.endY < selection.startY) {
      [selection.startY, selection.endY] = [selection.endY, selection.startY]
    }
  }

  mouse.isDown = false
  mouse.isDragging = false
}

// 滚轮缩放
const handleWheel = (e) => {
  e.preventDefault()
  const delta = e.deltaY > 0 ? 0.9 : 1.1
  const rect = canvas.value.getBoundingClientRect()
  const mouseX = e.clientX - rect.left
  const mouseY = e.clientY - rect.top

  // 以鼠标位置为中心缩放
  const beforeScale = image.scale
  image.scale = Math.max(0.1, Math.min(5, image.scale * delta))
  const scaleChange = image.scale / beforeScale

  image.offsetX = mouseX - (mouseX - image.offsetX) * scaleChange
  image.offsetY = mouseY - (mouseY - image.offsetY) * scaleChange

  drawCanvas()
}

// 缩放控制
const zoomIn = () => {
  image.scale = Math.min(5, image.scale * 1.2)
  drawCanvas()
}

const zoomOut = () => {
  image.scale = Math.max(0.1, image.scale / 1.2)
  drawCanvas()
}

const resetView = () => {
  const containerWidth = canvasSize.width
  const containerHeight = canvasSize.height
  const scaleX = containerWidth / image.originalWidth
  const scaleY = containerHeight / image.originalHeight
  image.scale = Math.min(scaleX, scaleY) * 0.8

  image.offsetX = (containerWidth - image.originalWidth * image.scale) / 2
  image.offsetY = (containerHeight - image.originalHeight * image.scale) / 2

  drawCanvas()
}

// 清除选择
const clearSelection = () => {
  selection.isSelected = false
  selection.isSelecting = false
  drawCanvas()
}

// 确认选择
const confirmSelection = async () => {
  if (!selection.isSelected || processing.value) return

  processing.value = true

  // 将Canvas坐标转换为原图坐标
  const realX = Math.round((selection.startX - image.offsetX) / image.scale)
  const realY = Math.round((selection.startY - image.offsetY) / image.scale)
  const realWidth = Math.round(selection.width / image.scale)
  const realHeight = Math.round(selection.height / image.scale)

  // 边界检查
  const bbox = {
    x: Math.max(0, realX),
    y: Math.max(0, realY),
    width: Math.min(realWidth, image.originalWidth - realX),
    height: Math.min(realHeight, image.originalHeight - realY)
  }

  try {
    console.log(appStore.sessionId)
    // 设置模板区域并进行检测（后端会自动进行检测）
    const response = await setTemplate(appStore.sessionId, bbox)
    console.log(response)
    appStore.templateBbox = bbox
    emit('template-selected')
    // 处理检测结果
    if (response.avatar_count > 0) {
      // 将检测结果和预览图保存到store
      appStore.detectedAvatars = response.detected_avatars
      appStore.previewImage = response.preview_image
      
      ElMessage.success(`检测完成！找到 ${response.detected_avatars.length} 个相似头像`)
      emit('processing-complete', response.detected_avatars)
    } else {
      ElMessage.warning('未检测到相似头像，请重新选择模板')
    }

  } catch (error) {
    ElMessage.error('检测失败: ' + (error.response?.detail || error.message))
  } finally {
    processing.value = false
  }
}

// 禁用右键菜单
onMounted(() => {
  if (canvas.value) {
    canvas.value.addEventListener('contextmenu', (e) => {
      e.preventDefault()
    })
  }
})
</script>

<style scoped>
.template-selector {
  padding: 20px;
}

.selector-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.selector-header h4 {
  margin: 0;
  color: #303133;
  font-size: 16px;
}

.canvas-container {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.canvas-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f5;
  cursor: crosshair;
}

.selection-canvas {
  display: block;
  background: white;
}

.selector-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.selection-info {
  color: #606266;
  font-size: 14px;
}

.footer-buttons {
  display: flex;
  gap: 12px;
}

.usage-tips {
  background: #f8f9fa;
  border-radius: 8px;
}

.tips-title {
  font-weight: 600;
  color: #303133;
}

.tips-list {
  margin: 8px 0 0 0;
  padding-left: 20px;
}

.tips-list li {
  margin-bottom: 6px;
  font-size: 14px;
  color: #606266;
}

.tips-list strong {
  color: #303133;
}
</style>