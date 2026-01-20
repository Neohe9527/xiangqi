"""
棋子类定义
"""
from abc import ABC, abstractmethod


class Piece(ABC):
    """棋子基类"""

    def __init__(self, piece_type, color, row, col):
        """
        初始化棋子

        Args:
            piece_type: 棋子类型 ('K', 'A', 'E', 'H', 'R', 'C', 'P')
            color: 颜色 ('red' or 'black')
            row: 行位置 (0-9)
            col: 列位置 (0-8)
        """
        self.type = piece_type
        self.color = color
        self.row = row
        self.col = col

    @abstractmethod
    def get_possible_moves(self, board):
        """
        获取所有可能的走法（不考虑是否送将）

        Args:
            board: 棋盘对象

        Returns:
            list: 可能的走法列表
        """
        pass

    def get_chinese_name(self):
        """获取棋子的中文名称"""
        names = {
            'K': '将' if self.color == 'red' else '帅',
            'A': '士',
            'E': '象' if self.color == 'red' else '象',
            'H': '马',
            'R': '车',
            'C': '炮',
            'P': '兵' if self.color == 'red' else '卒'
        }
        return names.get(self.type, '?')

    def copy(self):
        """创建棋子的副本"""
        piece_class = self.__class__
        return piece_class(self.color, self.row, self.col)

    def __repr__(self):
        return f"{self.color[0].upper()}{self.type}({self.row},{self.col})"


class King(Piece):
    """将/帅"""

    def __init__(self, color, row, col):
        super().__init__('K', color, row, col)

    def get_possible_moves(self, board):
        """将/帅只能在九宫格内移动，每次一步"""
        moves = []
        from core.move import Move

        # 九宫格范围
        if self.color == 'red':
            row_min, row_max = 7, 9
        else:
            row_min, row_max = 0, 2
        col_min, col_max = 3, 5

        # 四个方向
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            new_row = self.row + dr
            new_col = self.col + dc

            # 检查是否在九宫格内
            if row_min <= new_row <= row_max and col_min <= new_col <= col_max:
                target = board.get_piece(new_row, new_col)
                # 目标位置为空或有对方棋子
                if target is None or target.color != self.color:
                    moves.append(Move(self.row, self.col, new_row, new_col, self, target))

        return moves


class Advisor(Piece):
    """士"""

    def __init__(self, color, row, col):
        super().__init__('A', color, row, col)

    def get_possible_moves(self, board):
        """士只能在九宫格内斜着走"""
        moves = []
        from core.move import Move

        # 九宫格范围
        if self.color == 'red':
            row_min, row_max = 7, 9
        else:
            row_min, row_max = 0, 2
        col_min, col_max = 3, 5

        # 四个斜向
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            new_row = self.row + dr
            new_col = self.col + dc

            # 检查是否在九宫格内
            if row_min <= new_row <= row_max and col_min <= new_col <= col_max:
                target = board.get_piece(new_row, new_col)
                if target is None or target.color != self.color:
                    moves.append(Move(self.row, self.col, new_row, new_col, self, target))

        return moves


class Elephant(Piece):
    """象/相"""

    def __init__(self, color, row, col):
        super().__init__('E', color, row, col)

    def get_possible_moves(self, board):
        """象走田字，不能过河"""
        moves = []
        from core.move import Move

        # 象不能过河
        if self.color == 'red':
            row_limit = 5  # 红方不能越过第5行
        else:
            row_limit = 4  # 黑方不能越过第4行

        # 四个田字方向
        directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]

        for dr, dc in directions:
            new_row = self.row + dr
            new_col = self.col + dc

            # 检查是否越界和过河
            if 0 <= new_row <= 9 and 0 <= new_col <= 8:
                if (self.color == 'red' and new_row >= row_limit) or \
                   (self.color == 'black' and new_row <= row_limit):
                    # 检查象眼是否被堵
                    eye_row = self.row + dr // 2
                    eye_col = self.col + dc // 2
                    if board.get_piece(eye_row, eye_col) is None:
                        target = board.get_piece(new_row, new_col)
                        if target is None or target.color != self.color:
                            moves.append(Move(self.row, self.col, new_row, new_col, self, target))

        return moves


class Horse(Piece):
    """马"""

    def __init__(self, color, row, col):
        super().__init__('H', color, row, col)

    def get_possible_moves(self, board):
        """马走日字"""
        moves = []
        from core.move import Move

        # 八个可能的方向
        # 每个方向：(马腿方向, 最终位置)
        directions = [
            ((0, 1), (1, 2)), ((0, 1), (-1, 2)),   # 右
            ((0, -1), (1, -2)), ((0, -1), (-1, -2)),  # 左
            ((1, 0), (2, 1)), ((1, 0), (2, -1)),   # 下
            ((-1, 0), (-2, 1)), ((-1, 0), (-2, -1))   # 上
        ]

        for leg, final in directions:
            leg_row = self.row + leg[0]
            leg_col = self.col + leg[1]
            new_row = self.row + final[0]
            new_col = self.col + final[1]

            # 检查是否越界
            if 0 <= new_row <= 9 and 0 <= new_col <= 8:
                # 检查马腿是否被堵
                if board.get_piece(leg_row, leg_col) is None:
                    target = board.get_piece(new_row, new_col)
                    if target is None or target.color != self.color:
                        moves.append(Move(self.row, self.col, new_row, new_col, self, target))

        return moves


class Rook(Piece):
    """车"""

    def __init__(self, color, row, col):
        super().__init__('R', color, row, col)

    def get_possible_moves(self, board):
        """车可以直线移动任意距离"""
        moves = []
        from core.move import Move

        # 四个方向：上下左右
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            for distance in range(1, 10):
                new_row = self.row + dr * distance
                new_col = self.col + dc * distance

                # 检查是否越界
                if not (0 <= new_row <= 9 and 0 <= new_col <= 8):
                    break

                target = board.get_piece(new_row, new_col)
                if target is None:
                    # 空位，可以继续
                    moves.append(Move(self.row, self.col, new_row, new_col, self, None))
                elif target.color != self.color:
                    # 对方棋子，可以吃，但不能继续
                    moves.append(Move(self.row, self.col, new_row, new_col, self, target))
                    break
                else:
                    # 己方棋子，不能走
                    break

        return moves


class Cannon(Piece):
    """炮"""

    def __init__(self, color, row, col):
        super().__init__('C', color, row, col)

    def get_possible_moves(self, board):
        """炮移动时不能越子，吃子时必须隔一个子"""
        moves = []
        from core.move import Move

        # 四个方向：上下左右
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            jumped = False  # 是否已经跳过一个棋子
            for distance in range(1, 10):
                new_row = self.row + dr * distance
                new_col = self.col + dc * distance

                # 检查是否越界
                if not (0 <= new_row <= 9 and 0 <= new_col <= 8):
                    break

                target = board.get_piece(new_row, new_col)

                if not jumped:
                    # 还没跳过棋子
                    if target is None:
                        # 空位，可以移动
                        moves.append(Move(self.row, self.col, new_row, new_col, self, None))
                    else:
                        # 遇到棋子，标记为已跳过
                        jumped = True
                else:
                    # 已经跳过一个棋子
                    if target is not None:
                        # 遇到第二个棋子
                        if target.color != self.color:
                            # 对方棋子，可以吃
                            moves.append(Move(self.row, self.col, new_row, new_col, self, target))
                        # 无论如何都要停止
                        break

        return moves


class Pawn(Piece):
    """兵/卒"""

    def __init__(self, color, row, col):
        super().__init__('P', color, row, col)

    def get_possible_moves(self, board):
        """兵/卒过河前只能前进，过河后可以左右移动"""
        moves = []
        from core.move import Move

        if self.color == 'red':
            # 红方兵向上走（行号减小）
            forward = -1
            river_line = 4  # 过河线
            crossed = self.row <= river_line
        else:
            # 黑方卒向下走（行号增大）
            forward = 1
            river_line = 5
            crossed = self.row >= river_line

        # 向前走
        new_row = self.row + forward
        if 0 <= new_row <= 9:
            target = board.get_piece(new_row, self.col)
            if target is None or target.color != self.color:
                moves.append(Move(self.row, self.col, new_row, self.col, self, target))

        # 如果已过河，可以左右走
        if crossed:
            for dc in [-1, 1]:
                new_col = self.col + dc
                if 0 <= new_col <= 8:
                    target = board.get_piece(self.row, new_col)
                    if target is None or target.color != self.color:
                        moves.append(Move(self.row, self.col, self.row, new_col, self, target))

        return moves
