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
from ui.animation import AnimationManager, PieceAnimation
from ui.sound_manager import SoundManager
from ui.piece_images import PieceImageGenerator


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

        # 动画管理器
        self.animation_manager = AnimationManager()

        # 音效管理器
        try:
            self.sound_manager = SoundManager()
        except Exception as e:
            print(f"音效初始化失败: {e}")
            self.sound_manager = None

        # 棋子图片生成器
        try:
            self.piece_image_generator = PieceImageGenerator()
        except Exception as e:
            print(f"棋子图片生成失败: {e}")
            self.piece_image_generator = None

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
        # 如果有动画正在播放，不处理点击
        if self.animation_manager.has_active_animations():
            return

        board_pos = self.board_renderer.get_board_pos(pos[0], pos[1])
        if board_pos:
            row, col = board_pos
            result = self.game_manager.handle_click(row, col)

            # 如果成功执行了走法，播放音效
            if result and self.sound_manager:
                # 检查是否吃子
                last_move = self.game_manager.last_move
                if last_move and last_move.captured_piece:
                    self.sound_manager.play('capture')
                else:
                    self.sound_manager.play('move')

                # 检查是否将军
                if self.game_manager.is_in_check():
                    self.sound_manager.play('check')

    def update(self):
        """更新游戏状态"""
        # 更新动画
        self.animation_manager.update()

        # 如果模式选择对话框活跃，暂停游戏逻辑
        if self.mode_dialog.active:
            return

        # 检查游戏是否结束（只显示一次对话框）
        if self.game_manager.game_result != 'ongoing' and not self.game_over_shown:
            # 播放胜利音效
            if self.sound_manager:
                self.sound_manager.play('win')

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

        # 如果有动画正在播放，不执行AI移动
        if self.animation_manager.has_active_animations():
            return

        # 如果AI思考完成，先执行走法
        if self.ai_move is not None and not self.ai_thinking:
            # 创建移动动画
            move = self.ai_move
            piece = self.game_manager.board.get_piece(move.from_row, move.from_col)
            if piece:
                from_pos = self.board_renderer.get_screen_pos(move.from_row, move.from_col)
                to_pos = self.board_renderer.get_screen_pos(move.to_row, move.to_col)
                animation = PieceAnimation(piece, from_pos, to_pos, duration=0.3)
                self.animation_manager.add_animation(animation)

            # 执行走法
            self.game_manager.make_move(self.ai_move)

            # 播放音效
            if self.sound_manager:
                if self.ai_move.captured_piece:
                    self.sound_manager.play('capture')
                else:
                    self.sound_manager.play('move')

                if self.game_manager.is_in_check():
                    self.sound_manager.play('check')

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

        # 绘制棋子（包括动画中的棋子）
        self._draw_pieces_with_animation()

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

    def _draw_pieces_with_animation(self):
        """绘制棋子（包括动画）"""
        # 获取所有活跃的动画
        active_animations = self.animation_manager.get_active_animations()
        animating_pieces = [anim.piece for anim in active_animations]

        # 绘制非动画棋子
        for piece in self.game_manager.board.get_all_pieces():
            if piece not in animating_pieces:
                self.piece_renderer._draw_piece(piece)

        # 绘制动画中的棋子
        for animation in active_animations:
            current_pos = animation.update()
            if current_pos:
                x, y = current_pos
                piece = animation.piece

                # 使用图片渲染器绘制棋子（如果可用）
                if self.piece_image_generator:
                    image = self.piece_image_generator.get_piece_image(piece.color, piece.piece_type)
                    if image:
                        image_rect = image.get_rect(center=(int(x), int(y)))
                        self.screen.blit(image, image_rect)
                    else:
                        # 回退到原始渲染
                        self._draw_piece_at_position(piece, x, y)
                else:
                    self._draw_piece_at_position(piece, x, y)

    def _draw_piece_at_position(self, piece, x, y):
        """在指定位置绘制棋子"""
        piece_color = config.PIECE_COLORS[piece.color]
        bg_color = config.PIECE_BG_COLORS[piece.color]
        border_color = config.PIECE_BORDER_COLORS[piece.color]

        # 绘制棋子背景
        pygame.draw.circle(self.screen, bg_color, (int(x), int(y)), config.PIECE_RADIUS)

        # 绘制边框
        pygame.draw.circle(self.screen, border_color, (int(x), int(y)), config.PIECE_RADIUS, 4)

        # 绘制文字
        text = piece.get_chinese_name()
        try:
            font = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 32)
        except:
            try:
                font = pygame.font.SysFont('simhei', 32)
            except:
                font = pygame.font.Font(None, 36)

        text_surface = font.render(text, True, piece_color)
        text_rect = text_surface.get_rect(center=(int(x), int(y)))
        self.screen.blit(text_surface, text_rect)

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
