"""
菜单系统
"""
import pygame
import config


class Button:
    """按钮类"""

    def __init__(self, x, y, width, height, text, callback):
        """
        初始化按钮

        Args:
            x: X坐标
            y: Y坐标
            width: 宽度
            height: 高度
            text: 按钮文字
            callback: 点击回调函数
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False

        try:
            # macOS 使用系统中文字体
            self.font = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 20)
        except:
            try:
                self.font = pygame.font.SysFont('simhei', 20)
            except:
                self.font = pygame.font.Font(None, 24)

    def draw(self, surface):
        """绘制按钮"""
        color = config.COLOR_BUTTON_HOVER if self.hovered else config.COLOR_BUTTON

        # 绘制按钮背景
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, config.COLOR_LINE, self.rect, 2)

        # 绘制文字
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        """
        处理事件

        Args:
            event: Pygame事件

        Returns:
            bool: 是否处理了事件
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False


class Menu:
    """菜单系统"""

    def __init__(self, surface, x, y):
        """
        初始化菜单

        Args:
            surface: Pygame surface
            x: X坐标
            y: Y坐标
        """
        self.surface = surface
        self.x = x
        self.y = y
        self.buttons = []

    def add_button(self, text, callback, width=120, height=40):
        """
        添加按钮

        Args:
            text: 按钮文字
            callback: 点击回调
            width: 宽度
            height: 高度
        """
        x = self.x + len(self.buttons) * (width + 10)
        button = Button(x, self.y, width, height, text, callback)
        self.buttons.append(button)

    def draw(self):
        """绘制菜单"""
        for button in self.buttons:
            button.draw(self.surface)

    def handle_event(self, event):
        """
        处理事件

        Args:
            event: Pygame事件

        Returns:
            bool: 是否处理了事件
        """
        for button in self.buttons:
            if button.handle_event(event):
                return True
        return False


class GameModeDialog:
    """游戏模式选择对话框"""

    def __init__(self, surface):
        """
        初始化对话框

        Args:
            surface: Pygame surface
        """
        self.surface = surface
        self.active = False
        self.selected_mode = None
        self.selected_red = None
        self.selected_black = None
        self.selected_red_ai = 'alphabeta'
        self.selected_black_ai = 'alphabeta'
        self.ai_selection_side = None  # 'red' or 'black' - 当前选择哪方的AI

        # 对话框尺寸
        self.width = 700
        self.height = 700  # 增加高度以容纳更多内容
        self.x = (config.WINDOW_WIDTH - self.width) // 2
        self.y = (config.WINDOW_HEIGHT - self.height) // 2

        try:
            # macOS 使用系统中文字体
            self.font_title = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 32)
            self.font_normal = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 24)
            self.font_small = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 20)
        except:
            try:
                self.font_title = pygame.font.SysFont('simhei', 32)
                self.font_normal = pygame.font.SysFont('simhei', 24)
                self.font_small = pygame.font.SysFont('simhei', 20)
            except:
                self.font_title = pygame.font.Font(None, 36)
                self.font_normal = pygame.font.Font(None, 28)
                self.font_small = pygame.font.Font(None, 24)

        self._create_buttons()

    def _create_buttons(self):
        """创建按钮"""
        button_y = self.y + 100

        # 人机对弈按钮
        self.btn_human_vs_ai = Button(
            self.x + 100, button_y, 220, 50,
            "人机对弈", self._select_human_vs_ai
        )

        # AI vs AI 按钮
        self.btn_ai_vs_ai = Button(
            self.x + 380, button_y, 220, 50,
            "AI 对弈", self._select_ai_vs_ai
        )

        # AI难度选择按钮 - 人机对弈模式
        self.human_ai_buttons = []
        ai_types = [
            ('random', '新手小卒'),
            ('greedy', '贪心将军'),
            ('minimax', '谋略军师'),
            ('alphabeta', '深算国手')
        ]

        for i, (ai_type, name) in enumerate(ai_types):
            btn = Button(
                self.x + 100 + (i % 2) * 260,
                self.y + 280 + (i // 2) * 70,
                220, 55,
                name,
                lambda t=ai_type: self._select_ai_difficulty(t)
            )
            self.human_ai_buttons.append((ai_type, btn))

        # AI难度选择按钮 - AI对弈模式（红方）
        self.red_ai_buttons = []
        for i, (ai_type, name) in enumerate(ai_types):
            btn = Button(
                self.x + 50,
                self.y + 280 + i * 70,
                280, 55,
                name,
                lambda t=ai_type: self._select_red_ai(t)
            )
            self.red_ai_buttons.append((ai_type, btn))

        # AI难度选择按钮 - AI对弈模式（黑方）
        self.black_ai_buttons = []
        for i, (ai_type, name) in enumerate(ai_types):
            btn = Button(
                self.x + 370,
                self.y + 280 + i * 70,
                280, 55,
                name,
                lambda t=ai_type: self._select_black_ai(t)
            )
            self.black_ai_buttons.append((ai_type, btn))

        # 开始游戏按钮
        self.btn_start = Button(
            self.x + 250, self.y + 620, 200, 50,
            "开始游戏", self._start_game
        )

    def _select_human_vs_ai(self):
        """选择人机对弈"""
        self.selected_mode = 'human_vs_ai'
        self.selected_red = 'human'
        self.selected_black = 'ai'

    def _select_ai_vs_ai(self):
        """选择AI对弈"""
        self.selected_mode = 'ai_vs_ai'
        self.selected_red = 'ai'
        self.selected_black = 'ai'

    def _select_ai_difficulty(self, ai_type):
        """选择AI难度（人机对弈模式）"""
        self.selected_black_ai = ai_type

    def _select_red_ai(self, ai_type):
        """选择红方AI（AI对弈模式）"""
        self.selected_red_ai = ai_type

    def _select_black_ai(self, ai_type):
        """选择黑方AI（AI对弈模式）"""
        self.selected_black_ai = ai_type

    def _start_game(self):
        """开始游戏"""
        if self.selected_mode:
            self.active = False

    def show(self):
        """显示对话框"""
        self.active = True
        self.selected_mode = None

    def draw(self):
        """绘制对话框"""
        if not self.active:
            return

        # 绘制半透明背景
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.surface.blit(overlay, (0, 0))

        # 绘制对话框背景
        dialog_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.surface, (240, 240, 240), dialog_rect)
        pygame.draw.rect(self.surface, config.COLOR_LINE, dialog_rect, 3)

        # 标题
        title = self.font_title.render("选择游戏模式", True, config.COLOR_TEXT)
        title_rect = title.get_rect(center=(self.x + self.width // 2, self.y + 50))
        self.surface.blit(title, title_rect)

        # 绘制模式选择按钮
        self.btn_human_vs_ai.draw(self.surface)
        self.btn_ai_vs_ai.draw(self.surface)

        # 显示当前选择的模式
        if self.selected_mode:
            y = self.y + 180
            if self.selected_mode == 'human_vs_ai':
                mode_text = "人类 vs AI"
            else:
                mode_text = "AI vs AI"

            selection_text = self.font_normal.render(f"已选择: {mode_text}", True, config.COLOR_TEXT)
            selection_rect = selection_text.get_rect(center=(self.x + self.width // 2, y))
            self.surface.blit(selection_text, selection_rect)

            # 根据模式显示不同的AI选择界面
            if self.selected_mode == 'human_vs_ai':
                self._draw_human_vs_ai_selection(y + 50)
            else:
                self._draw_ai_vs_ai_selection(y + 50)

            # 绘制开始按钮
            self.btn_start.draw(self.surface)

    def _draw_human_vs_ai_selection(self, start_y):
        """绘制人机对弈的AI选择界面"""
        # 标题
        title = self.font_normal.render("选择AI难度:", True, config.COLOR_TEXT)
        title_rect = title.get_rect(center=(self.x + self.width // 2, start_y))
        self.surface.blit(title, title_rect)

        # 绘制AI难度按钮
        for ai_type, btn in self.human_ai_buttons:
            # 高亮当前选中的难度
            if ai_type == self.selected_black_ai:
                btn.hovered = True
            btn.draw(self.surface)
            btn.hovered = False

        # 显示当前选择
        ai_name = config.AI_CONFIGS.get(self.selected_black_ai, {}).get('name', '未知')
        ai_desc = config.AI_CONFIGS.get(self.selected_black_ai, {}).get('description', '')

        current_text = self.font_small.render(f"当前选择: {ai_name}", True, config.COLOR_TEXT)
        current_rect = current_text.get_rect(center=(self.x + self.width // 2, start_y + 210))
        self.surface.blit(current_text, current_rect)

        desc_text = self.font_small.render(ai_desc, True, (100, 100, 100))
        desc_rect = desc_text.get_rect(center=(self.x + self.width // 2, start_y + 240))
        self.surface.blit(desc_text, desc_rect)

    def _draw_ai_vs_ai_selection(self, start_y):
        """绘制AI对弈的双方AI选择界面"""
        # 标题
        title = self.font_normal.render("选择双方AI:", True, config.COLOR_TEXT)
        title_rect = title.get_rect(center=(self.x + self.width // 2, start_y))
        self.surface.blit(title, title_rect)

        # 红方标题
        red_title = self.font_normal.render("红方", True, (220, 20, 60))
        red_rect = red_title.get_rect(center=(self.x + 190, start_y + 40))
        self.surface.blit(red_title, red_rect)

        # 黑方标题
        black_title = self.font_normal.render("黑方", True, (0, 0, 0))
        black_rect = black_title.get_rect(center=(self.x + 510, start_y + 40))
        self.surface.blit(black_title, black_rect)

        # 绘制红方AI按钮
        for ai_type, btn in self.red_ai_buttons:
            if ai_type == self.selected_red_ai:
                btn.hovered = True
            btn.draw(self.surface)
            btn.hovered = False

        # 绘制黑方AI按钮
        for ai_type, btn in self.black_ai_buttons:
            if ai_type == self.selected_black_ai:
                btn.hovered = True
            btn.draw(self.surface)
            btn.hovered = False

        # 显示当前选择
        red_name = config.AI_CONFIGS.get(self.selected_red_ai, {}).get('name', '未知')
        black_name = config.AI_CONFIGS.get(self.selected_black_ai, {}).get('name', '未知')

        summary_text = self.font_small.render(f"红方: {red_name}  vs  黑方: {black_name}", True, config.COLOR_TEXT)
        summary_rect = summary_text.get_rect(center=(self.x + self.width // 2, start_y + 330))
        self.surface.blit(summary_text, summary_rect)

    def handle_event(self, event):
        """
        处理事件

        Args:
            event: Pygame事件

        Returns:
            bool: 是否处理了事件
        """
        if not self.active:
            return False

        # 处理模式选择按钮
        if self.btn_human_vs_ai.handle_event(event):
            return True
        if self.btn_ai_vs_ai.handle_event(event):
            return True

        # 处理AI难度选择按钮
        if self.selected_mode == 'human_vs_ai':
            # 人机对弈模式：处理AI难度选择
            for ai_type, btn in self.human_ai_buttons:
                if btn.handle_event(event):
                    return True
        elif self.selected_mode == 'ai_vs_ai':
            # AI对弈模式：处理红方和黑方AI选择
            for ai_type, btn in self.red_ai_buttons:
                if btn.handle_event(event):
                    return True
            for ai_type, btn in self.black_ai_buttons:
                if btn.handle_event(event):
                    return True

        # 处理开始游戏按钮
        if self.selected_mode and self.btn_start.handle_event(event):
            return True

        return False

    def get_selection(self):
        """
        获取选择结果

        Returns:
            dict: 选择信息，只有在对话框关闭且已选择模式时才返回
        """
        # 只有在对话框关闭（用户点击了开始游戏）时才返回选择结果
        if not self.active and self.selected_mode:
            return {
                'mode': self.selected_mode,
                'red_player': self.selected_red,
                'black_player': self.selected_black,
                'red_ai': self.selected_red_ai,
                'black_ai': self.selected_black_ai
            }
        return None


class GameOverDialog:
    """游戏结束对话框"""

    def __init__(self, surface):
        """
        初始化对话框

        Args:
            surface: Pygame surface
        """
        self.surface = surface
        self.active = False
        self.result = None
        self.winner = None

        # 对话框尺寸
        self.width = 500
        self.height = 300
        self.x = (config.WINDOW_WIDTH - self.width) // 2
        self.y = (config.WINDOW_HEIGHT - self.height) // 2

        try:
            # macOS 使用系统中文字体
            self.font_title = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 48)
            self.font_normal = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 24)
        except:
            try:
                self.font_title = pygame.font.SysFont('simhei', 48)
                self.font_normal = pygame.font.SysFont('simhei', 24)
            except:
                self.font_title = pygame.font.Font(None, 52)
                self.font_normal = pygame.font.Font(None, 28)

        self._create_buttons()

    def _create_buttons(self):
        """创建按钮"""
        # 新游戏按钮
        self.btn_new_game = Button(
            self.x + 50, self.y + 200, 180, 50,
            "新游戏", self._new_game
        )

        # 关闭按钮
        self.btn_close = Button(
            self.x + 270, self.y + 200, 180, 50,
            "关闭", self._close
        )

    def _new_game(self):
        """新游戏"""
        self.active = False
        self.on_new_game = True

    def _close(self):
        """关闭对话框"""
        self.active = False
        self.on_new_game = False

    def show(self, result, winner=None):
        """
        显示对话框

        Args:
            result: 游戏结果 ('red_win', 'black_win', 'draw')
            winner: 获胜方名称
        """
        self.active = True
        self.result = result
        self.winner = winner
        self.on_new_game = False

    def draw(self):
        """绘制对话框"""
        if not self.active:
            return

        # 绘制半透明背景
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.surface.blit(overlay, (0, 0))

        # 绘制对话框背景
        dialog_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.surface, (240, 240, 240), dialog_rect)
        pygame.draw.rect(self.surface, config.COLOR_LINE, dialog_rect, 4)

        # 显示结果
        if self.result == 'red_win':
            title_text = "红方胜利！"
            title_color = (220, 20, 60)
        elif self.result == 'black_win':
            title_text = "黑方胜利！"
            title_color = (0, 0, 0)
        else:
            title_text = "和棋"
            title_color = (100, 100, 100)

        title = self.font_title.render(title_text, True, title_color)
        title_rect = title.get_rect(center=(self.x + self.width // 2, self.y + 80))
        self.surface.blit(title, title_rect)

        # 显示获胜方信息
        if self.winner:
            winner_text = f"获胜方: {self.winner}"
            winner_surface = self.font_normal.render(winner_text, True, config.COLOR_TEXT)
            winner_rect = winner_surface.get_rect(center=(self.x + self.width // 2, self.y + 140))
            self.surface.blit(winner_surface, winner_rect)

        # 绘制按钮
        self.btn_new_game.draw(self.surface)
        self.btn_close.draw(self.surface)

    def handle_event(self, event):
        """
        处理事件

        Args:
            event: Pygame事件

        Returns:
            bool: 是否处理了事件
        """
        if not self.active:
            return False

        if self.btn_new_game.handle_event(event):
            return True
        if self.btn_close.handle_event(event):
            return True

        return False
