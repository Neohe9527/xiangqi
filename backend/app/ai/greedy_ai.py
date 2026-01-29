"""
贪心 AI - 贪心将军
"""
from app.ai.base_ai import BaseAI
from app.ai.evaluator import Evaluator


class GreedyAI(BaseAI):
    """贪心算法 AI，优先吃子"""

    def __init__(self, color):
        super().__init__('贪心将军', color, 2)
        self.evaluator = Evaluator()

    def get_move(self, board, time_limit=None):
        """
        评估所有走法，选择评分最高的

        优先级：吃子 > 威胁对方 > 保护己方

        Args:
            board: 棋盘对象
            time_limit: 时间限制（忽略）

        Returns:
            Move: 最佳走法
        """
        self.reset_thinking_info()

        # 重要：使用棋盘副本，避免修改原始棋盘导致UI闪烁
        board_copy = board.copy()
        legal_moves = board_copy.get_legal_moves(self.color)

        if not legal_moves:
            return None

        # 评估每个走法
        move_scores = []
        for move in legal_moves:
            score = self._evaluate_move(board_copy, move)
            move_scores.append((move, score))

        # 按评分排序
        move_scores.sort(key=lambda x: x[1], reverse=True)

        # 更新思考信息
        best_move, best_score = move_scores[0]
        self.thinking_info['depth'] = 1
        self.thinking_info['nodes_evaluated'] = len(legal_moves)
        self.thinking_info['best_move'] = best_move
        self.thinking_info['score'] = best_score
        self.thinking_info['candidate_moves'] = move_scores[:5]

        return best_move

    def _evaluate_move(self, board, move):
        """
        评估单个走法

        Args:
            board: 棋盘对象
            move: Move 对象

        Returns:
            float: 评分
        """
        score = 0

        # 1. 吃子得分（最高优先级）
        if move.captured:
            captured_value = self.evaluator.piece_values.get(move.captured.type, 0)
            score += captured_value * 10  # 吃子权重很高

        # 2. 执行走法后的局面评估
        captured = board.make_move(move)

        # 评估局面
        position_score = self.evaluator.evaluate(board)
        if self.color == 'red':
            score += position_score
        else:
            score -= position_score

        # 3. 检查是否将军
        from app.core.rules import is_in_check
        opponent_color = 'black' if self.color == 'red' else 'red'
        if is_in_check(board, opponent_color):
            score += 100  # 将军有额外奖励

        # 撤销走法
        board.undo_move(move, captured)

        return score
