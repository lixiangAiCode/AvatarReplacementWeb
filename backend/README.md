# FastAPI后端应用

## 启动方式

```bash
cd backend
pip install -r requirements.txt
python main.py
```

或使用uvicorn命令：
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API文档

启动后访问：http://localhost:8000/docs

## 目录结构

```
backend/
├── main.py              # 主应用入口
├── app/                 # 应用模块
│   ├── __init__.py
│   ├── models.py        # 数据模型
│   ├── routers/         # 路由模块
│   └── services/        # 业务逻辑
├── modules/             # 图像处理模块
│   ├── avatar_detector.py
│   ├── avatar_replacer.py
│   └── right_side_filter.py
├── temp/                # 临时文件存储
└── requirements.txt     # 依赖包
```