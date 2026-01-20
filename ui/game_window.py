"""
主游戏窗口
"""
import pygame
import threading
import config
from game.game_manager import GameManager
from ui.board_renderer import BoardRenderer
from ui.piece_renderer import PieceRenderer
from ui.info_panel import InfoPanel
from ui.menu import Menu, GameModeDialog, GameOverDialog


class GameWindow:
    """主游戏窗口"""

    def __init__(self):
        """初始化游戏窗口"""
        pygame.init()

        # 创建窗口
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption("中国象棋 - Chinese Chess")

        # 时钟
        self.clock = pygame.time.Clock()

        # 游戏管理器
        self.game_manager = GameManager()

        # 渲染器
        self.board_renderer = BoardRenderer(self.screen, 0, 0)
        self.piece_renderer = PieceRenderer(self.screen, self.board_renderer)

        # 信息面板
        panel_x = config.BOARD_WIDTH + 20
        panel_y = 100
        panel_width = config.WINDOW_WIDTH - config.BOARD_WIDTH - 40
        panel_height = config.WINDOW_HEIGHT - 120
        self.info_panel = InfoPanel(self.screen, panel_x, panel_y, panel_width, panel_height)

        # 菜单（移到右侧信息面板区域）
        menu_x = config.BOARD_WIDTH + 40
        menu_y = 20
        self.menu = Menu(self.screen, menu_x, menu_y)
        self.menu.add_button("新游戏", self._new_game)
        self.menu.add_button("悔棋", self._undo_move)
        self.menu.add_button("重置", self._reset_game)

        # 游戏模式对话框
        self.mode_dialog = GameModeDialog(self.screen)

        # 游戏结束对话框
        self.game_over_dialog = GameOverDialog(self.screen)
        self.game_over_shown = False  # 标记游戏结束对话框是否已显示

        # AI线程
        self.ai_thread = None
        self.ai_thinking = False
        self.ai_move = None

        # 运行标志
        self.running = True

        # 显示初始对话框
        self.mode_dialog.show()

    def _new_game(self):
        """新游戏"""
        self.mode_dialog.show()

    def _undo_move(self):
        """悔棋"""
        if self.game_manager.game_result == 'ongoing' and not self.ai_thinking:
            # 人机对弈时悔两步
            if self.game_manager.game_mode == config.MODE_HUMAN_VS_AI:
                self.game_manager.undo_move(steps=2)
            else:
                self.game_manager.undo_move(steps=1)

    def _reset_game(self):
        """重置游戏"""
        if not self.ai_thinking:
            self.game_manager.reset_game()
            self.game_over_shown = False  # 重置游戏结束标志

    def _start_ai_thinking(self):
        """在新线程中启动AI思考"""
        if self.ai_thinking:
            return

        self.ai_thinking = True
        self.ai_move = None

        def ai_think():
            move = self.game_manager.get_ai_move()
            self.ai_move = move
            self.ai_thinking = False

        self.ai_thread = threading.Thread(target=ai_think, daemon=True)
        self.ai_thread.start()

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # 游戏结束对话框事件（优先处理）
            if self.game_over_dialog.active:
                result = self.game_over_dialog.handle_event(event)
                if result:
                    # 按钮被点击，检查是否需要显示新游戏对话框
                    if self.game_over_dialog.on_new_game:
                        self.mode_dialog.show()
                    continue
                # 对话框活跃但没有点击按钮，阻止其他事件处理
                continue

            # 对话框事件
            if self.mode_dialog.handle_event(event):
                # 检查是否选择了游戏模式
                selection = self.mode_dialog.get_selection()
                if selection:
                    self.game_manager.setup_game(
                        selection['mode'],
                        selection['red_player'],
                        selection['black_player'],
                        selection['red_ai'],
                        selection['black_ai']
                    )
                    self.game_over_shown = False  # 重置游戏结束标志
                continue

            # 菜单事件
            if self.menu.handle_event(event):
                continue

            # 棋盘点击事件
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.mode_dialog.active and not self.game_over_dialog.active:
                    self._handle_board_click(event.pos)

    def _handle_board_click(self, pos):
        """处理棋盘点击"""
        board_pos = self.board_renderer.get_board_pos(pos[0], pos[1])
        if board_pos:
            row, col = board_pos
            self.game_manager.handle_click(row, col)

    def update(self):
        """更新游戏状态"""
        # 如果模式选择对话框活跃，暂停游戏逻辑
        if self.mode_dialog.active:
            return

        # 检查游戏是否结束（只显示一次对话框）
        if self.game_manager.game_result != 'ongoing' and not self.game_over_shown:
            # 获取获胜方名称
            winner = None
            if self.game_manager.game_result == 'red_win':
                player = self.game_manager.red_player
                if player and player.player_type == 'ai':
                    winner = player.ai.name
                else:
                    winner = "人类玩家"
            elif self.game_manager.game_result == 'black_win':
                player = self.game_manager.black_player
                if player and player.player_type == 'ai':
                    winner = player.ai.name
                else:
                    winner = "人类玩家"

            # 显示游戏结束对话框
            self.game_over_dialog.show(self.game_manager.game_result, winner)
            self.game_over_shown = True
            return

        # 如果游戏结束对话框活跃，暂停游戏逻辑
        if self.game_over_dialog.active:
            return

        # 如果AI思考完成，先执行走法
        if self.ai_move is not None and not self.ai_thinking:
            self.game_manager.make_move(self.ai_move)
            self.ai_move = None

        # 如果游戏正在进行且当前是AI回合
        elif (self.game_manager.game_result == 'ongoing' and
              self.game_manager.is_current_player_ai() and
              not self.ai_thinking and
              self.ai_move is None):

            # 启动AI思考
            self._start_ai_thinking()

    def draw(self):
        """绘制游戏画面"""
        # 清空屏幕
        self.screen.fill((255, 255, 255))

        # 绘制棋盘
        self.board_renderer.draw(self.game_manager)

        # 绘制棋子
        self.piece_renderer.draw(self.game_manager.board)

        # 绘制信息面板
        self.info_panel.draw(self.game_manager)

        # 绘制菜单
        self.menu.draw()

        # 绘制对话框
        self.mode_dialog.draw()

        # 绘制游戏结束对话框
        self.game_over_dialog.draw()

        # 更新显示
        pygame.display.flip()

    def run(self):
        """运行游戏主循环"""
        while self.running:
            # 处理事件
            self.handle_events()

            # 更新游戏状态
            self.update()

            # 绘制画面
            self.draw()

            # 控制帧率
            self.clock.tick(config.FPS)

        pygame.quit()
