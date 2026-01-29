"""
走法表示类
"""


class Move:
    """表示一次走棋"""

    def __init__(self, from_row, from_col, to_row, to_col, piece, captured=None):
        """
        初始化走法

        Args:
            from_row: 起始行
            from_col: 起始列
            to_row: 目标行
            to_col: 目标列
            piece: 移动的棋子
            captured: 被吃的棋子（如果有）
        """
        self.from_row = from_row
        self.from_col = from_col
        self.to_row = to_row
        self.to_col = to_col
        self.piece = piece
        self.captured = captured

    def __eq__(self, other):
        """判断两个走法是否相同"""
        if not isinstance(other, Move):
            return False
        return (self.from_row == other.from_row and
                self.from_col == other.from_col and
                self.to_row == other.to_row and
                self.to_col == other.to_col)

    def __hash__(self):
        """用于在集合和字典中使用"""
        return hash((self.from_row, self.from_col, self.to_row, self.to_col))

    def __repr__(self):
        """字符串表示"""
        return f"Move({self.from_row},{self.from_col})->{self.to_row},{self.to_col})"

    def to_chinese(self):
        """
        转换为中文记谱
        例如: "炮二平五"

        这是一个简化版本，完整实现需要考虑多个同类棋子的情况
        """
        piece_name = self.piece.get_chinese_name()

        # 简化版：只显示棋子名称和目标位置
        if self.piece.color == 'red':
            col_name = ['九', '八', '七', '六', '五', '四', '三', '二', '一'][self.from_col]
            target_col = ['九', '八', '七', '六', '五', '四', '三', '二', '一'][self.to_col]
        else:
            col_name = ['1', '2', '3', '4', '5', '6', '7', '8', '9'][self.from_col]
            target_col = ['1', '2', '3', '4', '5', '6', '7', '8', '9'][self.to_col]

        # 判断移动方向
        if self.to_col == self.from_col:
            # 直线移动
            if self.to_row > self.from_row:
                direction = '进'
            else:
                direction = '退'
            steps = abs(self.to_row - self.from_row)
            return f"{piece_name}{col_name}{direction}{steps}"
        else:
            # 横向移动
            direction = '平'
            return f"{piece_name}{col_name}{direction}{target_col}"

    def copy(self):
        """创建走法的副本"""
        return Move(self.from_row, self.from_col, self.to_row, self.to_col,
                   self.piece, self.captured)
