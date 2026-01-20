"""
棋盘类
"""
import random
from core.piece import King, Advisor, Elephant, Horse, Rook, Cannon, Pawn


class Board:
    """棋盘状态管理"""

    def __init__(self):
        """初始化棋盘"""
        self.grid = [[None for _ in range(9)] for _ in range(10)]
        self.red_pieces = []
        self.black_pieces = []
        self.hash_value = 0
        self._init_zobrist()
        self.setup_initial_position()

    def _init_zobrist(self):
        """初始化 Zobrist 哈希表"""
        random.seed(42)  # 固定种子以保证一致性
        self.zobrist_table = {}

        piece_types = ['K', 'A', 'E', 'H', 'R', 'C', 'P']
        colors = ['red', 'black']

        for piece_type in piece_types:
            for color in colors:
                for row in range(10):
                    for col in range(9):
                        key = (piece_type, color, row, col)
                        self.zobrist_table[key] = random.getrandbits(64)

    def setup_initial_position(self):
        """设置初始棋局"""
        # 清空棋盘
        self.grid = [[None for _ in range(9)] for _ in range(10)]
        self.red_pieces = []
        self.black_pieces = []
        self.hash_value = 0

        # 黑方（上方，行0-4）
        # 第0行：车马象士将士象马车
        self.add_piece(Rook('black', 0, 0))
        self.add_piece(Horse('black', 0, 1))
        self.add_piece(Elephant('black', 0, 2))
        self.add_piece(Advisor('black', 0, 3))
        self.add_piece(King('black', 0, 4))
        self.add_piece(Advisor('black', 0, 5))
        self.add_piece(Elephant('black', 0, 6))
        self.add_piece(Horse('black', 0, 7))
        self.add_piece(Rook('black', 0, 8))

        # 第2行：炮
        self.add_piece(Cannon('black', 2, 1))
        self.add_piece(Cannon('black', 2, 7))

        # 第3行：卒
        for col in [0, 2, 4, 6, 8]:
            self.add_piece(Pawn('black', 3, col))

        # 红方（下方，行5-9）
        # 第6行：兵
        for col in [0, 2, 4, 6, 8]:
            self.add_piece(Pawn('red', 6, col))

        # 第7行：炮
        self.add_piece(Cannon('red', 7, 1))
        self.add_piece(Cannon('red', 7, 7))

        # 第9行：车马象士将士象马车
        self.add_piece(Rook('red', 9, 0))
        self.add_piece(Horse('red', 9, 1))
        self.add_piece(Elephant('red', 9, 2))
        self.add_piece(Advisor('red', 9, 3))
        self.add_piece(King('red', 9, 4))
        self.add_piece(Advisor('red', 9, 5))
        self.add_piece(Elephant('red', 9, 6))
        self.add_piece(Horse('red', 9, 7))
        self.add_piece(Rook('red', 9, 8))

    def add_piece(self, piece):
        """添加棋子到棋盘"""
        self.grid[piece.row][piece.col] = piece
        if piece.color == 'red':
            self.red_pieces.append(piece)
        else:
            self.black_pieces.append(piece)

        # 更新哈希值
        key = (piece.type, piece.color, piece.row, piece.col)
        if key in self.zobrist_table:
            self.hash_value ^= self.zobrist_table[key]

    def remove_piece(self, piece):
        """从棋盘移除棋子"""
        self.grid[piece.row][piece.col] = None
        if piece.color == 'red':
            if piece in self.red_pieces:
                self.red_pieces.remove(piece)
        else:
            if piece in self.black_pieces:
                self.black_pieces.remove(piece)

        # 更新哈希值
        key = (piece.type, piece.color, piece.row, piece.col)
        if key in self.zobrist_table:
            self.hash_value ^= self.zobrist_table[key]

    def get_piece(self, row, col):
        """获取指定位置的棋子"""
        if 0 <= row <= 9 and 0 <= col <= 8:
            return self.grid[row][col]
        return None

    def make_move(self, move):
        """
        执行走法

        Args:
            move: Move 对象

        Returns:
            被吃的棋子（用于撤销）
        """
        # 重要：从当前棋盘获取实际的棋子对象，而不是使用move.piece
        # 因为move.piece可能来自副本棋盘
        actual_piece = self.get_piece(move.from_row, move.from_col)

        if actual_piece is None:
            # 如果起始位置没有棋子，说明move无效
            return None

        # 移除起始位置的棋子哈希
        key = (actual_piece.type, actual_piece.color, move.from_row, move.from_col)
        if key in self.zobrist_table:
            self.hash_value ^= self.zobrist_table[key]

        # 移除目标位置的棋子（如果有）
        captured = self.get_piece(move.to_row, move.to_col)
        if captured:
            self.remove_piece(captured)

        # 移动棋子
        self.grid[move.from_row][move.from_col] = None
        self.grid[move.to_row][move.to_col] = actual_piece
        actual_piece.row = move.to_row
        actual_piece.col = move.to_col

        # 添加新位置的棋子哈希
        key = (actual_piece.type, actual_piece.color, move.to_row, move.to_col)
        if key in self.zobrist_table:
            self.hash_value ^= self.zobrist_table[key]

        return captured

    def undo_move(self, move, captured_piece):
        """
        撤销走法

        Args:
            move: Move 对象
            captured_piece: 被吃的棋子
        """
        # 重要：从当前棋盘获取实际的棋子对象
        actual_piece = self.get_piece(move.to_row, move.to_col)

        if actual_piece is None:
            return

        # 移除当前位置的棋子哈希
        key = (actual_piece.type, actual_piece.color, move.to_row, move.to_col)
        if key in self.zobrist_table:
            self.hash_value ^= self.zobrist_table[key]

        # 移动棋子回原位
        self.grid[move.to_row][move.to_col] = captured_piece
        self.grid[move.from_row][move.from_col] = actual_piece
        actual_piece.row = move.from_row
        actual_piece.col = move.from_col

        # 恢复被吃的棋子
        if captured_piece:
            if captured_piece.color == 'red':
                if captured_piece not in self.red_pieces:
                    self.red_pieces.append(captured_piece)
            else:
                if captured_piece not in self.black_pieces:
                    self.black_pieces.append(captured_piece)

            # 恢复被吃棋子的哈希
            key = (captured_piece.type, captured_piece.color, captured_piece.row, captured_piece.col)
            if key in self.zobrist_table:
                self.hash_value ^= self.zobrist_table[key]

        # 恢复原位置的棋子哈希
        key = (actual_piece.type, actual_piece.color, move.from_row, move.from_col)
        if key in self.zobrist_table:
            self.hash_value ^= self.zobrist_table[key]

    def get_all_pieces(self, color=None):
        """获取所有棋子或指定颜色的棋子"""
        if color == 'red':
            return self.red_pieces.copy()
        elif color == 'black':
            return self.black_pieces.copy()
        else:
            return self.red_pieces + self.black_pieces

    def get_legal_moves(self, color):
        """
        获取某方所有合法走法

        Args:
            color: 'red' or 'black'

        Returns:
            list: 合法走法列表
        """
        from core.rules import is_legal_move

        legal_moves = []
        pieces = self.red_pieces if color == 'red' else self.black_pieces

        for piece in pieces:
            possible_moves = piece.get_possible_moves(self)
            for move in possible_moves:
                if is_legal_move(self, move, color):
                    legal_moves.append(move)

        return legal_moves

    def find_king(self, color):
        """找到指定颜色的将/帅"""
        pieces = self.red_pieces if color == 'red' else self.black_pieces
        for piece in pieces:
            if piece.type == 'K':
                return piece
        return None

    def copy(self):
        """创建棋盘的深拷贝"""
        new_board = Board()
        new_board.grid = [[None for _ in range(9)] for _ in range(10)]
        new_board.red_pieces = []
        new_board.black_pieces = []
        new_board.hash_value = self.hash_value
        new_board.zobrist_table = self.zobrist_table

        # 复制所有棋子
        for piece in self.get_all_pieces():
            new_piece = piece.copy()
            new_board.grid[new_piece.row][new_piece.col] = new_piece
            if new_piece.color == 'red':
                new_board.red_pieces.append(new_piece)
            else:
                new_board.black_pieces.append(new_piece)

        return new_board

    def clear(self):
        """清空棋盘"""
        self.grid = [[None for _ in range(9)] for _ in range(10)]
        self.red_pieces = []
        self.black_pieces = []
        self.hash_value = 0

    def __repr__(self):
        """字符串表示（用于调试）"""
        result = []
        for row in range(10):
            row_str = []
            for col in range(9):
                piece = self.grid[row][col]
                if piece:
                    row_str.append(f"{piece.color[0]}{piece.type}")
                else:
                    row_str.append("--")
            result.append(" ".join(row_str))
        return "\n".join(result)
