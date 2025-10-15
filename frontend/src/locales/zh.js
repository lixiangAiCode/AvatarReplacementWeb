export default {
  // Header
  header: {
    title: '聊天头像替换工具',
    subtitle: '基于模板匹配的智能头像批量替换'
  },

  // Navigation & Common
  common: {
    next: '下一步',
    previous: '上一步',
    cancel: '取消',
    confirm: '确认',
    submit: '提交',
    reset: '重置',
    close: '关闭',
    save: '保存',
    delete: '删除',
    edit: '编辑',
    view: '查看',
    download: '下载',
    upload: '上传',
    loading: '加载中...',
    success: '成功',
    error: '错误',
    warning: '警告',
    info: '信息'
  },

  // Upload Components
  upload: {
    chatImage: '上传聊天截图',
    chatImageTip: '上传需要进行头像替换的聊天截图',
    avatar: '上传新头像',
    avatarTip: '上传要替换成的新头像图片',
    dragTip: '拖拽文件到此处，或点击选择文件',
    dragTipActive: '释放文件到此处',
    fileTypeError: '请只上传图片文件',
    fileSizeError: '文件大小不能超过 {size}MB',
    uploadSuccess: '上传成功',
    uploadError: '上传失败',
    selectFile: '选择文件'
  },

  // Template Selector
  template: {
    title: '选择头像模板',
    instruction: '点击并拖拽选择要替换的头像区域',
    selectedArea: '选中区域',
    coordinates: '坐标',
    width: '宽度',
    height: '高度',
    clearSelection: '清除选择',
    confirmSelection: '确认选择'
  },

  // Processing & Results
  process: {
    title: '处理中',
    detecting: '正在检测相似头像...',
    replacing: '正在替换头像...',
    finishing: '正在完成处理...',
    completed: '处理完成',
    failed: '处理失败',
    progress: '进度：{percent}%',
    avatarsFound: '找到 {count} 个相似头像',
    avatarsReplaced: '已替换 {count} 个头像',
    startProcessing: '开始处理',
    viewResult: '查看结果',
    downloadResult: '下载结果'
  },

  // Parameters
  parameters: {
    title: '处理参数',
    threshold: '匹配阈值',
    thresholdTip: '数值越高要求匹配度越高',
    rightRatio: '右侧筛选',
    rightRatioTip: '根据屏幕位置筛选聊天气泡',
    presets: '预设配置',
    custom: '自定义',
    high: '高精度',
    medium: '中等精度',
    low: '低精度'
  },

  // Results
  results: {
    title: '处理结果',
    original: '原始图片',
    processed: '处理后图片',
    comparison: '对比视图',
    statistics: '统计信息',
    totalAvatars: '找到头像总数',
    replacedAvatars: '成功替换数量',
    processingTime: '处理时间',
    downloadOriginal: '下载原图',
    downloadProcessed: '下载结果',
    newProcessing: '新建处理'
  },

  // Steps
  steps: {
    step1: '上传图片',
    step2: '选择模板',
    step3: '设置参数',
    step4: '处理下载',
    uploadImages: '上传聊天截图和新头像',
    selectTemplate: '选择要替换的头像区域',
    setParameters: '配置处理参数',
    processDownload: '开始处理并下载结果'
  },

  // Error Messages
  errors: {
    sessionNotFound: '会话不存在',
    fileUploadFailed: '文件上传失败',
    processingFailed: '处理失败',
    networkError: '网络错误',
    invalidFileType: '无效的文件类型',
    fileTooLarge: '文件过大',
    noTemplateSelected: '未检测到相似头像，请重新选择模板',
    missingFiles: '没有可下载的图片',
    unexpectedError: '发生意外错误'
  },

  // Footer
  footer: {
    copyright: '© 2025 聊天头像替换在线工具',
    privacyPolicy: '隐私政策'
  },

  // Privacy Policy Page
  privacy: {
    title: '隐私政策',
    lastUpdated: '最后更新时间：{date}',
    sections: {
      introduction: '简介',
      informationCollection: '我们收集的信息',
      informationProvided: '您提供的信息',
      automaticCollection: '自动收集的信息',
      informationUse: '我们如何使用您的信息',
      dataStorage: '数据存储和安全',
      thirdPartyServices: '第三方服务',
      cookiesTracking: 'Cookies和跟踪',
      userRights: '您的权利',
      childrenPrivacy: '儿童隐私',
      policyChanges: '政策变更',
      contactUs: '联系我们'
    }
  },

  // Language Switcher
  language: {
    english: 'English',
    chinese: '中文',
    switchTo: '切换到{lang}'
  }
}