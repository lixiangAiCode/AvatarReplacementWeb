<template>
  <div class="image-upload">
    <el-row :gutter="20">
      <!-- 聊天截图上传 -->
      <el-col :span="12">
        <div class="upload-section">
          <h3 class="section-title">
            <el-icon><ChatDotRound /></el-icon>
            聊天记录截图
          </h3>
          <el-upload
            ref="chatUploadRef"
            :auto-upload="false"
            :show-file-list="false"
            :on-change="handleChatImageChange"
            accept="image/*"
            drag
          >
            <div v-if="!chatImagePreview" class="upload-placeholder">
              <el-icon class="upload-icon"><Plus /></el-icon>
              <div class="upload-text">点击或拖拽上传聊天截图</div>
              <div class="upload-hint">支持 PNG、JPG、JPEG、BMP 格式</div>
            </div>
            <div v-else class="image-preview">
              <img :src="chatImagePreview" alt="聊天截图预览" />
              <div class="image-overlay">
                <el-button
                  type="danger"
                  size="small"
                  :icon="Delete"
                  @click.stop="removeChatImage"
                  circle
                />
              </div>
            </div>
          </el-upload>
          <el-button
            v-if="chatImageFile && !chatImageUploaded"
            type="primary"
            :loading="uploading.chat"
            @click="uploadChatImage"
            class="upload-btn"
          >
            <el-icon><Upload /></el-icon>
            上传聊天截图
          </el-button>
          <div v-if="chatImageUploaded" class="upload-success">
            <el-icon><SuccessFilled /></el-icon>
            聊天截图上传成功
          </div>
        </div>
      </el-col>

      <!-- 新头像上传 -->
      <el-col :span="12">
        <div class="upload-section">
          <h3 class="section-title">
            <el-icon><Avatar /></el-icon>
            新头像图片
          </h3>
          <el-upload
            ref="avatarUploadRef"
            :auto-upload="false"
            :show-file-list="false"
            :on-change="handleAvatarChange"
            accept="image/*"
            drag
          >
            <div v-if="!avatarPreview" class="upload-placeholder">
              <el-icon class="upload-icon"><Plus /></el-icon>
              <div class="upload-text">点击或拖拽上传新头像</div>
              <div class="upload-hint">建议使用正方形图片</div>
            </div>
            <div v-else class="image-preview">
              <img :src="avatarPreview" alt="新头像预览" />
              <div class="image-overlay">
                <el-button
                  type="danger"
                  size="small"
                  :icon="Delete"
                  @click.stop="removeAvatar"
                  circle
                />
              </div>
            </div>
          </el-upload>
          <el-button
            v-if="avatarFile && !avatarUploaded"
            type="primary"
            :loading="uploading.avatar"
            @click="uploadAvatar"
            class="upload-btn"
          >
            <el-icon><Upload /></el-icon>
            上传新头像
          </el-button>
          <div v-if="avatarUploaded" class="upload-success">
            <el-icon><SuccessFilled /></el-icon>
            新头像上传成功
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 上传提示 -->
    <div class="upload-tips">
      <el-alert
        title="上传提示"
        type="info"
        :closable="false"
        show-icon
      >
        <ul>
          <li>请先上传聊天记录截图，然后上传要替换的新头像</li>
          <li>建议聊天截图清晰完整，头像边界明显</li>
          <li>新头像建议使用正方形图片，系统会自动调整尺寸</li>
          <li>支持的图片格式：PNG、JPG、JPEG、BMP</li>
        </ul>
      </el-alert>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAppStore } from '../stores/app'
import { uploadChatImage as apiUploadChatImage, uploadAvatar as apiUploadAvatar } from '../api/upload'
import {
  ChatDotRound,
  Avatar,
  Plus,
  Upload,
  Delete,
  SuccessFilled
} from '@element-plus/icons-vue'

const emit = defineEmits(['uploaded'])
const appStore = useAppStore()

// 文件和预览状态
const chatImageFile = ref(null)
const chatImagePreview = ref('')
const chatImageUploaded = ref(false)

const avatarFile = ref(null)
const avatarPreview = ref('')
const avatarUploaded = ref(false)

// 上传状态
const uploading = reactive({
  chat: false,
  avatar: false
})

// 处理聊天截图选择
const handleChatImageChange = (file) => {
  chatImageFile.value = file.raw
  chatImageUploaded.value = false

  // 生成预览
  const reader = new FileReader()
  reader.onload = (e) => {
    chatImagePreview.value = e.target.result
  }
  reader.readAsDataURL(file.raw)
}

// 处理新头像选择
const handleAvatarChange = (file) => {
  avatarFile.value = file.raw
  avatarUploaded.value = false

  // 生成预览
  const reader = new FileReader()
  reader.onload = (e) => {
    avatarPreview.value = e.target.result
  }
  reader.readAsDataURL(file.raw)
}

// 上传聊天截图
const uploadChatImage = async () => {
  if (!chatImageFile.value || !appStore.sessionId) return

  uploading.chat = true
  try {
    await apiUploadChatImage(appStore.sessionId, chatImageFile.value)
    chatImageUploaded.value = true
    appStore.chatImage = chatImagePreview.value
    checkUploadComplete()
    ElMessage.success('聊天截图上传成功')
  } catch (error) {
    ElMessage.error('聊天截图上传失败')
  } finally {
    uploading.chat = false
  }
}

// 上传新头像
const uploadAvatar = async () => {
  if (!avatarFile.value || !appStore.sessionId) return

  uploading.avatar = true
  try {
    await apiUploadAvatar(appStore.sessionId, avatarFile.value)
    avatarUploaded.value = true
    appStore.newAvatar = avatarPreview.value
    checkUploadComplete()
    ElMessage.success('新头像上传成功')
  } catch (error) {
    ElMessage.error('新头像上传失败')
  } finally {
    uploading.avatar = false
  }
}

// 检查上传是否完成
const checkUploadComplete = () => {
  if (chatImageUploaded.value && avatarUploaded.value) {
    emit('uploaded')
  }
}

// 删除聊天截图
const removeChatImage = () => {
  chatImageFile.value = null
  chatImagePreview.value = ''
  chatImageUploaded.value = false
  appStore.chatImage = null
}

// 删除新头像
const removeAvatar = () => {
  avatarFile.value = null
  avatarPreview.value = ''
  avatarUploaded.value = false
  appStore.newAvatar = null
}
</script>

<style scoped>
.image-upload {
  padding: 20px;
}

.upload-section {
  text-align: center;
}

.section-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 20px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

:deep(.el-upload) {
  width: 100%;
}

:deep(.el-upload-dragger) {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  border: 2px dashed #d9d9d9;
  background-color: #fafafa;
  transition: all 0.3s ease;
}

:deep(.el-upload-dragger:hover) {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 20px;
}

.upload-icon {
  font-size: 48px;
  color: #c0c4cc;
  margin-bottom: 16px;
}

.upload-text {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.upload-hint {
  font-size: 12px;
  color: #909399;
}

.image-preview {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.image-overlay {
  position: absolute;
  top: 8px;
  right: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-preview:hover .image-overlay {
  opacity: 1;
}

.upload-btn {
  margin-top: 16px;
  width: 120px;
}

.upload-success {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
  color: #67c23a;
  font-size: 14px;
}

.upload-tips {
  margin-top: 30px;
}

.upload-tips ul {
  margin: 0;
  padding-left: 20px;
}

.upload-tips li {
  margin-bottom: 4px;
  font-size: 14px;
}
</style>