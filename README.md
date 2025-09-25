# 🎭 聊天头像替换工具 - Web版本

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.4+-green.svg)](https://vuejs.org/)
[![Element Plus](https://img.shields.io/badge/Element%20Plus-2.4+-blue.svg)](https://element-plus.org/)

> 一个基于模板匹配的智能头像批量替换工具，支持从聊天记录截图中自动识别并替换头像。

## ✨ 功能特色

- 🖼️ **智能图片上传** - 支持拖拽上传，实时预览
- 🎯 **精准模板选择** - 可视化Canvas框选头像区域
- ⚙️ **灵活参数调节** - 预设配置和自定义参数
- 📊 **实时处理进度** - 动态显示处理状态和进度
- 🎨 **现代化UI设计** - 响应式设计，毛玻璃效果
- 🔄 **步骤式引导** - 清晰的操作流程指导

## 🎬 功能演示

![头像替换流程](docs/images/demo-workflow.gif)

## 🛠️ 技术栈

### 前端技术
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite 5.0
- **UI组件库**: Element Plus 2.4
- **状态管理**: Pinia 2.1
- **HTTP客户端**: Axios 1.6
- **Canvas交互**: Konva.js 9.2
- **图标**: Element Plus Icons

### 后端技术
- **框架**: FastAPI
- **图像处理**: OpenCV
- **异步支持**: Uvicorn
- **会话管理**: 基于UUID的会话系统
- **文件存储**: 本地存储
- **API路由**: 模块化路由设计

## 📁 项目结构

```
头像替换web/
├── frontend/                 # Vue.js 前端应用
│   ├── src/
│   │   ├── components/       # 可复用组件
│   │   │   ├── ImageUpload.vue       # 图片上传组件
│   │   │   ├── TemplateSelector.vue  # Canvas模板选择
│   │   │   ├── ParameterPanel.vue    # 参数调节面板
│   │   │   └── ResultPreview.vue     # 结果展示组件
│   │   ├── views/
│   │   │   └── AvatarReplace.vue     # 主页面
│   │   ├── stores/
│   │   │   └── app.js                # Pinia状态管理
│   │   ├── api/
│   │   │   ├── request.js            # Axios封装
│   │   │   ├── session.js            # 会话管理API
│   │   │   └── upload.js             # 上传处理API
│   │   ├── router/
│   │   │   └── index.js              # Vue Router配置
│   │   ├── App.vue                   # 根组件
│   │   └── main.js                   # 应用入口
│   ├── public/                       # 静态资源
│   ├── index.html                    # HTML模板
│   ├── package.json                  # 前端依赖配置
│   └── vite.config.js               # Vite构建配置
├── backend/                  # FastAPI 后端应用
│   ├── app/
│   │   ├── models.py                 # 数据模型
│   │   ├── session_manager.py       # 会话管理
│   │   └── routers/                  # API路由
│   │       ├── session.py           # 会话相关API
│   │       └── upload.py            # 文件上传API
│   ├── modules/              # 图像处理模块
│   │   ├── avatar_detector.py       # 头像检测算法
│   │   ├── avatar_replacer.py       # 头像替换处理
│   │   ├── right_side_filter.py     # 右侧消息过滤
│   │   └── web_adapter.py           # Web适配器
│   ├── main.py               # FastAPI应用入口
│   └── requirements.txt      # 后端依赖
└── docs/                     # 项目文档
    ├── api.md               # API接口文档
    ├── components.md        # 组件使用文档
    └── deployment.md        # 部署指南
```

## 🚀 快速开始

### 环境要求

**前端环境：**
- Node.js >= 16.0.0
- npm >= 8.0.0 或 yarn >= 1.22.0

**后端环境：**
- Python >= 3.8
- pip >= 21.0
- OpenCV 相关依赖

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/lixiangAiCode/AvatarReplacementWeb.git
   cd AvatarReplacementWeb
   ```

2. **安装后端依赖**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **启动后端服务**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **安装前端依赖**
   ```bash
   cd ../frontend
   npm install
   ```

5. **启动前端开发服务器**
   ```bash
   npm run dev
   ```

6. **访问应用**
   ```
   前端: http://localhost:3000
   后端API: http://localhost:8000
   ```

### 生产构建

**前端构建：**
```bash
cd frontend
npm run build
```

**后端部署：**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

构建产物将生成在 `frontend/dist` 目录中。

## 📖 使用指南

### 1. 上传图片
- 📱 上传聊天记录截图（支持拖拽）
- 👤 上传新的头像图片
- ✅ 等待上传完成确认

### 2. 选择模板
- 🎯 在聊天截图中框选需要替换的头像区域
- 📏 支持多个头像区域选择
- 🔧 可调整选择框的位置和大小

### 3. 参数调节
- ⚙️ 选择预设配置或自定义参数
- 🎨 调整匹配精度、边缘羽化等选项
- 🚀 开始处理任务

### 4. 查看结果
- 📊 实时查看处理进度
- 🖼️ 预览替换效果
- 💾 下载处理后的图片

## 🔧 配置说明

### 开发环境配置

在 `frontend/vite.config.js` 中可以配置：

```javascript
export default defineConfig({
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // 后端API地址
        changeOrigin: true,
      }
    }
  }
})
```

### API 代理配置

前端开发时，API请求会代理到后端服务器：
- 前端: `http://localhost:3000`
- 后端: `http://localhost:8000`

## 🎨 组件说明

### ImageUpload 组件
负责图片上传功能，支持：
- 拖拽上传
- 文件格式验证
- 实时预览
- 上传进度显示

### TemplateSelector 组件
Canvas头像区域选择，功能包括：
- 可视化框选
- 多区域选择
- 精确定位
- 实时反馈

### ParameterPanel 组件
参数配置面板，提供：
- 预设模板
- 自定义参数
- 实时预览
- 参数保存

### ResultPreview 组件
结果展示组件，支持：
- 对比显示
- 下载功能
- 质量评估
- 批量操作

## 📝 API 接口

### 会话管理
- `POST /api/session/create` - 创建新会话
- `GET /api/session/{id}/status` - 获取会话状态

### 文件上传
- `POST /api/upload/chat` - 上传聊天截图
- `POST /api/upload/avatar` - 上传新头像

### 图像处理
- `POST /api/process/start` - 开始处理任务
- `GET /api/process/{id}/result` - 获取处理结果

详细API文档请查看：[API接口文档](docs/api.md)

## 🎯 开发路线图

### 已完成 ✅
- [x] 前端框架搭建
- [x] 基础组件开发
- [x] 状态管理实现
- [x] UI界面设计
- [x] 后端API开发
- [x] 图像处理算法
- [x] 前后端联调
- [x] 会话管理系统
- [x] 文件上传处理
- [x] 头像检测与替换

### 优化中 🚧
- [ ] 性能优化
- [ ] 错误处理完善
- [ ] 用户体验提升

### 计划中 📋
- [ ] 批量处理功能
- [ ] 模板保存/加载
- [ ] 用户偏好设置
- [ ] 多语言支持
- [ ] Docker容器化部署
- [ ] 云存储集成

## 🤝 贡献指南

我们欢迎所有形式的贡献！

1. **Fork** 本项目
2. **创建** 特性分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **打开** Pull Request

### 开发规范

- 使用 ESLint 进行代码检查
- 遵循 Vue 3 组合式API规范
- 提交信息遵循 [Conventional Commits](https://conventionalcommits.org/)
- 确保所有测试通过

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源协议。

## 📞 联系方式

- **项目地址**: [GitHub Repository](https://github.com/lixiangAiCode/AvatarReplacementWeb)
- **问题反馈**: [Issues](https://github.com/lixiangAiCode/AvatarReplacementWeb/issues)
- **功能建议**: [Discussions](https://github.com/lixiangAiCode/AvatarReplacementWeb/discussions)

## 🙏 致谢

感谢以下开源项目：

- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [Element Plus](https://element-plus.org/) - Vue 3组件库
- [Vite](https://vitejs.dev/) - 下一代前端构建工具
- [Konva.js](https://konvajs.org/) - 2D Canvas库

---

<div align="center">
  <p>如果这个项目对你有帮助，请给我们一个 ⭐️</p>
  <p>Made with ❤️ by LixiangAI</p>
</div>
