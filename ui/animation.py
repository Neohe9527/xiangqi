"""
棋子移动动画系统
"""
import time


class PieceAnimation:
    """棋子移动动画"""

    def __init__(self, piece, from_pos, to_pos, duration=0.3):
        """
        初始化动画

        Args:
            piece: 棋子对象
            from_pos: 起始位置 (x, y)
            to_pos: 目标位置 (x, y)
            duration: 动画持续时间（秒）
        """
        self.piece = piece
        self.from_x, self.from_y = from_pos
        self.to_x, self.to_y = to_pos
        self.duration = duration
        self.start_time = time.time()
        self.finished = False

    def update(self):
        """
        更新动画状态

        Returns:
            tuple: 当前位置 (x, y)，如果动画结束返回 None
        """
        if self.finished:
            return None

        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.duration, 1.0)

        if progress >= 1.0:
            self.finished = True
            return None

        # 使用缓动函数（ease-out）
        progress = self._ease_out_cubic(progress)

        # 计算当前位置
        current_x = self.from_x + (self.to_x - self.from_x) * progress
        current_y = self.from_y + (self.to_y - self.from_y) * progress

        return (current_x, current_y)

    def _ease_out_cubic(self, t):
        """缓动函数：三次方缓出"""
        return 1 - pow(1 - t, 3)

    def is_finished(self):
        """动画是否结束"""
        return self.finished


class AnimationManager:
    """动画管理器"""

    def __init__(self):
        """初始化动画管理器"""
        self.animations = []

    def add_animation(self, animation):
        """
        添加动画

        Args:
            animation: PieceAnimation 对象
        """
        self.animations.append(animation)

    def update(self):
        """更新所有动画"""
        # 移除已完成的动画
        self.animations = [anim for anim in self.animations if not anim.is_finished()]

    def get_active_animations(self):
        """获取所有活跃的动画"""
        return self.animations

    def has_active_animations(self):
        """是否有活跃的动画"""
        return len(self.animations) > 0

    def clear(self):
        """清除所有动画"""
        self.animations.clear()
