import cv2
import numpy as np

class AvatarReplacer:
    def __init__(self):
        pass

    def create_rounded_mask(self, width, height, corner_radius):
        """
        创建圆角矩形遮罩
        :param width: 遮罩宽度
        :param height: 遮罩高度
        :param corner_radius: 圆角半径
        :return: 遮罩图像
        """
        mask = np.zeros((height, width), dtype=np.uint8)

        # 创建圆角矩形
        # 四个角的圆形
        cv2.circle(mask, (corner_radius, corner_radius), corner_radius, 255, -1)
        cv2.circle(mask, (width - corner_radius, corner_radius), corner_radius, 255, -1)
        cv2.circle(mask, (corner_radius, height - corner_radius), corner_radius, 255, -1)
        cv2.circle(mask, (width - corner_radius, height - corner_radius), corner_radius, 255, -1)

        # 填充中间的矩形区域
        cv2.rectangle(mask, (corner_radius, 0), (width - corner_radius, height), 255, -1)
        cv2.rectangle(mask, (0, corner_radius), (width, height - corner_radius), 255, -1)

        return mask

    def extract_original_mask(self, original_roi):
        """
        从原始头像区域提取遮罩（用于保持原有的圆角形状）
        :param original_roi: 原始头像区域
        :return: 提取的遮罩
        """
        h, w = original_roi.shape[:2]

        # 创建一个基础的圆角矩形遮罩
        # 根据头像尺寸自动计算圆角半径
        corner_radius = min(w, h) // 8  # 圆角半径为宽高最小值的1/8

        mask = np.zeros((h, w), dtype=np.uint8)

        # 创建圆角矩形
        if corner_radius > 0:
            # 四个角的圆形
            if corner_radius < w//2 and corner_radius < h//2:
                cv2.circle(mask, (corner_radius, corner_radius), corner_radius, 255, -1)
                cv2.circle(mask, (w - corner_radius, corner_radius), corner_radius, 255, -1)
                cv2.circle(mask, (corner_radius, h - corner_radius), corner_radius, 255, -1)
                cv2.circle(mask, (w - corner_radius, h - corner_radius), corner_radius, 255, -1)

                # 填充中间的矩形区域
                cv2.rectangle(mask, (corner_radius, 0), (w - corner_radius, h), 255, -1)
                cv2.rectangle(mask, (0, corner_radius), (w, h - corner_radius), 255, -1)
            else:
                # 如果圆角半径太大，就创建一个椭圆
                cv2.ellipse(mask, (w//2, h//2), (w//2-2, h//2-2), 0, 0, 360, 255, -1)
        else:
            # 如果没有圆角，就是矩形
            cv2.rectangle(mask, (0, 0), (w, h), 255, -1)

        # 轻微的高斯模糊使边缘更平滑
        mask = cv2.GaussianBlur(mask, (3, 3), 0)

        return mask

    def replace_avatar(self, original_img, new_avatar, position, size, shape='rect', corner_radius=None):
        """
        替换单个头像
        :param original_img: 聊天记录原图（BGR）
        :param new_avatar: 新头像（BGR）
        :param position: (x, y) 左上角坐标
        :param size: (w, h) 头像尺寸
        :param shape: 'circle'、'rect' 或 'rounded'
        :param corner_radius: 圆角半径（当shape='rounded'时使用）
        :return: 替换后的图片
        """
        x, y = position
        w, h = size

        # 调整新头像尺寸
        resized_avatar = cv2.resize(new_avatar, (w, h))

        # 提取原图对应区域
        roi = original_img[y:y+h, x:x+w]

        if shape == 'circle':
            # 创建圆形遮罩
            mask = np.zeros((h, w), dtype=np.uint8)
            cv2.circle(mask, (w//2, h//2), min(w, h)//2, 255, -1)
        elif shape == 'rounded':
            # 使用原始头像区域提取遮罩，保持原有形状
            mask = self.extract_original_mask(roi)
        else:
            # 方形直接替换
            result_img = original_img.copy()
            result_img[y:y+h, x:x+w] = resized_avatar
            return result_img

        # 应用遮罩进行替换
        # 创建3通道遮罩
        mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        mask_inv_3ch = cv2.cvtColor(cv2.bitwise_not(mask), cv2.COLOR_GRAY2BGR)

        # 归一化遮罩到0-1范围，用于alpha混合
        mask_norm = mask_3ch.astype(np.float32) / 255.0
        mask_inv_norm = mask_inv_3ch.astype(np.float32) / 255.0

        # 使用alpha混合，保留原始背景
        roi_float = roi.astype(np.float32)
        avatar_float = resized_avatar.astype(np.float32)

        # 只在遮罩区域内替换头像，遮罩外保持原样
        blended = roi_float * mask_inv_norm + avatar_float * mask_norm
        blended = blended.astype(np.uint8)

        # 替换回原图
        result_img = original_img.copy()
        result_img[y:y+h, x:x+w] = blended

        return result_img