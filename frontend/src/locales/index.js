import { createI18n } from 'vue-i18n'
import en from './en.js'
import zh from './zh.js'

// 默认语言
const DEFAULT_LOCALE = 'en'

// 从localStorage获取保存的语言设置，如果没有则使用默认语言
function getStoredLocale() {
  const stored = localStorage.getItem('avatar-replacement-locale')
  return stored || DEFAULT_LOCALE
}

// 创建i18n实例
const i18n = createI18n({
  legacy: false, // 使用 Composition API 模式
  locale: getStoredLocale(), // 设置默认语言
  fallbackLocale: DEFAULT_LOCALE, // 设置备用语言
  messages: {
    en,
    zh
  }
})

// 保存语言设置到localStorage
export function setLocale(locale) {
  if (i18n.global.availableLocales.includes(locale)) {
    i18n.global.locale.value = locale
    localStorage.setItem('avatar-replacement-locale', locale)
    return true
  }
  return false
}

// 获取当前语言
export function getCurrentLocale() {
  return i18n.global.locale.value
}

// 获取可用语言列表
export function getAvailableLocales() {
  return i18n.global.availableLocales
}

export default i18n