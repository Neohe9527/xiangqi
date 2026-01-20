"""
信息面板
"""
import pygame
import config


class InfoPanel:
    """信息面板，显示游戏状态和AI思考信息"""

    def __init__(self, surface, x, y, width, height):
        """
        初始化信息面板

        Args:
            surface: Pygame surface
            x: X坐标
            y: Y坐标
            width: 宽度
            height: 高度
        """
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._init_fonts()

    def _init_fonts(self):
        """初始化字体"""
        try:
            # macOS 使用系统中文字体
            self.font_large = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 24)
            self.font_medium = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 20)
            self.font_small = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 18)
        except:
            try:
                self.font_large = pygame.font.SysFont('simhei', 24)
                self.font_medium = pygame.font.SysFont('simhei', 20)
                self.font_small = pygame.font.SysFont('simhei', 18)
            except:
                self.font_large = pygame.font.Font(None, 28)
                self.font_medium = pygame.font.Font(None, 24)
                self.font_small = pygame.font.Font(None, 20)

    def draw(self, game_manager):
        """
        绘制信息面板

        Args:
            game_manager: 游戏管理器
        """
        # 绘制背景（带渐变和阴影）
        self._draw_panel_background()

        current_y = self.y + 20

        # 游戏信息
        current_y = self._draw_game_info(game_manager, current_y)

        # AI思考信息
        if game_manager.is_current_player_ai():
            current_y = self._draw_ai_thinking(game_manager, current_y)

        # 走棋历史
        current_y = self._draw_move_history(game_manager, current_y)

    def _draw_panel_background(self):
        """绘制面板背景"""
        # 绘制阴影
        shadow_rect = pygame.Rect(self.x + 3, self.y + 3, self.width, self.height)
        shadow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 30), (0, 0, self.width, self.height), border_radius=10)
        self.surface.blit(shadow_surface, (self.x + 3, self.y + 3))

        # 绘制渐变背景
        for i in range(self.height):
            ratio = i / self.height
            r = int(config.COLOR_PANEL_BG[0] - 5 * ratio)
            g = int(config.COLOR_PANEL_BG[1] - 5 * ratio)
            b = int(config.COLOR_PANEL_BG[2] - 5 * ratio)
            pygame.draw.line(self.surface, (r, g, b),
                           (self.x, self.y + i), (self.x + self.width, self.y + i))

        # 绘制圆角边框
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.surface, config.COLOR_LINE, panel_rect, 3, border_radius=10)

    def _draw_game_info(self, game_manager, start_y):
        """绘制游戏信息"""
        y = start_y

        # 标题（带图标效果）
        self._draw_section_header("游戏信息", y)
        y += 45

        # 红方玩家（带颜色标识）
        red_player = game_manager.red_player
        if red_player is None:
            red_text = "未设置"
        elif red_player.player_type == 'human':
            red_text = "人类玩家"
        else:
            red_text = red_player.ai.name

        self._draw_player_info("红方", red_text, config.PIECE_COLORS['red'], y)
        y += 35

        # 黑方玩家
        black_player = game_manager.black_player
        if black_player is None:
            black_text = "未设置"
        elif black_player.player_type == 'human':
            black_text = "人类玩家"
        else:
            black_text = black_player.ai.name

        self._draw_player_info("黑方", black_text, config.PIECE_COLORS['black'], y)
        y += 40

        # 当前状态（高亮显示）
        status_text = game_manager.get_game_status_text()
        self._draw_status_box(status_text, y)
        y += 45

        # 回合数（带图标）
        move_count = game_manager.history.get_move_count()
        round_num = move_count // 2 + 1
        self._draw_info_item("回合", str(round_num), y)
        y += 30

        return y

    def _draw_section_header(self, text, y):
        """绘制区块标题"""
        # 绘制装饰线
        pygame.draw.line(self.surface, config.COLOR_BUTTON,
                        (self.x + 20, y + 12), (self.x + 15, y + 12), 3)

        # 绘制标题文字
        text_surface = self.font_large.render(text, True, config.COLOR_TEXT)
        self.surface.blit(text_surface, (self.x + 20, y))

    def _draw_player_info(self, label, value, color, y):
        """绘制玩家信息"""
        # 绘制颜色标识圆点
        pygame.draw.circle(self.surface, color, (self.x + 30, y + 10), 8)
        pygame.draw.circle(self.surface, (255, 255, 255), (self.x + 30, y + 10), 8, 2)

        # 绘制标签
        label_surface = self.font_medium.render(f"{label}:", True, config.COLOR_TEXT)
        self.surface.blit(label_surface, (self.x + 45, y))

        # 绘制值
        value_surface = self.font_medium.render(value, True, color)
        self.surface.blit(value_surface, (self.x + 110, y))

    def _draw_status_box(self, text, y):
        """绘制状态框"""
        # 绘制背景框
        box_rect = pygame.Rect(self.x + 20, y, self.width - 40, 35)
        pygame.draw.rect(self.surface, (240, 248, 255), box_rect, border_radius=5)
        pygame.draw.rect(self.surface, config.COLOR_BUTTON, box_rect, 2, border_radius=5)

        # 绘制文字（居中）
        text_surface = self.font_medium.render(text, True, config.COLOR_BUTTON)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, y + 17))
        self.surface.blit(text_surface, text_rect)

    def _draw_info_item(self, label, value, y):
        """绘制信息项"""
        # 绘制标签
        label_surface = self.font_small.render(f"{label}:", True, config.COLOR_TEXT)
        self.surface.blit(label_surface, (self.x + 30, y))

        # 绘制值（加粗）
        value_surface = self.font_medium.render(value, True, config.COLOR_BUTTON)
        self.surface.blit(value_surface, (self.x + 90, y - 2))

    def _draw_ai_thinking(self, game_manager, start_y):
        """绘制AI思考信息"""
        y = start_y + 10

        # 标题
        text = self.font_large.render("AI 思考分析", True, config.COLOR_TEXT)
        self.surface.blit(text, (self.x + 20, y))
        y += 35

        # 分隔线
        pygame.draw.line(self.surface, config.COLOR_LINE,
                        (self.x + 20, y), (self.x + self.width - 20, y), 1)
        y += 15

        # 获取AI思考信息
        thinking_info = game_manager.get_ai_thinking_info()
        if thinking_info:
            # 只显示简单的思考状态，不显示详细信息
            text = self.font_medium.render("思考中...", True, config.COLOR_TEXT)
            self.surface.blit(text, (self.x + 20, y))
            y += 30

        return y

    def _draw_move_history(self, game_manager, start_y):
        """绘制走棋历史"""
        y = start_y + 10

        # 标题
        self._draw_section_header("走棋历史", y)
        y += 45

        # 获取最近的走法
        move_texts = game_manager.history.get_move_list_text(max_moves=10)

        if not move_texts:
            text = self.font_small.render("暂无走棋记录", True, (150, 150, 150))
            self.surface.blit(text, (self.x + 30, y))
        else:
            for i, move_text in enumerate(move_texts):
                # 交替背景色
                if i % 2 == 0:
                    bg_rect = pygame.Rect(self.x + 20, y - 2, self.width - 40, 24)
                    pygame.draw.rect(self.surface, (245, 245, 250), bg_rect, border_radius=3)

                text = self.font_small.render(move_text, True, config.COLOR_TEXT)
                self.surface.blit(text, (self.x + 30, y))
                y += 24

        return y
