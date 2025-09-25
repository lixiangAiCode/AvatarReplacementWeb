import cv2
import numpy as np
from typing import Optional, Callable
from .avatar_detector import AvatarDetector
from .avatar_replacer import AvatarReplacer
from .right_side_filter import RightSideFilter

class WebChatAvatarReplacer:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.detector = AvatarDetector()
        self.replacer = AvatarReplacer()
        self.filter = RightSideFilter()
        self.progress_callback: Optional[Callable] = None

    def set_progress_callback(self, callback: Callable):
        """设置进度回调函数，用于实时更新前端"""
        self.progress_callback = callback

    def set_template_from_bytes(self, chat_image_bytes: bytes, bbox: tuple):
        """
        从字节数据设置头像模板
        :param chat_image_bytes: 聊天记录图片字节数据
        :param bbox: (x, y, w, h) 手动框选的头像区域
        """
        chat_img = self._bytes_to_cv2(chat_image_bytes)
        if chat_img is None:
            raise ValueError('聊天记录图片加载失败')
        return self.detector.set_template(chat_img, bbox)

    async def process_from_bytes(self,
                                chat_image_bytes: bytes,
                                avatar_bytes: bytes,
                                bbox: tuple,
                                threshold: float = 0.8,
                                right_ratio: float = 0.6):
        """从字节数据处理，适配Web上传"""

        # 1. 字节转OpenCV图像
        chat_img = self._bytes_to_cv2(chat_image_bytes)
        avatar_img = self._bytes_to_cv2(avatar_bytes)

        if chat_img is None or avatar_img is None:
            raise ValueError('图片加载失败，请检查图片格式')

        if self.progress_callback:
            await self.progress_callback(10, "图片加载完成")

        # 2. 设置模板
        self.detector.set_template(chat_img, bbox)

        if self.progress_callback:
            await self.progress_callback(30, "模板设置完成")

        # 3. 检测头像
        avatar_locations = self.detector.template_match_avatars(chat_img, threshold)

        if self.progress_callback:
            await self.progress_callback(60, f"检测到{len(avatar_locations)}个头像")

        # 4. 筛选右侧头像
        right_avatars = self.filter.filter_right_avatars(
            [(x+w//2, y+h//2, min(w,h)//2) for x,y,w,h in avatar_locations],
            chat_img.shape[1]
        )

        # 5. 批量替换
        result_img = chat_img.copy()
        for x_center, y_center, r in right_avatars:
            # 找到对应的原始检测框
            for x, y, w, h in avatar_locations:
                if abs(x + w//2 - x_center) < 5 and abs(y + h//2 - y_center) < 5:
                    if x >= 0 and y >= 0 and x + w <= chat_img.shape[1] and y + h <= chat_img.shape[0]:
                        result_img = self.replacer.replace_avatar(
                            result_img, avatar_img, (x, y), (w, h), shape='rounded'
                        )
                    break

        if self.progress_callback:
            await self.progress_callback(100, f"处理完成，替换了{len(right_avatars)}个头像")

        return result_img, len(right_avatars)

    def _bytes_to_cv2(self, image_bytes: bytes):
        """字节数据转OpenCV格式"""
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return img
        except Exception:
            return None

    def _cv2_to_bytes(self, cv2_img, format='.png'):
        """OpenCV图像转字节数据"""
        success, buffer = cv2.imencode(format, cv2_img)
        if success:
            return buffer.tobytes()
        return None