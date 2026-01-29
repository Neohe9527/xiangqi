"""
随机 AI - 新手小卒
"""
import random
from app.ai.base_ai import BaseAI


class RandomAI(BaseAI):
    """具有基本走子常识的AI（优先吃子，避免丢子）"""

    def __init__(self, color):
        super().__init__('新手小卒', color, 1)
        # 棋子价值表
        self.piece_values = {
            'K': 10000,
            'R': 900,
            'C': 450,
            'H': 450,
            'A': 200,
            'E': 200,
            'P': 100
        }

    def get_move(self, board, time_limit=None):
        """
        选择走法，优先吃子和避免丢子

        Args:
            board: 棋盘对象
            time_limit: 时间限制（忽略）

        Returns:
            Move: 选择的走法
        """
        self.reset_thinking_info()

        # 获取所有合法走法
        legal_moves = board.get_legal_moves(self.color)

        if not legal_moves:
            return None

        # 评估每个走法
        move_scores = []
        for move in legal_moves:
            score = self._evaluate_move(board, move)
            move_scores.append((move, score))

        # 按分数排序
        move_scores.sort(key=lambda x: x[1], reverse=True)

        # 获取最高分数
        best_score = move_scores[0][1]

        # 从最高分的走法中随机选择一个
        best_moves = [m for m, s in move_scores if s == best_score]
        move = random.choice(best_moves)

        # 更新思考信息
        self.thinking_info['depth'] = 1
        self.thinking_info['nodes_evaluated'] = len(legal_moves)
        self.thinking_info['best_move'] = move
        self.thinking_info['score'] = best_score
        self.thinking_info['candidate_moves'] = move_scores[:5]

        return move

    def _evaluate_move(self, board, move):
        """
        评估走法的价值

        Args:
            board: 棋盘对象
            move: 走法

        Returns:
            float: 走法分数
        """
        score = 0

        # 1. 吃子价值（最高优先级）
        if move.captured:
            captured_value = self.piece_values.get(move.captured.type, 0)
            score += captured_value * 10

        # 2. 检查走法后是否会被吃（避免丢子）
        # 使用棋盘副本避免闪烁
        board_copy = board.copy()
        captured = board_copy.make_move(move)

        # 检查移动后的棋子是否会被对方吃掉
        piece = board_copy.get_piece(move.to_row, move.to_col)
        if piece:
            opponent_color = 'black' if self.color == 'red' else 'red'
            opponent_moves = board_copy.get_legal_moves(opponent_color)

            # 检查对方是否能吃掉这个棋子
            can_be_captured = False
            for opp_move in opponent_moves:
                if opp_move.to_row == move.to_row and opp_move.to_col == move.to_col:
                    can_be_captured = True
                    break

            # 如果会被吃，扣分
            if can_be_captured:
                piece_value = self.piece_values.get(piece.type, 0)
                score -= piece_value * 5

        # 3. 将军加分
        from app.core.rules import is_in_check
        opponent_color = 'black' if self.color == 'red' else 'red'
        if is_in_check(board_copy, opponent_color):
            score += 300

        # 4. 随机因子（避免完全确定性）
        score += random.uniform(-10, 10)

        return score
