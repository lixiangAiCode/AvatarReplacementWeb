from typing import Dict, Optional
import asyncio
from datetime import datetime, timedelta
import uuid
import os
import shutil

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        self._cleanup_task = None

    def create_session(self) -> str:
        """创建新的处理会话"""
        session_id = str(uuid.uuid4())
        temp_dir = f"temp/{session_id}"
        os.makedirs(temp_dir, exist_ok=True)

        self.sessions[session_id] = {
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'status': 'created',
            'progress': 0,
            'message': '会话已创建',
            'temp_dir': temp_dir,
            'chat_image_path': None,
            'avatar_path': None,
            'result_path': None,
            'template_bbox': None
        }
        return session_id

    def get_session(self, session_id: str) -> Optional[dict]:
        """获取会话信息"""
        return self.sessions.get(session_id)

    def update_session(self, session_id: str, **kwargs):
        """更新会话信息"""
        if session_id in self.sessions:
            self.sessions[session_id].update({
                'updated_at': datetime.now(),
                **kwargs
            })

    def set_progress(self, session_id: str, progress: int, message: str):
        """更新处理进度"""
        self.update_session(session_id, progress=progress, message=message)

    def start_cleanup_task(self):
        """启动清理任务"""
        if self._cleanup_task is None:
            try:
                self._cleanup_task = asyncio.create_task(self._cleanup_expired())
            except RuntimeError:
                # 如果没有运行的事件循环，暂时跳过
                pass

    def delete_session(self, session_id: str):
        """删除会话并清理文件"""
        if session_id in self.sessions:
            # 清理临时文件
            temp_dir = self.sessions[session_id].get('temp_dir')
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

            del self.sessions[session_id]

    async def _cleanup_expired(self):
        """定期清理过期会话 (2小时后过期)"""
        while True:
            try:
                now = datetime.now()
                expired_sessions = [
                    sid for sid, data in self.sessions.items()
                    if now - data['created_at'] > timedelta(hours=2)
                ]

                for session_id in expired_sessions:
                    self.delete_session(session_id)

                await asyncio.sleep(3600)  # 每小时检查一次
            except Exception as e:
                print(f"清理过期会话时出错: {e}")
                await asyncio.sleep(3600)

# 全局会话管理器实例
session_manager = SessionManager()