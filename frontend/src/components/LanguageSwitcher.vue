<template>
  <div class="language-switcher">
    <el-dropdown trigger="hover" @command="handleLanguageSwitch">
      <span class="language-trigger">
        <el-icon class="language-icon">
          <Operation />
        </el-icon>
        <span class="current-language">{{ getCurrentLanguageLabel() }}</span>
        <el-icon class="dropdown-icon">
          <ArrowDown />
        </el-icon>
      </span>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item
            v-for="option in getOtherLocaleOptions()"
            :key="option.value"
            :command="option.value"
            class="language-option"
          >
            <span class="language-flag">{{ option.icon }}</span>
            <span class="language-label">{{ option.label }}</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script setup>
import { Operation, ArrowDown } from '@element-plus/icons-vue'
import { useLocaleStore } from '../stores/locale.js'
import { useI18n } from 'vue-i18n'

const localeStore = useLocaleStore()
const { t } = useI18n()

// 获取当前语言显示标签
function getCurrentLanguageLabel() {
  const currentOption = localeStore.getCurrentLocaleOption()
  return currentOption ? currentOption.label : 'EN'
}

// 获取其他语言选项
function getOtherLocaleOptions() {
  return localeStore.getOtherLocaleOptions()
}

// 处理语言切换
function handleLanguageSwitch(locale) {
  const success = localeStore.switchLocale(locale)
  if (success) {
    // 可以添加切换成功的提示
    console.log(`Language switched to: ${locale}`)
  }
}
</script>

<style scoped>
.language-switcher {
  display: flex;
  align-items: center;
}

.language-trigger {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  color: white;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.language-trigger:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.language-icon {
  font-size: 16px;
}

.current-language {
  font-size: 14px;
  font-weight: 500;
  user-select: none;
}

.dropdown-icon {
  font-size: 12px;
  transition: transform 0.3s ease;
}

.language-trigger:hover .dropdown-icon {
  transform: rotate(180deg);
}

.language-option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px !important;
}

.language-flag {
  font-size: 16px;
}

.language-label {
  font-size: 14px;
  font-weight: 500;
}

/* 自定义Element Plus下拉菜单样式 */
:deep(.el-dropdown-menu) {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

:deep(.el-dropdown-menu__item) {
  color: #333;
  transition: all 0.3s ease;
}

:deep(.el-dropdown-menu__item:hover) {
  background: rgba(64, 158, 255, 0.1);
  color: #409eff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .language-trigger {
    padding: 6px 10px;
  }

  .current-language {
    font-size: 13px;
  }

  .language-icon {
    font-size: 14px;
  }
}
</style>