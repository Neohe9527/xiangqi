"""
测试脚本 - 验证核心功能
"""
import sys
sys.path.insert(0, '/Users/hewei06/Desktop/code/games/xiangqi')

from core.board import Board
from core.rules import is_in_check, is_checkmate, get_game_result
from ai.random_ai import RandomAI
from ai.greedy_ai import GreedyAI
from ai.minimax_ai import MinimaxAI
from ai.alphabeta_ai import AlphaBetaAI


def test_board():
    """测试棋盘"""
    print("测试棋盘初始化...")
    board = Board()

    # 检查初始棋子数量
    assert len(board.red_pieces) == 16, "红方棋子数量错误"
    assert len(board.black_pieces) == 16, "黑方棋子数量错误"

    # 检查将帅位置
    red_king = board.find_king('red')
    black_king = board.find_king('black')
    assert red_king is not None, "找不到红方将"
    assert black_king is not None, "找不到黑方帅"
    assert red_king.row == 9 and red_king.col == 4, "红方将位置错误"
    assert black_king.row == 0 and black_king.col == 4, "黑方帅位置错误"

    print("✓ 棋盘测试通过")


def test_moves():
    """测试走法生成"""
    print("\n测试走法生成...")
    board = Board()

    # 获取红方所有合法走法
    red_moves = board.get_legal_moves('red')
    print(f"  红方初始合法走法数: {len(red_moves)}")
    assert len(red_moves) > 0, "红方没有合法走法"

    # 获取黑方所有合法走法
    black_moves = board.get_legal_moves('black')
    print(f"  黑方初始合法走法数: {len(black_moves)}")
    assert len(black_moves) > 0, "黑方没有合法走法"

    print("✓ 走法生成测试通过")


def test_ai():
    """测试AI"""
    print("\n测试AI...")
    board = Board()

    # 测试随机AI
    print("  测试随机AI...")
    random_ai = RandomAI('red')
    move = random_ai.get_move(board)
    assert move is not None, "随机AI没有返回走法"
    print(f"    随机AI选择: {move}")

    # 测试贪心AI
    print("  测试贪心AI...")
    greedy_ai = GreedyAI('red')
    move = greedy_ai.get_move(board)
    assert move is not None, "贪心AI没有返回走法"
    print(f"    贪心AI选择: {move}")

    # 测试MinimaxAI
    print("  测试MinimaxAI (深度2)...")
    minimax_ai = MinimaxAI('red', depth=2)
    move = minimax_ai.get_move(board)
    assert move is not None, "MinimaxAI没有返回走法"
    info = minimax_ai.get_thinking_info()
    print(f"    MinimaxAI选择: {move}")
    print(f"    评估节点数: {info['nodes_evaluated']}")

    # 测试AlphaBetaAI
    print("  测试AlphaBetaAI (深度3)...")
    alphabeta_ai = AlphaBetaAI('red', depth=3, time_limit=5)
    move = alphabeta_ai.get_move(board)
    assert move is not None, "AlphaBetaAI没有返回走法"
    info = alphabeta_ai.get_thinking_info()
    print(f"    AlphaBetaAI选择: {move}")
    print(f"    搜索深度: {info['depth']}")
    print(f"    评估节点数: {info['nodes_evaluated']}")
    print(f"    评分: {info['score']}")

    print("✓ AI测试通过")


def test_game_flow():
    """测试游戏流程"""
    print("\n测试游戏流程...")
    board = Board()

    # 模拟几步棋
    moves_played = 0
    max_moves = 10

    for i in range(max_moves):
        color = 'red' if i % 2 == 0 else 'black'
        legal_moves = board.get_legal_moves(color)

        if not legal_moves:
            print(f"  第{i+1}步: {color}方无合法走法")
            break

        # 选择第一个合法走法
        move = legal_moves[0]
        captured = board.make_move(move)
        moves_played += 1

        print(f"  第{i+1}步: {color}方 {move.to_chinese()}")

        # 检查游戏结果
        next_color = 'black' if color == 'red' else 'red'
        result = get_game_result(board, next_color)
        if result != 'ongoing':
            print(f"  游戏结束: {result}")
            break

    print(f"✓ 游戏流程测试通过 (执行了{moves_played}步)")


def main():
    """运行所有测试"""
    print("=" * 50)
    print("中国象棋游戏 - 核心功能测试")
    print("=" * 50)

    try:
        test_board()
        test_moves()
        test_ai()
        test_game_flow()

        print("\n" + "=" * 50)
        print("✓ 所有测试通过！")
        print("=" * 50)
        print("\n游戏已准备就绪，可以运行: python3 main.py")

    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
