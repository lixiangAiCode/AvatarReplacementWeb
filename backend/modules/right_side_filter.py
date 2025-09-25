class RightSideFilter:
    def __init__(self, right_ratio=0.6):
        """
        :param right_ratio: 右侧阈值比例，默认0.6，表示图片右侧40%区域
        """
        self.right_ratio = right_ratio

    def filter_right_avatars(self, avatars, image_width):
        """
        只保留右侧头像
        :param avatars: [(x, y, r), ...]
        :param image_width: 图片宽度
        :return: 右侧头像列表
        """
        threshold = int(image_width * self.right_ratio)
        right_avatars = [a for a in avatars if a[0] > threshold]
        return right_avatars