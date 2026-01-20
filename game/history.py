"""
走棋历史记录
"""


class History:
    """走棋历史管理"""

    def __init__(self):
        """初始化历史记录"""
        self.moves = []  # 走法列表
        self.captured_pieces = []  # 被吃棋子列表

    def add_move(self, move, captured_piece):
        """
        添加一步棋

        Args:
            move: Move 对象
            captured_piece: 被吃的棋子（如果有）
        """
        self.moves.append(move)
        self.captured_pieces.append(captured_piece)

    def undo_last_move(self):
        """
        撤销最后一步棋

        Returns:
            tuple: (move, captured_piece) 或 None
        """
        if not self.moves:
            return None

        move = self.moves.pop()
        captured_piece = self.captured_pieces.pop()
        return move, captured_piece

    def get_last_move(self):
        """
        获取最后一步棋

        Returns:
            Move: 最后一步棋，如果没有则返回 None
        """
        if self.moves:
            return self.moves[-1]
        return None

    def get_move_count(self):
        """获取总步数"""
        return len(self.moves)

    def get_moves(self):
        """获取所有走法"""
        return self.moves.copy()

    def clear(self):
        """清空历史记录"""
        self.moves.clear()
        self.captured_pieces.clear()

    def get_move_list_text(self, max_moves=10):
        """
        获取走法列表的文本表示（用于UI显示）

        Args:
            max_moves: 最多显示的步数

        Returns:
            list: 走法文本列表
        """
        result = []
        start_index = max(0, len(self.moves) - max_moves)

        for i in range(start_index, len(self.moves)):
            move = self.moves[i]
            move_num = i + 1

            # 每两步为一回合
            if i % 2 == 0:
                text = f"{move_num // 2 + 1}. {move.to_chinese()}"
            else:
                text = f"   {move.to_chinese()}"

            result.append(text)

        return result

    def __repr__(self):
        return f"History({len(self.moves)} moves)"
