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
        # 绘制背景
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.surface, config.COLOR_PANEL_BG, panel_rect)
        pygame.draw.rect(self.surface, config.COLOR_LINE, panel_rect, 2)

        current_y = self.y + 20

        # 游戏信息
        current_y = self._draw_game_info(game_manager, current_y)

        # AI思考信息
        if game_manager.is_current_player_ai():
            current_y = self._draw_ai_thinking(game_manager, current_y)

        # 走棋历史
        current_y = self._draw_move_history(game_manager, current_y)

    def _draw_game_info(self, game_manager, start_y):
        """绘制游戏信息"""
        y = start_y

        # 标题
        text = self.font_large.render("游戏信息", True, config.COLOR_TEXT)
        self.surface.blit(text, (self.x + 20, y))
        y += 35

        # 分隔线
        pygame.draw.line(self.surface, config.COLOR_LINE,
                        (self.x + 20, y), (self.x + self.width - 20, y), 1)
        y += 15

        # 红方玩家
        red_player = game_manager.red_player
        if red_player is None:
            red_text = "红方: 未设置"
        elif red_player.player_type == 'human':
            red_text = "红方: 人类玩家"
        else:
            red_text = f"红方: {red_player.ai.name}"
        text = self.font_medium.render(red_text, True, config.COLOR_TEXT)
        self.surface.blit(text, (self.x + 20, y))
        y += 30

        # 黑方玩家
        black_player = game_manager.black_player
        if black_player is None:
            black_text = "黑方: 未设置"
        elif black_player.player_type == 'human':
            black_text = "黑方: 人类玩家"
        else:
            black_text = f"黑方: {black_player.ai.name}"
        text = self.font_medium.render(black_text, True, config.COLOR_TEXT)
        self.surface.blit(text, (self.x + 20, y))
        y += 35

        # 当前状态
        status_text = game_manager.get_game_status_text()
        text = self.font_medium.render(status_text, True, config.COLOR_TEXT)
        self.surface.blit(text, (self.x + 20, y))
        y += 30

        # 回合数
        move_count = game_manager.history.get_move_count()
        round_num = move_count // 2 + 1
        text = self.font_small.render(f"回合: {round_num}", True, config.COLOR_TEXT)
        self.surface.blit(text, (self.x + 20, y))
        y += 30

        return y

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
        text = self.font_large.render("走棋历史", True, config.COLOR_TEXT)
        self.surface.blit(text, (self.x + 20, y))
        y += 35

        # 分隔线
        pygame.draw.line(self.surface, config.COLOR_LINE,
                        (self.x + 20, y), (self.x + self.width - 20, y), 1)
        y += 15

        # 获取最近的走法
        move_texts = game_manager.history.get_move_list_text(max_moves=10)

        if not move_texts:
            text = self.font_small.render("暂无走棋记录", True, config.COLOR_TEXT)
            self.surface.blit(text, (self.x + 20, y))
        else:
            for move_text in move_texts:
                text = self.font_small.render(move_text, True, config.COLOR_TEXT)
                self.surface.blit(text, (self.x + 20, y))
                y += 22

        return y
