"""
游戏规则：将军、将死等判定
"""


def is_in_check(board, color):
    """
    判断某方是否被将军

    Args:
        board: 棋盘对象
        color: 'red' or 'black'

    Returns:
        bool: 是否被将军
    """
    king = board.find_king(color)
    if not king:
        return False

    # 检查对方所有棋子是否能攻击到己方的将/帅
    opponent_color = 'black' if color == 'red' else 'red'
    opponent_pieces = board.get_all_pieces(opponent_color)

    for piece in opponent_pieces:
        possible_moves = piece.get_possible_moves(board)
        for move in possible_moves:
            if move.to_row == king.row and move.to_col == king.col:
                return True

    # 特殊规则：检查将帅是否对面
    opponent_king = board.find_king(opponent_color)
    if opponent_king and king.col == opponent_king.col:
        # 同一列，检查中间是否有棋子
        min_row = min(king.row, opponent_king.row)
        max_row = max(king.row, opponent_king.row)
        has_piece_between = False
        for row in range(min_row + 1, max_row):
            if board.get_piece(row, king.col) is not None:
                has_piece_between = True
                break
        if not has_piece_between:
            return True

    return False


def is_legal_move(board, move, color):
    """
    判断走法是否合法（不会导致己方被将军）

    Args:
        board: 棋盘对象
        move: Move 对象
        color: 'red' or 'black'

    Returns:
        bool: 是否合法
    """
    # 执行走法
    captured = board.make_move(move)

    # 检查是否导致己方被将军
    in_check = is_in_check(board, color)

    # 撤销走法
    board.undo_move(move, captured)

    return not in_check


def is_checkmate(board, color):
    """
    判断某方是否被将死

    Args:
        board: 棋盘对象
        color: 'red' or 'black'

    Returns:
        bool: 是否被将死
    """
    # 如果没有被将军，就不是将死
    if not is_in_check(board, color):
        return False

    # 检查是否有任何合法走法可以解除将军
    legal_moves = board.get_legal_moves(color)
    return len(legal_moves) == 0


def is_stalemate(board, color):
    """
    判断是否僵局（无子可动但未被将军）

    Args:
        board: 棋盘对象
        color: 'red' or 'black'

    Returns:
        bool: 是否僵局
    """
    # 如果被将军，就不是僵局
    if is_in_check(board, color):
        return False

    # 检查是否有任何合法走法
    legal_moves = board.get_legal_moves(color)
    return len(legal_moves) == 0


def get_game_result(board, current_color):
    """
    获取游戏结果

    Args:
        board: 棋盘对象
        current_color: 当前轮到的颜色

    Returns:
        str: 'red_win', 'black_win', 'draw', 'ongoing'
    """
    if is_checkmate(board, current_color):
        # 当前方被将死，对方获胜
        return 'black_win' if current_color == 'red' else 'red_win'

    if is_stalemate(board, current_color):
        # 僵局，和棋
        return 'draw'

    # 检查是否只剩将帅（简化的和棋判定）
    red_pieces = board.get_all_pieces('red')
    black_pieces = board.get_all_pieces('black')

    if len(red_pieces) == 1 and len(black_pieces) == 1:
        # 双方都只剩将帅
        return 'draw'

    return 'ongoing'
