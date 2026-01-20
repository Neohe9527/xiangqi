"""
游戏管理器
"""
import time
from core.board import Board
from core.rules import get_game_result, is_in_check
from game.history import History
from game.player import HumanPlayer, AIPlayer
from ai.random_ai import RandomAI
from ai.greedy_ai import GreedyAI
from ai.minimax_ai import MinimaxAI
from ai.alphabeta_ai import AlphaBetaAI
import config


class GameManager:
    """游戏状态管理"""

    def __init__(self):
        """初始化游戏管理器"""
        self.board = Board()
        self.history = History()
        self.red_player = None
        self.black_player = None
        self.current_color = 'red'  # 红方先走
        self.game_mode = config.MODE_HUMAN_VS_AI
        self.game_result = 'ongoing'
        self.paused = False
        self.selected_piece = None
        self.legal_moves_for_selected = []
        self.last_move = None  # 记录最后一步走法

    def setup_game(self, mode, red_player_type, black_player_type,
                   red_ai_type='random', black_ai_type='alphabeta'):
        """
        设置游戏

        Args:
            mode: 游戏模式 ('human_vs_ai', 'ai_vs_ai', 'setup')
            red_player_type: 'human' or 'ai'
            black_player_type: 'human' or 'ai'
            red_ai_type: AI类型 ('random', 'greedy', 'minimax', 'alphabeta')
            black_ai_type: AI类型
        """
        self.game_mode = mode
        self.board.setup_initial_position()
        self.history.clear()
        self.current_color = 'red'
        self.game_result = 'ongoing'
        self.selected_piece = None
        self.legal_moves_for_selected = []
        self.last_move = None  # 重置最后一步走法

        # 创建红方玩家
        if red_player_type == 'human':
            self.red_player = HumanPlayer('red')
        else:
            ai = self._create_ai('red', red_ai_type)
            self.red_player = AIPlayer('red', ai)

        # 创建黑方玩家
        if black_player_type == 'human':
            self.black_player = HumanPlayer('black')
        else:
            ai = self._create_ai('black', black_ai_type)
            self.black_player = AIPlayer('black', ai)

    def _create_ai(self, color, ai_type):
        """创建AI实例"""
        if ai_type == 'random':
            return RandomAI(color)
        elif ai_type == 'greedy':
            return GreedyAI(color)
        elif ai_type == 'minimax':
            return MinimaxAI(color, depth=3)
        elif ai_type == 'alphabeta':
            return AlphaBetaAI(color, depth=6, time_limit=15)
        else:
            return RandomAI(color)

    def get_current_player(self):
        """获取当前玩家"""
        return self.red_player if self.current_color == 'red' else self.black_player

    def is_current_player_ai(self):
        """当前玩家是否是AI"""
        player = self.get_current_player()
        return player is not None and player.player_type == 'ai'

    def handle_click(self, row, col):
        """
        处理棋盘点击（人类玩家）

        Args:
            row: 行
            col: 列

        Returns:
            bool: 是否成功执行了走法
        """
        if self.game_result != 'ongoing':
            return False

        if self.is_current_player_ai():
            return False

        piece = self.board.get_piece(row, col)

        # 如果没有选中棋子
        if self.selected_piece is None:
            # 选中己方棋子
            if piece and piece.color == self.current_color:
                self.selected_piece = piece
                self.legal_moves_for_selected = self._get_legal_moves_for_piece(piece)
                return False
        else:
            # 已经选中了棋子
            # 检查是否点击了目标位置
            target_move = None
            for move in self.legal_moves_for_selected:
                if move.to_row == row and move.to_col == col:
                    target_move = move
                    break

            if target_move:
                # 执行走法
                self.make_move(target_move)
                self.selected_piece = None
                self.legal_moves_for_selected = []
                return True
            else:
                # 重新选择棋子
                if piece and piece.color == self.current_color:
                    self.selected_piece = piece
                    self.legal_moves_for_selected = self._get_legal_moves_for_piece(piece)
                else:
                    self.selected_piece = None
                    self.legal_moves_for_selected = []
                return False

    def _get_legal_moves_for_piece(self, piece):
        """获取指定棋子的合法走法"""
        from core.rules import is_legal_move
        possible_moves = piece.get_possible_moves(self.board)
        legal_moves = []
        for move in possible_moves:
            if is_legal_move(self.board, move, piece.color):
                legal_moves.append(move)
        return legal_moves

    def make_move(self, move):
        """
        执行走法

        Args:
            move: Move 对象

        Returns:
            bool: 是否成功
        """
        if self.game_result != 'ongoing':
            return False

        # 执行走法
        captured = self.board.make_move(move)

        # 记录历史
        self.history.add_move(move, captured)

        # 记录最后一步走法
        self.last_move = move

        # 切换玩家
        self.current_color = 'black' if self.current_color == 'red' else 'red'

        # 检查游戏结果
        self.game_result = get_game_result(self.board, self.current_color)

        return True

    def undo_move(self, steps=1):
        """
        悔棋

        Args:
            steps: 悔棋步数（人机对弈时通常是2步）

        Returns:
            bool: 是否成功
        """
        if self.game_result != 'ongoing':
            return False

        for _ in range(steps):
            result = self.history.undo_last_move()
            if result is None:
                return False

            move, captured = result
            self.board.undo_move(move, captured)
            self.current_color = 'black' if self.current_color == 'red' else 'red'

        self.game_result = 'ongoing'
        self.selected_piece = None
        self.legal_moves_for_selected = []
        return True

    def get_ai_move(self):
        """
        获取AI的走法

        Returns:
            Move: AI选择的走法
        """
        player = self.get_current_player()
        if player is None or player.player_type != 'ai':
            return None

        return player.get_move(self.board)

    def get_ai_thinking_info(self):
        """获取AI思考信息"""
        player = self.get_current_player()
        if player is not None and player.player_type == 'ai':
            return player.get_thinking_info()
        return None

    def is_in_check(self, color=None):
        """检查指定颜色是否被将军"""
        if color is None:
            color = self.current_color
        return is_in_check(self.board, color)

    def get_game_status_text(self):
        """获取游戏状态文本"""
        if self.game_result == 'red_win':
            return "红方胜利！"
        elif self.game_result == 'black_win':
            return "黑方胜利！"
        elif self.game_result == 'draw':
            return "和棋"
        else:
            player = self.get_current_player()
            if player is None:
                return "请选择游戏模式"

            color_text = "红方" if self.current_color == 'red' else "黑方"

            if player.player_type == 'ai':
                return f"{color_text}思考中... ({player.ai.name})"
            else:
                return f"{color_text}走棋"

    def reset_game(self):
        """重置游戏"""
        self.board.setup_initial_position()
        self.history.clear()
        self.current_color = 'red'
        self.game_result = 'ongoing'
        self.selected_piece = None
        self.legal_moves_for_selected = []

    def setup_custom_position(self):
        """设置自定义局面（残局布置）"""
        self.board.clear()
        self.history.clear()
        self.current_color = 'red'
        self.game_result = 'ongoing'
        self.selected_piece = None
        self.legal_moves_for_selected = []
