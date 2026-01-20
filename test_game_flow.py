"""
调试脚本 - 测试完整的游戏流程
"""
import sys
sys.path.insert(0, '/Users/hewei06/Desktop/code/games/xiangqi')

from game.game_manager import GameManager
import time

print('=' * 50)
print('测试完整游戏流程')
print('=' * 50)
print()

# 创建游戏管理器
gm = GameManager()

# 设置游戏（人类 vs AI）
print('设置游戏: 人类(红) vs AI(黑)')
gm.setup_game('human_vs_ai', 'human', 'ai', 'random', 'alphabeta')
print(f'红方: {gm.red_player}')
print(f'黑方: {gm.black_player}')
print()

# 人类走第一步
print('人类(红方)走第一步...')
legal_moves = gm.board.get_legal_moves('red')
first_move = legal_moves[0]
print(f'选择走法: {first_move}')
success = gm.make_move(first_move)
print(f'走法执行: {"成功" if success else "失败"}')
print(f'当前轮到: {gm.current_color}')
print(f'是否AI回合: {gm.is_current_player_ai()}')
print()

# AI思考
print('AI(黑方)开始思考...')
start_time = time.time()
ai_move = gm.get_ai_move()
end_time = time.time()

print(f'AI思考完成')
print(f'思考时间: {end_time - start_time:.2f} 秒')
print(f'AI选择: {ai_move}')
print()

if ai_move:
    print('执行AI走法...')
    success = gm.make_move(ai_move)
    print(f'走法执行: {"成功" if success else "失败"}')
    print(f'当前轮到: {gm.current_color}')
    print()
    print('✓ 游戏流程正常')
else:
    print('✗ AI没有返回走法！')
