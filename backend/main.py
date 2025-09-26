from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routers import session, upload
from app.session_manager import session_manager

# 创建应用实例
app = FastAPI(
    title="聊天头像替换API",
    description="基于模板匹配的聊天头像批量替换工具",
    version="1.0.0"
)

# 配置CORS，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],  # 允许所有域名访问
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(session.router)
app.include_router(upload.router)

# 确保临时目录存在
os.makedirs("temp", exist_ok=True)

@app.on_event("startup")
async def startup_event():
    """应用启动时的事件处理"""
    # 启动会话清理任务
    session_manager.start_cleanup_task()

@app.get("/")
async def root():
    return {"message": "聊天头像替换API服务运行中"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)