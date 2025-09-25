# 前端Vue项目

## 启动方式

```bash
cd frontend
npm install
npm run dev
```

访问：http://localhost:3000

## 项目结构

```
frontend/
├── src/
│   ├── components/          # Vue组件
│   │   ├── ImageUpload.vue     # 图片上传组件
│   │   ├── TemplateSelector.vue # Canvas模板选择组件
│   │   ├── ParameterPanel.vue   # 参数调节组件
│   │   └── ResultPreview.vue    # 结果展示组件
│   ├── views/
│   │   └── AvatarReplace.vue   # 主页面
│   ├── stores/
│   │   └── app.js              # Pinia状态管理
│   ├── api/
│   │   ├── request.js          # Axios封装
│   │   ├── session.js          # 会话API
│   │   └── upload.js           # 上传和处理API
│   ├── router/
│   │   └── index.js            # Vue Router配置
│   ├── App.vue                 # 根组件
│   └── main.js                 # 应用入口
├── public/                     # 静态资源
├── index.html                  # HTML模板
├── package.json               # 依赖配置
└── vite.config.js            # Vite配置
```

## 技术栈

- **Vue 3** - 响应式框架
- **Composition API** - 组合式API
- **Pinia** - 状态管理
- **Element Plus** - UI组件库
- **Axios** - HTTP客户端
- **Canvas 2D** - 图像交互
- **Vite** - 构建工具

## 主要功能

1. **步骤式界面** - 引导用户完成操作流程
2. **图片上传** - 支持拖拽上传和预览
3. **Canvas模板选择** - 交互式头像区域框选
4. **参数调节** - 预设配置和自定义参数
5. **实时处理进度** - 显示处理状态和进度
6. **结果展示** - 对比效果和下载功能