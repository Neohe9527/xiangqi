"""
局面评估函数 - 基于专业象棋引擎的评估策略
"""
import config


class Evaluator:
    """局面评估器"""

    def __init__(self):
        """初始化评估器"""
        # 棋子基础价值
        self.piece_values = config.PIECE_VALUES.copy()

        # 位置价值表（参考专业象棋引擎）
        self._init_position_tables()

    def _init_position_tables(self):
        """初始化位置价值表"""
        # 车的位置价值（控制要道和中路）
        self.rook_position_value = [
            [14, 14, 12, 18, 16, 18, 12, 14, 14],
            [16, 20, 18, 24, 26, 24, 18, 20, 16],
            [12, 12, 12, 18, 18, 18, 12, 12, 12],
            [11, 13, 13, 16, 16, 16, 13, 13, 11],
            [11, 11, 11, 14, 14, 14, 11, 11, 11],
            [11, 11, 11, 14, 14, 14, 11, 11, 11],
            [11, 13, 13, 16, 16, 16, 13, 13, 11],
            [12, 12, 12, 18, 18, 18, 12, 12, 12],
            [16, 20, 18, 24, 26, 24, 18, 20, 16],
            [14, 14, 12, 18, 16, 18, 12, 14, 14],
        ]

        # 马的位置价值（中心控制）
        self.horse_position_value = [
            [4, 8, 16, 12, 4, 12, 16, 8, 4],
            [4, 10, 28, 16, 8, 16, 28, 10, 4],
            [12, 14, 16, 20, 18, 20, 16, 14, 12],
            [8, 24, 18, 24, 20, 24, 18, 24, 8],
            [6, 16, 14, 18, 16, 18, 14, 16, 6],
            [4, 12, 16, 14, 12, 14, 16, 12, 4],
            [2, 6, 8, 6, 10, 6, 8, 6, 2],
            [4, 2, 8, 8, 4, 8, 8, 2, 4],
            [0, 2, 4, 4, -2, 4, 4, 2, 0],
            [0, -4, 0, 0, 0, 0, 0, -4, 0],
        ]

        # 炮的位置价值（中路和河口）
        self.cannon_position_value = [
            [6, 4, 0, -10, -12, -10, 0, 4, 6],
            [2, 2, 0, -4, -14, -4, 0, 2, 2],
            [2, 2, 0, -10, -8, -10, 0, 2, 2],
            [0, 0, -2, 4, 10, 4, -2, 0, 0],
            [0, 0, 0, 2, 8, 2, 0, 0, 0],
            [-2, 0, 4, 2, 6, 2, 4, 0, -2],
            [0, 0, 0, 2, 4, 2, 0, 0, 0],
            [4, 0, 8, 6, 10, 6, 8, 0, 4],
            [0, 2, 4, 6, 6, 6, 4, 2, 0],
            [0, 0, 2, 6, 6, 6, 2, 0, 0],
        ]

        # 兵/卒的位置价值（过河更有价值）
        self.pawn_position_value = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, -2, 0, 4, 0, -2, 0, 0],
            [2, 0, 8, 0, 8, 0, 8, 0, 2],
            [6, 12, 18, 18, 20, 18, 18, 12, 6],
            [10, 20, 30, 34, 40, 34, 30, 20, 10],
            [14, 26, 42, 60, 80, 60, 42, 26, 14],
            [18, 36, 56, 80, 120, 80, 56, 36, 18],
            [0, 3, 6, 9, 12, 9, 6, 3, 0],
        ]

        # 士的位置价值（保护将帅）
        self.advisor_position_value = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 20, 0, 20, 0, 0, 0],
            [0, 0, 0, 0, 23, 0, 0, 0, 0],
            [0, 0, 0, 20, 0, 20, 0, 0, 0],
        ]

        # 相/象的位置价值
        self.elephant_position_value = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 20, 0, 0, 0, 20, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 18, 0, 0, 0, 18, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, -2, 0, 0, 0, -2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 20, 0, 0, 0, 20, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # 将/帅的位置价值（中心更安全）
        self.king_position_value = [
            [0, 0, 0, 8, 8, 8, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 10, 10, 10, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 10, 10, 10, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 8, 8, 8, 0, 0, 0],
        ]

    def evaluate(self, board):
        """
        评估当前局面

        Args:
            board: 棋盘对象

        Returns:
            float: 评分（正数表示红方优势，负数表示黑方优势）
        """
        score = 0

        # 1. 子力价值（50%权重）
        score += self._evaluate_material(board) * 0.5

        # 2. 位置价值（30%权重）
        score += self._evaluate_position(board) * 0.3

        # 3. 将帅安全（20%权重）
        score += self._evaluate_king_safety(board) * 0.2

        return score

    def _evaluate_material(self, board):
        """评估子力价值"""
        score = 0

        for piece in board.get_all_pieces():
            value = self.piece_values.get(piece.type, 0)
            if piece.color == 'red':
                score += value
            else:
                score -= value

        return score

    def _evaluate_position(self, board):
        """评估位置价值"""
        score = 0

        for piece in board.get_all_pieces():
            pos_value = 0
            row = piece.row if piece.color == 'red' else (9 - piece.row)

            if piece.type == 'R':
                pos_value = self.rook_position_value[row][piece.col]
            elif piece.type == 'H':
                pos_value = self.horse_position_value[row][piece.col]
            elif piece.type == 'C':
                pos_value = self.cannon_position_value[row][piece.col]
            elif piece.type == 'P':
                pos_value = self.pawn_position_value[row][piece.col]
            elif piece.type == 'A':
                pos_value = self.advisor_position_value[row][piece.col]
            elif piece.type == 'E':
                pos_value = self.elephant_position_value[row][piece.col]
            elif piece.type == 'K':
                pos_value = self.king_position_value[row][piece.col]

            if piece.color == 'red':
                score += pos_value
            else:
                score -= pos_value

        return score

    def _evaluate_king_safety(self, board):
        """评估将帅安全"""
        from core.rules import is_in_check

        score = 0

        # 被将军是很危险的
        if is_in_check(board, 'red'):
            score -= 60
        if is_in_check(board, 'black'):
            score += 60

        # 检查将帅周围的保护
        red_king = board.find_king('red')
        black_king = board.find_king('black')

        if red_king:
            # 统计红方将帅周围的己方棋子数量
            protection = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = red_king.row + dr, red_king.col + dc
                    if 0 <= r <= 9 and 0 <= c <= 8:
                        p = board.get_piece(r, c)
                        if p and p.color == 'red':
                            protection += 1
            score += protection * 5

        if black_king:
            # 统计黑方将帅周围的己方棋子数量
            protection = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = black_king.row + dr, black_king.col + dc
                    if 0 <= r <= 9 and 0 <= c <= 8:
                        p = board.get_piece(r, c)
                        if p and p.color == 'black':
                            protection += 1
            score -= protection * 5

        return score

    def quick_evaluate(self, board):
        """
        快速评估（只考虑子力）

        Args:
            board: 棋盘对象

        Returns:
            float: 评分
        """
        return self._evaluate_material(board)
