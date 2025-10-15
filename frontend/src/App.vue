<template>
  <div id="app">
    <el-container class="app-container">
      <!-- 顶部导航 -->
      <el-header class="app-header">
        <div class="header-content">
          <h1 class="title">
            <el-icon><Avatar /></el-icon>
            聊天头像替换工具
          </h1>
          <div class="subtitle">基于模板匹配的智能头像批量替换</div>
        </div>
      </el-header>

      <!-- 主内容区 -->
      <el-main class="app-main">
        <router-view />
      </el-main>

      <!-- 底部信息 -->
      <el-footer class="app-footer">
        <div class="footer-content">
          <span>© 2025 Avatar Replacement Online | </span>
          <router-link to="/privacy-policy" class="privacy-link">Privacy Policy</router-link>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { Avatar } from '@element-plus/icons-vue'
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.app-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.header-content {
  text-align: center;
  width: 100%;
}

.title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-size: 28px;
  font-weight: 600;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.subtitle {
  font-size: 14px;
  opacity: 0.9;
  margin-top: 4px;
}

.app-main {
  padding: 20px;
  flex: 1;
}

.app-footer {
  background: rgba(0, 0, 0, 0.1);
  color: white;
  text-align: center;
  padding: 10px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-content {
  font-size: 12px;
  opacity: 0.7;
}

.privacy-link {
  color: white;
  text-decoration: none;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.privacy-link:hover {
  opacity: 1;
  text-decoration: underline;
}

/* 全局样式 */
:global(body) {
  margin: 0;
  font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}

:global(#app) {
  width: 100%;
  min-height: 100vh;
}
</style>