"""
Master AI - 绝世棋圣
最强AI实现，包含所有高级优化技术
"""
import time
from app.ai.base_ai import BaseAI
from app.ai.evaluator import Evaluator


class MasterAI(BaseAI):
    """最强AI - 使用所有高级优化技术"""

    def __init__(self, color, depth=10, time_limit=60, quiescence_depth=8):
        super().__init__('绝世棋圣', color, 5)
        self.evaluator = Evaluator()
        self.max_depth = depth
        self.time_limit = time_limit
        self.quiescence_depth = quiescence_depth
        self.nodes_evaluated = 0
        self.transposition_table = {}
        self.killer_moves = {}  # 杀手走法表
        self.history_table = {}  # 历史启发式表
        self.start_time = 0
        self.pv_table = {}  # 主变例表

    def get_move(self, board, time_limit=None):
        """使用迭代加深和所有优化技术选择最佳走法"""
        self.reset_thinking_info()
        self.nodes_evaluated = 0
        self.transposition_table.clear()
        self.killer_moves.clear()
        self.pv_table.clear()
        self.start_time = time.time()

        if time_limit:
            self.time_limit = time_limit

        board_copy = board.copy()
        legal_moves = board_copy.get_legal_moves(self.color)
        if not legal_moves:
            return None

        best_move = None
        best_score = float('-inf')

        # 迭代加深搜索 - 使用渴望窗口
        aspiration_window = 50
        previous_score = 0

        for depth in range(1, self.max_depth + 1):
            if time.time() - self.start_time > self.time_limit * 0.85:
                break

            # 渴望窗口搜索
            alpha = previous_score - aspiration_window if depth > 1 else float('-inf')
            beta = previous_score + aspiration_window if depth > 1 else float('inf')

            current_best_move = None
            current_best_score = float('-inf')
            candidate_moves = []

            # 使用PV走法和历史启发式排序
            sorted_moves = self._order_moves_advanced(board_copy, legal_moves, depth, best_move)

            failed_low = False
            failed_high = False

            for move in sorted_moves:
                if time.time() - self.start_time > self.time_limit:
                    break

                captured = board_copy.make_move(move)

                # PVS搜索 (Principal Variation Search)
                if current_best_move is None:
                    score = -self._alpha_beta(board_copy, depth - 1, -beta, -alpha, False, depth)
                else:
                    # 零窗口搜索
                    score = -self._alpha_beta(board_copy, depth - 1, -alpha - 1, -alpha, False, depth)
                    if alpha < score < beta:
                        # 重新搜索
                        score = -self._alpha_beta(board_copy, depth - 1, -beta, -score, False, depth)

                board_copy.undo_move(move, captured)

                candidate_moves.append((move, score))

                if score > current_best_score:
                    current_best_score = score
                    current_best_move = move

                if score > alpha:
                    alpha = score

                if score >= beta:
                    failed_high = True
                    break

            # 渴望窗口失败处理
            if failed_high or (current_best_score <= previous_score - aspiration_window and depth > 1):
                # 重新搜索完整窗口
                alpha = float('-inf')
                beta = float('inf')
                current_best_move = None
                current_best_score = float('-inf')
                candidate_moves = []

                for move in sorted_moves:
                    if time.time() - self.start_time > self.time_limit:
                        break

                    captured = board_copy.make_move(move)
                    score = -self._alpha_beta(board_copy, depth - 1, -beta, -alpha, False, depth)
                    board_copy.undo_move(move, captured)

                    candidate_moves.append((move, score))

                    if score > current_best_score:
                        current_best_score = score
                        current_best_move = move

                    alpha = max(alpha, score)

            if current_best_move:
                best_move = current_best_move
                best_score = current_best_score
                previous_score = current_best_score

                # 更新PV表
                self.pv_table[0] = best_move

                candidate_moves.sort(key=lambda x: x[1], reverse=True)
                self.thinking_info['depth'] = depth
                self.thinking_info['nodes_evaluated'] = self.nodes_evaluated
                self.thinking_info['best_move'] = best_move
                self.thinking_info['score'] = best_score
                self.thinking_info['candidate_moves'] = candidate_moves[:5]

        return best_move

    def _alpha_beta(self, board, depth, alpha, beta, maximizing, root_depth):
        """Alpha-Beta搜索，包含所有优化"""
        self.nodes_evaluated += 1

        if time.time() - self.start_time > self.time_limit:
            return 0

        # 置换表查询
        board_hash = board.hash_value
        if board_hash in self.transposition_table:
            cached_depth, cached_score, cached_flag = self.transposition_table[board_hash]
            if cached_depth >= depth:
                if cached_flag == 'exact':
                    return cached_score
                elif cached_flag == 'lower' and cached_score >= beta:
                    return cached_score
                elif cached_flag == 'upper' and cached_score <= alpha:
                    return cached_score

        from app.core.rules import is_checkmate, is_in_check
        current_color = self.color if maximizing else ('black' if self.color == 'red' else 'red')

        # 检查将死
        if is_checkmate(board, current_color):
            score = (float('-inf') + (root_depth - depth) * 1000) if maximizing else (float('inf') - (root_depth - depth) * 1000)
            return score

        # 到达搜索深度
        if depth <= 0:
            return self._quiescence_search(board, alpha, beta, maximizing, self.quiescence_depth)

        legal_moves = board.get_legal_moves(current_color)
        if not legal_moves:
            return 0

        # 空着裁剪 (Null Move Pruning) - 不在被将军时使用
        if depth >= 3 and not is_in_check(board, current_color):
            # 跳过一步，看对方能否获得优势
            null_score = -self._alpha_beta(board, depth - 3, -beta, -beta + 1, not maximizing, root_depth)
            if null_score >= beta:
                return beta

        # 走法排序
        sorted_moves = self._order_moves_advanced(board, legal_moves, depth)

        original_alpha = alpha
        best_score = float('-inf') if maximizing else float('inf')
        best_move = None

        for i, move in enumerate(sorted_moves):
            captured = board.make_move(move)

            # Late Move Reduction (LMR)
            reduction = 0
            if i >= 4 and depth >= 3 and not move.captured and not is_in_check(board, 'black' if current_color == 'red' else 'red'):
                reduction = 1 if i < 10 else 2

            if maximizing:
                if reduction > 0:
                    score = -self._alpha_beta(board, depth - 1 - reduction, -beta, -alpha, False, root_depth)
                    if score > alpha:
                        score = -self._alpha_beta(board, depth - 1, -beta, -alpha, False, root_depth)
                else:
                    score = -self._alpha_beta(board, depth - 1, -beta, -alpha, False, root_depth)

                board.undo_move(move, captured)

                if score > best_score:
                    best_score = score
                    best_move = move

                alpha = max(alpha, score)
                if beta <= alpha:
                    # 更新杀手走法和历史表
                    self._update_killer_move(depth, move)
                    self._update_history(move, depth)
                    break
            else:
                if reduction > 0:
                    score = -self._alpha_beta(board, depth - 1 - reduction, -beta, -alpha, True, root_depth)
                    if score < beta:
                        score = -self._alpha_beta(board, depth - 1, -beta, -alpha, True, root_depth)
                else:
                    score = -self._alpha_beta(board, depth - 1, -beta, -alpha, True, root_depth)

                board.undo_move(move, captured)

                if score < best_score:
                    best_score = score
                    best_move = move

                beta = min(beta, score)
                if beta <= alpha:
                    self._update_killer_move(depth, move)
                    self._update_history(move, depth)
                    break

        # 存入置换表
        if best_score <= original_alpha:
            flag = 'upper'
        elif best_score >= beta:
            flag = 'lower'
        else:
            flag = 'exact'

        self.transposition_table[board_hash] = (depth, best_score, flag)

        return best_score

    def _order_moves_advanced(self, board, moves, depth, pv_move=None):
        """高级走法排序"""
        from app.core.rules import is_in_check, is_checkmate

        def move_priority(move):
            priority = 0

            # PV走法最高优先级
            if pv_move and move == pv_move:
                priority += 1000000

            # 杀手走法
            if depth in self.killer_moves:
                if move in self.killer_moves[depth]:
                    priority += 90000

            # 历史启发式
            move_key = (move.piece.type, move.from_row, move.from_col, move.to_row, move.to_col)
            if move_key in self.history_table:
                priority += self.history_table[move_key]

            # 执行走法检查战术价值
            captured = board.make_move(move)
            opponent_color = 'black' if self.color == 'red' else 'red'

            if is_checkmate(board, opponent_color):
                priority += 500000

            elif is_in_check(board, opponent_color):
                priority += 50000

            # 威胁将帅
            opponent_king = board.find_king(opponent_color)
            if opponent_king:
                distance = abs(move.to_row - opponent_king.row) + abs(move.to_col - opponent_king.col)
                if distance <= 2:
                    priority += 10000 - distance * 1000

            board.undo_move(move, captured)

            # 吃子 MVV-LVA
            if move.captured:
                captured_value = self.evaluator.piece_values.get(move.captured.type, 0)
                attacker_value = self.evaluator.piece_values.get(move.piece.type, 0)
                priority += captured_value * 100 - attacker_value

            # 进攻性走法
            if self.color == 'red' and move.to_row <= 4:
                priority += 100
            elif self.color == 'black' and move.to_row >= 5:
                priority += 100

            # 中心控制
            if 3 <= move.to_col <= 5:
                priority += 50

            return priority

        return sorted(moves, key=move_priority, reverse=True)

    def _update_killer_move(self, depth, move):
        """更新杀手走法表"""
        if depth not in self.killer_moves:
            self.killer_moves[depth] = []

        if move not in self.killer_moves[depth]:
            self.killer_moves[depth].insert(0, move)
            if len(self.killer_moves[depth]) > 2:
                self.killer_moves[depth].pop()

    def _update_history(self, move, depth):
        """更新历史启发式表"""
        move_key = (move.piece.type, move.from_row, move.from_col, move.to_row, move.to_col)
        if move_key not in self.history_table:
            self.history_table[move_key] = 0
        self.history_table[move_key] += depth * depth

    def _quiescence_search(self, board, alpha, beta, maximizing, depth):
        """静态搜索"""
        stand_pat = self.evaluator.evaluate(board)
        stand_pat = stand_pat if self.color == 'red' else -stand_pat

        if time.time() - self.start_time > self.time_limit:
            return stand_pat

        if depth <= 0:
            return stand_pat

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

        current_color = self.color if maximizing else ('black' if self.color == 'red' else 'red')
        legal_moves = board.get_legal_moves(current_color)
        tactical_moves = self._get_tactical_moves(board, legal_moves, current_color)

        if not tactical_moves:
            return stand_pat

        tactical_moves = self._order_moves_advanced(board, tactical_moves, 0)

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
        """获取战术走法"""
        from app.core.rules import is_in_check

        tactical_moves = []
        opponent_color = 'black' if color == 'red' else 'red'

        for move in moves:
            if move.captured:
                tactical_moves.append(move)
                continue

            captured = board.make_move(move)
            if is_in_check(board, opponent_color):
                tactical_moves.append(move)
            board.undo_move(move, captured)

        return tactical_moves
