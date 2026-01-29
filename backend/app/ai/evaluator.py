"""
局面评估函数 - 基于专业象棋引擎的评估策略
"""
from app import config


class Evaluator:
    """局面评估器"""

    def __init__(self):
        """初始化评估器"""
        # 棋子基础价值
        self.piece_values = config.PIECE_VALUES.copy()

        # 位置价值表（参考专业象棋引擎）
        self._init_position_tables()

    def _init_position_tables(self):
        """初始化位置价值表 - 基于专业象棋引擎优化"""
        # 车的位置价值（控制要道和中路）- 优化版
        self.rook_position_value = [
            [206, 208, 207, 213, 214, 213, 207, 208, 206],
            [206, 212, 209, 216, 233, 216, 209, 212, 206],
            [206, 208, 207, 214, 216, 214, 207, 208, 206],
            [206, 213, 213, 216, 216, 216, 213, 213, 206],
            [208, 211, 211, 214, 215, 214, 211, 211, 208],
            [208, 212, 212, 214, 215, 214, 212, 212, 208],
            [204, 209, 204, 212, 214, 212, 204, 209, 204],
            [198, 208, 204, 212, 212, 212, 204, 208, 198],
            [200, 208, 206, 212, 200, 212, 206, 208, 200],
            [194, 206, 204, 212, 200, 212, 204, 206, 194],
        ]

        # 马的位置价值（中心控制）- 优化版
        self.horse_position_value = [
            [90, 90, 90, 96, 90, 96, 90, 90, 90],
            [90, 96, 103, 97, 94, 97, 103, 96, 90],
            [92, 98, 99, 103, 99, 103, 99, 98, 92],
            [93, 108, 100, 107, 100, 107, 100, 108, 93],
            [90, 100, 99, 103, 104, 103, 99, 100, 90],
            [90, 98, 101, 102, 103, 102, 101, 98, 90],
            [92, 94, 98, 95, 98, 95, 98, 94, 92],
            [93, 92, 94, 95, 92, 95, 94, 92, 93],
            [85, 90, 92, 93, 78, 93, 92, 90, 85],
            [88, 85, 90, 88, 90, 88, 90, 85, 88],
        ]

        # 炮的位置价值（中路和河口）- 优化版
        self.cannon_position_value = [
            [100, 100, 96, 91, 90, 91, 96, 100, 100],
            [98, 98, 96, 92, 89, 92, 96, 98, 98],
            [97, 97, 96, 91, 92, 91, 96, 97, 97],
            [96, 99, 99, 98, 100, 98, 99, 99, 96],
            [96, 96, 96, 96, 100, 96, 96, 96, 96],
            [95, 96, 99, 96, 100, 96, 99, 96, 95],
            [96, 96, 96, 96, 96, 96, 96, 96, 96],
            [97, 96, 100, 99, 101, 99, 100, 96, 97],
            [96, 97, 98, 98, 98, 98, 98, 97, 96],
            [96, 96, 97, 99, 99, 99, 97, 96, 96],
        ]

        # 兵/卒的位置价值（过河更有价值）- 优化版
        self.pawn_position_value = [
            [9, 9, 9, 11, 13, 11, 9, 9, 9],
            [19, 24, 34, 42, 44, 42, 34, 24, 19],
            [19, 24, 32, 37, 37, 37, 32, 24, 19],
            [19, 23, 27, 29, 30, 29, 27, 23, 19],
            [14, 18, 20, 27, 29, 27, 20, 18, 14],
            [7, 0, 13, 0, 16, 0, 13, 0, 7],
            [7, 0, 7, 0, 15, 0, 7, 0, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # 士的位置价值（保护将帅）- 优化版
        self.advisor_position_value = [
            [0, 0, 0, 20, 0, 20, 0, 0, 0],
            [0, 0, 0, 0, 23, 0, 0, 0, 0],
            [0, 0, 0, 20, 0, 20, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # 相/象的位置价值 - 优化版
        self.elephant_position_value = [
            [0, 0, 20, 0, 0, 0, 20, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [18, 0, 0, 0, 23, 0, 0, 0, 18],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 20, 0, 0, 0, 20, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # 将/帅的位置价值（中心更安全）- 优化版
        self.king_position_value = [
            [0, 0, 0, 8888, 8888, 8888, 0, 0, 0],
            [0, 0, 0, 8888, 8888, 8888, 0, 0, 0],
            [0, 0, 0, 8888, 8888, 8888, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

    def evaluate(self, board):
        """
        评估当前局面

        Args:
            board: 棋盘对象

        Returns:
            float: 评分（正数表示红方优势，负数表示黑方优势）
        """
        from app.core.rules import is_checkmate, get_game_result

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

        # 1. 子力价值（35%权重）- 进一步降低，更注重战术
        material_score = self._evaluate_material(board)
        score += material_score * 0.35

        # 2. 位置价值（30%权重）- 提高位置的重要性
        score += self._evaluate_position(board) * 0.30

        # 3. 将帅安全（15%权重）
        score += self._evaluate_king_safety(board) * 0.15

        # 4. 进攻性评估（15%权重）
        score += self._evaluate_aggression(board) * 0.15

        # 5. 残局评估（5%权重）- 新增
        score += self._evaluate_endgame(board, material_score) * 0.05

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
        from app.core.rules import is_in_check

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
        from app.core.rules import is_in_check

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

    def _evaluate_endgame(self, board, material_score):
        """
        残局评估 - 根据子力判断是否进入残局，并调整策略

        Args:
            board: 棋盘对象
            material_score: 当前子力评分

        Returns:
            float: 残局评分
        """
        score = 0

        # 统计双方子力
        red_pieces = []
        black_pieces = []
        for piece in board.get_all_pieces():
            if piece.color == 'red':
                red_pieces.append(piece)
            else:
                black_pieces.append(piece)

        total_pieces = len(red_pieces) + len(black_pieces)

        # 判断是否进入残局（总子力少于16个）
        if total_pieces <= 16:
            # 残局中，将帅应该更主动
            red_king = board.find_king('red')
            black_king = board.find_king('black')

            if red_king and black_king:
                # 残局中，将帅之间的距离很重要
                king_distance = abs(red_king.row - black_king.row) + abs(red_king.col - black_king.col)

                # 如果我方优势，应该缩小距离（追杀）
                if material_score > 200:
                    score += (15 - king_distance) * 10
                # 如果对方优势，应该拉大距离（逃跑）
                elif material_score < -200:
                    score += king_distance * 10

            # 残局中，兵的价值大幅提升
            for piece in board.get_all_pieces():
                if piece.type == 'P':
                    # 过河兵在残局中价值更高
                    if piece.color == 'red' and piece.row <= 4:
                        score += 50
                    elif piece.color == 'black' and piece.row >= 5:
                        score -= 50

                    # 接近对方底线的兵价值极高
                    if piece.color == 'red' and piece.row <= 2:
                        score += 100
                    elif piece.color == 'black' and piece.row >= 7:
                        score -= 100

        # 判断是否是单子残局（极少子力）
        if total_pieces <= 10:
            # 单车、单炮残局
            red_major_pieces = [p for p in red_pieces if p.type in ['R', 'C']]
            black_major_pieces = [p for p in black_pieces if p.type in ['R', 'C']]

            # 如果一方只剩将帅，另一方有大子，大幅加分
            if len(red_pieces) == 1 and len(black_major_pieces) > 0:
                score -= 500  # 黑方必胜
            elif len(black_pieces) == 1 and len(red_major_pieces) > 0:
                score += 500  # 红方必胜

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
