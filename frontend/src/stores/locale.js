import { defineStore } from 'pinia'
import { ref } from 'vue'
import { setLocale, getCurrentLocale, getAvailableLocales } from '../locales/index.js'

export const useLocaleStore = defineStore('locale', () => {
  // 当前语言
  const currentLocale = ref(getCurrentLocale())

  // 可用语言列表
  const availableLocales = getAvailableLocales()

  // 语言选项配置
  const localeOptions = [
    {
      value: 'en',
      label: 'English',
      icon: '🇺🇸'
    },
    {
      value: 'zh',
      label: '中文',
      icon: '🇨🇳'
    }
  ]

  // 切换语言
  function switchLocale(locale) {
    if (setLocale(locale)) {
      currentLocale.value = locale
      return true
    }
    return false
  }

  // 获取当前语言选项
  function getCurrentLocaleOption() {
    return localeOptions.find(option => option.value === currentLocale.value)
  }

  // 获取其他语言选项（用于切换）
  function getOtherLocaleOptions() {
    return localeOptions.filter(option => option.value !== currentLocale.value)
  }

  // 是否为中文
  function isZh() {
    return currentLocale.value === 'zh'
  }

  // 是否为英文
  function isEn() {
    return currentLocale.value === 'en'
  }

  return {
    currentLocale,
    availableLocales,
    localeOptions,
    switchLocale,
    getCurrentLocaleOption,
    getOtherLocaleOptions,
    isZh,
    isEn
  }
})