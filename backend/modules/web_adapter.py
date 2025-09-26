import cv2
import numpy as np
import base64
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

    async def detect_similar_avatars(self,
                                    chat_image_bytes: bytes,
                                    bbox: tuple,
                                    threshold: float = 0.8,
                                    right_ratio: float = 0.6):
        """检测相似头像，返回检测结果"""
        
        # 1. 字节转OpenCV图像
        chat_img = self._bytes_to_cv2(chat_image_bytes)
        if chat_img is None:
            raise ValueError('聊天记录图片加载失败，请检查图片格式')

        if self.progress_callback:
            await self.progress_callback(10, "开始检测相似头像...")

        # 2. 设置模板
        self.detector.set_template(chat_img, bbox)

        if self.progress_callback:
            await self.progress_callback(30, "模板设置完成")

        # 3. 检测所有相似头像
        avatar_locations = self.detector.template_match_avatars(chat_img, threshold)

        if self.progress_callback:
            await self.progress_callback(60, f"检测到 {len(avatar_locations)} 个相似头像")

        # 4. 筛选右侧头像（默认只替换右侧的头像）
        right_avatars = self.filter.filter_right_avatars(
            [(x+w//2, y+h//2, min(w,h)//2) for x,y,w,h in avatar_locations],
            chat_img.shape[1]
        )

        if self.progress_callback:
            await self.progress_callback(90, f"筛选后得到 {len(right_avatars)} 个目标头像")

        # 5. 生成带检测框的预览图
        preview_img = chat_img.copy()
        detected_avatars = []
        
        for i, (x_center, y_center, r) in enumerate(right_avatars):
            # 找到对应的原始检测框
            for x, y, w, h in avatar_locations:
                if abs(x + w//2 - x_center) < 5 and abs(y + h//2 - y_center) < 5:
                    if x >= 0 and y >= 0 and x + w <= chat_img.shape[1] and y + h <= chat_img.shape[0]:
                        # 在预览图上绘制检测框
                        cv2.rectangle(preview_img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        # 添加编号标签
                        cv2.putText(preview_img, f'{i+1}', (x, y-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        detected_avatars.append({
                            "id": i,
                            "x": x,
                            "y": y,
                            "width": w,
                            "height": h,
                            "center_x": x_center,
                            "center_y": y_center,
                            "radius": r
                        })
                    break

        # 生成预览图的base64
        preview_bytes = self._cv2_to_bytes(preview_img)
        preview_base64 = self._image_to_base64(preview_bytes) if preview_bytes else None

        if self.progress_callback:
            await self.progress_callback(100, f"检测完成，找到 {len(detected_avatars)} 个相似头像")

        return detected_avatars, preview_base64

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

    def _image_to_base64(self, image_bytes: bytes):
        """将图像字节转换为base64字符串"""
        if image_bytes:
            return base64.b64encode(image_bytes).decode('utf-8')
        return None