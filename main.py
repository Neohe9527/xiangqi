"""
中国象棋游戏 - 主程序入口

支持功能：
- 人机对弈
- AI vs AI 对弈
- 多种AI难度（新手小卒、贪心将军、谋略军师、深算国手）
- 悔棋功能
- AI思考过程可视化
- 走棋历史记录
"""
import sys
from ui.game_window import GameWindow


def main():
    """主函数"""
    try:
        # 创建并运行游戏窗口
        game = GameWindow()
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
