import cv2
import numpy as np

class AvatarDetector:
    def __init__(self):
        self.template = None
        self.template_shape = None

    def set_template(self, image, bbox):
        """
        设置头像模板
        :param image: 聊天记录图片
        :param bbox: (x, y, w, h) 手动框选的头像区域
        """
        x, y, w, h = bbox
        self.template = image[y:y+h, x:x+w]
        self.template_shape = (w, h)
        return self.template

    def template_match_avatars(self, image, threshold=0.8):
        """
        使用模板匹配检测头像
        :param image: 聊天记录图片
        :param threshold: 匹配阈值
        :return: [(x, y, w, h), ...] 检测到的头像位置
        """
        if self.template is None:
            return []

        # 模板匹配
        result = cv2.matchTemplate(image, self.template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)

        # 获取匹配位置
        matches = []
        w, h = self.template_shape
        for pt in zip(*locations[::-1]):
            matches.append((pt[0], pt[1], w, h))

        # 非最大值抑制，去除重叠检测框
        if matches:
            matches = self.non_max_suppression(matches, 0.3)

        return matches

    def non_max_suppression(self, boxes, overlap_threshold):
        """
        非最大值抑制，去除重叠的检测框
        :param boxes: [(x, y, w, h), ...]
        :param overlap_threshold: 重叠阈值
        :return: 筛选后的检测框
        """
        if len(boxes) == 0:
            return []

        # 转换为 (x1, y1, x2, y2) 格式
        boxes_array = []
        for x, y, w, h in boxes:
            boxes_array.append([x, y, x+w, y+h])
        boxes_array = np.array(boxes_array, dtype=np.float32)

        # 计算面积
        areas = (boxes_array[:, 2] - boxes_array[:, 0]) * (boxes_array[:, 3] - boxes_array[:, 1])

        # 按照右下角y坐标排序
        indices = np.argsort(boxes_array[:, 3])

        keep = []
        while len(indices) > 0:
            # 选择最后一个索引
            last = len(indices) - 1
            i = indices[last]
            keep.append(i)

            if len(indices) == 1:
                break

            # 计算交集
            xx1 = np.maximum(boxes_array[i, 0], boxes_array[indices[:last], 0])
            yy1 = np.maximum(boxes_array[i, 1], boxes_array[indices[:last], 1])
            xx2 = np.minimum(boxes_array[i, 2], boxes_array[indices[:last], 2])
            yy2 = np.minimum(boxes_array[i, 3], boxes_array[indices[:last], 3])

            # 计算交集面积
            w = np.maximum(0, xx2 - xx1)
            h = np.maximum(0, yy2 - yy1)
            intersection = w * h

            # 计算IoU
            union = areas[i] + areas[indices[:last]] - intersection
            overlap = intersection / union

            # 删除重叠度高的框
            indices = np.delete(indices, np.concatenate(([last], np.where(overlap > overlap_threshold)[0])))

        # 返回保留的检测框
        result = []
        for i in keep:
            x1, y1, x2, y2 = boxes_array[i]
            result.append((int(x1), int(y1), int(x2-x1), int(y2-y1)))

        return result