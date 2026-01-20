"""
玩家抽象类
"""
from abc import ABC, abstractmethod


class Player(ABC):
    """玩家基类（人类或AI）"""

    def __init__(self, color, player_type):
        """
        初始化玩家

        Args:
            color: 'red' or 'black'
            player_type: 'human' or 'ai'
        """
        self.color = color
        self.player_type = player_type

    @abstractmethod
    def get_move(self, board):
        """
        获取走法

        Args:
            board: 棋盘对象

        Returns:
            Move: 走法对象
        """
        pass

    def __repr__(self):
        return f"{self.player_type.capitalize()}Player({self.color})"


class HumanPlayer(Player):
    """人类玩家"""

    def __init__(self, color):
        super().__init__(color, 'human')
        self.selected_move = None

    def get_move(self, board):
        """
        获取人类玩家的走法（通过UI交互）

        Args:
            board: 棋盘对象

        Returns:
            Move: 走法对象（由UI设置）
        """
        # 这个方法在UI层会被调用
        # selected_move 由UI交互设置
        move = self.selected_move
        self.selected_move = None
        return move

    def set_move(self, move):
        """设置选择的走法"""
        self.selected_move = move


class AIPlayer(Player):
    """AI玩家"""

    def __init__(self, color, ai_instance):
        """
        初始化AI玩家

        Args:
            color: 'red' or 'black'
            ai_instance: AI实例（RandomAI, GreedyAI等）
        """
        super().__init__(color, 'ai')
        self.ai = ai_instance

    def get_move(self, board):
        """
        获取AI的走法

        Args:
            board: 棋盘对象

        Returns:
            Move: 走法对象
        """
        return self.ai.get_move(board)

    def get_thinking_info(self):
        """获取AI思考信息"""
        return self.ai.get_thinking_info()

    def __repr__(self):
        return f"AIPlayer({self.color}, {self.ai.name})"
