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
        from core.rules import is_checkmate, get_game_result

        # 首先检查是否已经分出胜负
        red_result = get_game_result(board, 'red')
        black_result = get_game_result(board, 'black')

        # 红方胜利 - 给予极高分数
        if red_result == 'red_win' or black_result == 'red_win':
            return 100000

        # 黑方胜利 - 给予极低分数
        if red_result == 'black_win' or black_result == 'black_win':
            return -100000

        # 和棋
        if red_result == 'draw' or black_result == 'draw':
            return 0

        # 检查是否即将被将死（距离胜负只有一步）
        # 如果对方被将死，给予极高奖励
        if is_checkmate(board, 'black'):
            return 50000
        if is_checkmate(board, 'red'):
            return -50000

        score = 0

        # 1. 子力价值（40%权重）- 降低权重，让AI更注重战术
        score += self._evaluate_material(board) * 0.4

        # 2. 位置价值（25%权重）
        score += self._evaluate_position(board) * 0.25

        # 3. 将帅安全（20%权重）
        score += self._evaluate_king_safety(board) * 0.2

        # 4. 进攻性评估（15%权重）- 新增：鼓励进攻
        score += self._evaluate_aggression(board) * 0.15

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

    def _evaluate_aggression(self, board):
        """
        评估进攻性 - 鼓励AI主动进攻

        Args:
            board: 棋盘对象

        Returns:
            float: 进攻性评分
        """
        from core.rules import is_in_check

        score = 0

        # 1. 控制对方半场的棋子数量（鼓励进攻）
        red_in_enemy = 0
        black_in_enemy = 0

        for piece in board.get_all_pieces():
            if piece.color == 'red' and piece.row <= 4:  # 红方在黑方半场
                red_in_enemy += 1
                # 过河兵特别奖励
                if piece.type == 'P':
                    score += 30
            elif piece.color == 'black' and piece.row >= 5:  # 黑方在红方半场
                black_in_enemy += 1
                if piece.type == 'P':
                    score -= 30

        score += (red_in_enemy - black_in_enemy) * 15

        # 2. 威胁对方将帅的棋子数量
        red_king = board.find_king('red')
        black_king = board.find_king('black')

        if black_king:
            # 统计能攻击到黑方将帅附近的红方棋子
            threat_count = 0
            for piece in board.get_all_pieces():
                if piece.color == 'red':
                    moves = piece.get_possible_moves(board)
                    for move in moves:
                        # 如果能走到将帅附近3格内
                        distance = abs(move.to_row - black_king.row) + abs(move.to_col - black_king.col)
                        if distance <= 3:
                            threat_count += 1
                            break
            score += threat_count * 20

        if red_king:
            # 统计能攻击到红方将帅附近的黑方棋子
            threat_count = 0
            for piece in board.get_all_pieces():
                if piece.color == 'black':
                    moves = piece.get_possible_moves(board)
                    for move in moves:
                        distance = abs(move.to_row - red_king.row) + abs(move.to_col - red_king.col)
                        if distance <= 3:
                            threat_count += 1
                            break
            score -= threat_count * 20

        # 3. 控制中心区域（中路3列）
        red_center_control = 0
        black_center_control = 0

        for piece in board.get_all_pieces():
            if 3 <= piece.col <= 5:  # 中路3列
                if piece.color == 'red':
                    red_center_control += 1
                else:
                    black_center_control += 1

        score += (red_center_control - black_center_control) * 10

        # 4. 活动力评估（可走的合法步数）
        red_mobility = len(board.get_legal_moves('red'))
        black_mobility = len(board.get_legal_moves('black'))
        score += (red_mobility - black_mobility) * 2

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
