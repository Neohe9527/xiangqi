"""
Minimax AI - 谋略军师
"""
from app.ai.base_ai import BaseAI
from app.ai.evaluator import Evaluator


class MinimaxAI(BaseAI):
    """使用 Minimax 算法的 AI"""

    def __init__(self, color, depth=3):
        super().__init__('谋略军师', color, 3)
        self.evaluator = Evaluator()
        self.max_depth = depth
        self.nodes_evaluated = 0

    def get_move(self, board, time_limit=None):
        """
        使用 Minimax 算法选择最佳走法

        Args:
            board: 棋盘对象
            time_limit: 时间限制（暂未实现）

        Returns:
            Move: 最佳走法
        """
        self.reset_thinking_info()
        self.nodes_evaluated = 0

        # 重要：使用棋盘副本，避免修改原始棋盘导致UI闪烁
        board_copy = board.copy()
        legal_moves = board_copy.get_legal_moves(self.color)
        if not legal_moves:
            return None

        best_move = None
        best_score = float('-inf')
        candidate_moves = []

        # 评估每个走法
        for move in legal_moves:
            captured = board_copy.make_move(move)

            # Minimax 搜索
            score = self._minimax(board_copy, self.max_depth - 1, False)

            board_copy.undo_move(move, captured)

            candidate_moves.append((move, score))

            if score > best_score:
                best_score = score
                best_move = move

        # 更新思考信息
        candidate_moves.sort(key=lambda x: x[1], reverse=True)
        self.thinking_info['depth'] = self.max_depth
        self.thinking_info['nodes_evaluated'] = self.nodes_evaluated
        self.thinking_info['best_move'] = best_move
        self.thinking_info['score'] = best_score
        self.thinking_info['candidate_moves'] = candidate_moves[:5]

        return best_move

    def _minimax(self, board, depth, maximizing):
        """
        Minimax 算法

        Args:
            board: 棋盘对象
            depth: 搜索深度
            maximizing: 是否是最大化节点

        Returns:
            float: 评分
        """
        self.nodes_evaluated += 1

        # 到达搜索深度或游戏结束
        if depth == 0:
            score = self.evaluator.evaluate(board)
            return score if self.color == 'red' else -score

        # 检查游戏是否结束
        from app.core.rules import is_checkmate
        current_color = self.color if maximizing else ('black' if self.color == 'red' else 'red')

        if is_checkmate(board, current_color):
            # 被将死，返回极端分数
            return float('-inf') if maximizing else float('inf')

        legal_moves = board.get_legal_moves(current_color)
        if not legal_moves:
            # 无子可动（僵局）
            return 0

        if maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                captured = board.make_move(move)
                eval_score = self._minimax(board, depth - 1, False)
                board.undo_move(move, captured)
                max_eval = max(max_eval, eval_score)
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                captured = board.make_move(move)
                eval_score = self._minimax(board, depth - 1, True)
                board.undo_move(move, captured)
                min_eval = min(min_eval, eval_score)
            return min_eval
