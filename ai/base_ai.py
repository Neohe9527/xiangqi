"""
AI 基类接口
"""
from abc import ABC, abstractmethod


class BaseAI(ABC):
    """AI 基类"""

    def __init__(self, name, color, difficulty):
        """
        初始化 AI

        Args:
            name: AI 名称
            color: 'red' or 'black'
            difficulty: 难度等级 (1-4)
        """
        self.name = name
        self.color = color
        self.difficulty = difficulty
        self.thinking_info = {
            'depth': 0,
            'nodes_evaluated': 0,
            'best_move': None,
            'score': 0,
            'principal_variation': [],
            'candidate_moves': []
        }

    @abstractmethod
    def get_move(self, board, time_limit=None):
        """
        获取最佳走法

        Args:
            board: 棋盘对象
            time_limit: 时间限制（秒），None 表示无限制

        Returns:
            Move: 最佳走法
        """
        pass

    def get_thinking_info(self):
        """
        获取思考过程信息（用于可视化）

        Returns:
            dict: 思考信息
        """
        return self.thinking_info.copy()

    def reset_thinking_info(self):
        """重置思考信息"""
        self.thinking_info = {
            'depth': 0,
            'nodes_evaluated': 0,
            'best_move': None,
            'score': 0,
            'principal_variation': [],
            'candidate_moves': []
        }

    def __repr__(self):
        return f"{self.name}({self.color}, difficulty={self.difficulty})"
