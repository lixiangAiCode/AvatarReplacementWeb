export default {
  // Header
  header: {
    title: 'Avatar Replacement Online',
    subtitle: 'Intelligent batch avatar replacement based on template matching'
  },

  // Navigation & Common
  common: {
    next: 'Next',
    previous: 'Previous',
    cancel: 'Cancel',
    confirm: 'Confirm',
    submit: 'Submit',
    reset: 'Reset',
    close: 'Close',
    save: 'Save',
    delete: 'Delete',
    edit: 'Edit',
    view: 'View',
    download: 'Download',
    upload: 'Upload',
    loading: 'Loading...',
    success: 'Success',
    error: 'Error',
    warning: 'Warning',
    info: 'Info'
  },

  // Upload Components
  upload: {
    chatImage: 'Upload Chat Screenshot',
    chatImageTip: 'Upload a chat screenshot for avatar replacement',
    avatar: 'Upload New Avatar',
    avatarTip: 'Upload the new avatar image to replace with',
    dragTip: 'Drop files here, or click to select',
    dragTipActive: 'Drop files here',
    fileTypeError: 'Please upload image files only',
    fileSizeError: 'File size cannot exceed {size}MB',
    uploadSuccess: 'Upload successful',
    uploadError: 'Upload failed',
    selectFile: 'Select File'
  },

  // Template Selector
  template: {
    title: 'Select Avatar Template',
    instruction: 'Click and drag to select the avatar area you want to replace',
    selectedArea: 'Selected Area',
    coordinates: 'Coordinates',
    width: 'Width',
    height: 'Height',
    clearSelection: 'Clear Selection',
    confirmSelection: 'Confirm Selection'
  },

  // Processing & Results
  process: {
    title: 'Processing',
    detecting: 'Detecting similar avatars...',
    replacing: 'Replacing avatars...',
    finishing: 'Finalizing results...',
    completed: 'Processing completed',
    failed: 'Processing failed',
    progress: 'Progress: {percent}%',
    avatarsFound: 'Found {count} similar avatars',
    avatarsReplaced: 'Replaced {count} avatars',
    startProcessing: 'Start Processing',
    viewResult: 'View Result',
    downloadResult: 'Download Result'
  },

  // Parameters
  parameters: {
    title: 'Processing Parameters',
    threshold: 'Match Threshold',
    thresholdTip: 'Higher values require closer matches',
    rightRatio: 'Right Side Filter',
    rightRatioTip: 'Filter chat bubbles based on screen position',
    presets: 'Presets',
    custom: 'Custom',
    high: 'High Precision',
    medium: 'Medium Precision',
    low: 'Low Precision'
  },

  // Results
  results: {
    title: 'Results',
    original: 'Original Image',
    processed: 'Processed Image',
    comparison: 'Comparison View',
    statistics: 'Statistics',
    totalAvatars: 'Total Avatars Found',
    replacedAvatars: 'Successfully Replaced',
    processingTime: 'Processing Time',
    downloadOriginal: 'Download Original',
    downloadProcessed: 'Download Result',
    newProcessing: 'New Processing'
  },

  // Steps
  steps: {
    step1: 'Upload Images',
    step2: 'Select Template',
    step3: 'Set Parameters',
    step4: 'Process & Download',
    uploadImages: 'Upload chat screenshot and new avatar',
    selectTemplate: 'Select the avatar area to replace',
    setParameters: 'Configure processing parameters',
    processDownload: 'Start processing and download results'
  },

  // Error Messages
  errors: {
    sessionNotFound: 'Session not found',
    fileUploadFailed: 'File upload failed',
    processingFailed: 'Processing failed',
    networkError: 'Network error',
    invalidFileType: 'Invalid file type',
    fileTooLarge: 'File too large',
    noTemplateSelected: 'No similar avatars detected, please reselect template',
    missingFiles: 'No image available for download',
    unexpectedError: 'An unexpected error occurred'
  },

  // Footer
  footer: {
    copyright: '© 2025 Avatar Replacement Online',
    privacyPolicy: 'Privacy Policy'
  },

  // Privacy Policy Page
  privacy: {
    title: 'Privacy Policy',
    lastUpdated: 'Last updated: {date}',
    sections: {
      introduction: 'Introduction',
      informationCollection: 'Information We Collect',
      informationProvided: 'Information You Provide',
      automaticCollection: 'Automatically Collected Information',
      informationUse: 'How We Use Your Information',
      dataStorage: 'Data Storage and Security',
      thirdPartyServices: 'Third-Party Services',
      cookiesTracking: 'Cookies and Tracking',
      userRights: 'Your Rights',
      childrenPrivacy: "Children's Privacy",
      policyChanges: 'Changes to This Policy',
      contactUs: 'Contact Us'
    }
  },

  // Language Switcher
  language: {
    english: 'English',
    chinese: 'Chinese',
    switchTo: 'Switch to {lang}'
  }
}