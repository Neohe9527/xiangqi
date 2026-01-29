"""
Alpha-Beta AI - 深算国手
"""
import time
from app.ai.base_ai import BaseAI
from app.ai.evaluator import Evaluator


class AlphaBetaAI(BaseAI):
    """使用 Alpha-Beta 剪枝算法的高级 AI"""

    def __init__(self, color, depth=3, time_limit=3):
        super().__init__('深算国手', color, 4)
        self.evaluator = Evaluator()
        self.max_depth = depth
        self.time_limit = time_limit
        self.nodes_evaluated = 0
        self.transposition_table = {}  # 置换表
        self.start_time = 0

    def get_move(self, board, time_limit=None):
        """
        使用 Alpha-Beta 剪枝和迭代加深选择最佳走法

        Args:
            board: 棋盘对象
            time_limit: 时间限制（秒）

        Returns:
            Move: 最佳走法
        """
        self.reset_thinking_info()
        self.nodes_evaluated = 0
        self.transposition_table.clear()
        self.start_time = time.time()

        if time_limit:
            self.time_limit = time_limit

        # 重要：使用棋盘副本，避免修改原始棋盘导致UI闪烁
        board_copy = board.copy()
        legal_moves = board_copy.get_legal_moves(self.color)
        if not legal_moves:
            return None

        best_move = None
        best_score = float('-inf')

        # 迭代加深搜索
        for depth in range(1, self.max_depth + 1):
            if time.time() - self.start_time > self.time_limit * 0.9:
                break

            current_best_move = None
            current_best_score = float('-inf')
            candidate_moves = []

            # 走法排序（使用上一次迭代的结果）
            sorted_moves = self._order_moves(board_copy, legal_moves, best_move)

            for move in sorted_moves:
                if time.time() - self.start_time > self.time_limit:
                    break

                captured = board_copy.make_move(move)

                score = self._alpha_beta(
                    board_copy, depth - 1, float('-inf'), float('inf'), False
                )

                board_copy.undo_move(move, captured)

                candidate_moves.append((move, score))

                if score > current_best_score:
                    current_best_score = score
                    current_best_move = move

            if current_best_move:
                best_move = current_best_move
                best_score = current_best_score

                # 更新思考信息
                candidate_moves.sort(key=lambda x: x[1], reverse=True)
                self.thinking_info['depth'] = depth
                self.thinking_info['nodes_evaluated'] = self.nodes_evaluated
                self.thinking_info['best_move'] = best_move
                self.thinking_info['score'] = best_score
                self.thinking_info['candidate_moves'] = candidate_moves[:5]

        return best_move

    def _alpha_beta(self, board, depth, alpha, beta, maximizing):
        """
        Alpha-Beta 剪枝算法

        Args:
            board: 棋盘对象
            depth: 搜索深度
            alpha: Alpha 值
            beta: Beta 值
            maximizing: 是否是最大化节点

        Returns:
            float: 评分
        """
        self.nodes_evaluated += 1

        # 检查时间限制
        if time.time() - self.start_time > self.time_limit:
            return 0

        # 查置换表
        board_hash = board.hash_value
        if board_hash in self.transposition_table:
            cached_depth, cached_score = self.transposition_table[board_hash]
            if cached_depth >= depth:
                return cached_score

        # 检查游戏是否结束（优先检查，确保AI能识别胜负）
        from app.core.rules import is_checkmate, get_game_result
        current_color = self.color if maximizing else ('black' if self.color == 'red' else 'red')

        # 检查是否被将死
        if is_checkmate(board, current_color):
            # 被将死的一方，距离越近惩罚越大（鼓励AI尽快获胜或尽量拖延失败）
            score = (float('-inf') + depth * 1000) if maximizing else (float('inf') - depth * 1000)
            self.transposition_table[board_hash] = (depth, score)
            return score

        # 到达搜索深度，进行杀棋搜索
        if depth == 0:
            # 使用杀棋搜索而不是直接评估
            return self._quiescence_search(board, alpha, beta, maximizing, 4)

        legal_moves = board.get_legal_moves(current_color)
        if not legal_moves:
            # 无子可走但未被将死，判和
            self.transposition_table[board_hash] = (depth, 0)
            return 0

        # 走法排序
        sorted_moves = self._order_moves(board, legal_moves)

        if maximizing:
            max_eval = float('-inf')
            for move in sorted_moves:
                captured = board.make_move(move)
                eval_score = self._alpha_beta(board, depth - 1, alpha, beta, False)
                board.undo_move(move, captured)

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                if beta <= alpha:
                    break  # Beta 剪枝

            self.transposition_table[board_hash] = (depth, max_eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in sorted_moves:
                captured = board.make_move(move)
                eval_score = self._alpha_beta(board, depth - 1, alpha, beta, True)
                board.undo_move(move, captured)

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                if beta <= alpha:
                    break  # Alpha 剪枝

            self.transposition_table[board_hash] = (depth, min_eval)
            return min_eval

    def _order_moves(self, board, moves, best_move=None):
        """
        走法排序，提高剪枝效率

        优先级：
        1. 上次迭代的最佳走法
        2. 将死对方的走法（最高优先级）
        3. 吃子走法（按被吃棋子价值排序）
        4. 将军走法
        5. 进攻性走法（威胁对方将帅）
        6. 其他走法

        Args:
            board: 棋盘对象
            moves: 走法列表
            best_move: 上次迭代的最佳走法

        Returns:
            list: 排序后的走法列表
        """
        from app.core.rules import is_in_check, is_checkmate

        def move_priority(move):
            priority = 0

            # 上次迭代的最佳走法
            if best_move and move == best_move:
                priority += 100000

            # 执行走法
            captured = board.make_move(move)
            opponent_color = 'black' if self.color == 'red' else 'red'

            # 将死对方（最高优先级）
            if is_checkmate(board, opponent_color):
                priority += 50000

            # 将军走法
            elif is_in_check(board, opponent_color):
                priority += 5000

            # 威胁对方将帅（距离将帅3格内）
            opponent_king = board.find_king(opponent_color)
            if opponent_king:
                distance = abs(move.to_row - opponent_king.row) + abs(move.to_col - opponent_king.col)
                if distance <= 3:
                    priority += 1000 - distance * 100  # 距离越近优先级越高

            board.undo_move(move, captured)

            # 吃子走法
            if move.captured:
                captured_value = self.evaluator.piece_values.get(move.captured.type, 0)
                attacker_value = self.evaluator.piece_values.get(move.piece.type, 0)
                # MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
                priority += captured_value * 100 - attacker_value

            # 进攻性走法（进入对方半场）
            if self.color == 'red' and move.to_row <= 4:
                priority += 50
            elif self.color == 'black' and move.to_row >= 5:
                priority += 50

            # 控制中心
            if 3 <= move.to_col <= 5:
                priority += 30

            return priority

        return sorted(moves, key=move_priority, reverse=True)

    def _quiescence_search(self, board, alpha, beta, maximizing, depth):
        """
        杀棋搜索（Quiescence Search）
        在叶子节点继续搜索吃子和将军走法，避免水平线效应

        Args:
            board: 棋盘对象
            alpha: Alpha 值
            beta: Beta 值
            maximizing: 是否是最大化节点
            depth: 剩余搜索深度

        Returns:
            float: 评分
        """
        # 先进行静态评估
        stand_pat = self.evaluator.evaluate(board)
        stand_pat = stand_pat if self.color == 'red' else -stand_pat

        # 检查时间限制
        if time.time() - self.start_time > self.time_limit:
            return stand_pat

        # 达到杀棋搜索深度限制
        if depth <= 0:
            return stand_pat

        # Beta 剪枝
        if maximizing:
            if stand_pat >= beta:
                return beta
            if stand_pat > alpha:
                alpha = stand_pat
        else:
            if stand_pat <= alpha:
                return alpha
            if stand_pat < beta:
                beta = stand_pat

        # 获取当前玩家
        current_color = self.color if maximizing else ('black' if self.color == 'red' else 'red')

        # 只搜索吃子和将军走法
        legal_moves = board.get_legal_moves(current_color)
        tactical_moves = self._get_tactical_moves(board, legal_moves, current_color)

        # 如果没有战术走法，返回静态评估
        if not tactical_moves:
            return stand_pat

        # 对战术走法排序
        tactical_moves = self._order_moves(board, tactical_moves)

        if maximizing:
            max_eval = stand_pat
            for move in tactical_moves:
                captured = board.make_move(move)
                eval_score = self._quiescence_search(board, alpha, beta, False, depth - 1)
                board.undo_move(move, captured)

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                if beta <= alpha:
                    break

            return max_eval
        else:
            min_eval = stand_pat
            for move in tactical_moves:
                captured = board.make_move(move)
                eval_score = self._quiescence_search(board, alpha, beta, True, depth - 1)
                board.undo_move(move, captured)

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                if beta <= alpha:
                    break

            return min_eval

    def _get_tactical_moves(self, board, moves, color):
        """
        获取战术走法（吃子和将军）

        Args:
            board: 棋盘对象
            moves: 所有合法走法
            color: 当前颜色

        Returns:
            list: 战术走法列表
        """
        from app.core.rules import is_in_check

        tactical_moves = []
        opponent_color = 'black' if color == 'red' else 'red'

        for move in moves:
            # 吃子走法
            if move.captured:
                tactical_moves.append(move)
                continue

            # 将军走法
            captured = board.make_move(move)
            if is_in_check(board, opponent_color):
                tactical_moves.append(move)
            board.undo_move(move, captured)

        return tactical_moves

