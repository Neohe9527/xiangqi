"""
棋盘渲染器
"""
import pygame
import config


class BoardRenderer:
    """棋盘渲染"""

    def __init__(self, surface, offset_x=0, offset_y=0):
        """
        初始化棋盘渲染器

        Args:
            surface: Pygame surface
            offset_x: X偏移
            offset_y: Y偏移
        """
        self.surface = surface
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.cell_size = config.CELL_SIZE
        self.margin = config.BOARD_MARGIN

        # 创建棋盘背景纹理
        self._create_board_texture()

    def _create_board_texture(self):
        """创建棋盘木纹背景纹理"""
        self.board_texture = pygame.Surface((config.BOARD_WIDTH, config.BOARD_HEIGHT))

        # 绘制渐变木纹效果
        for y in range(config.BOARD_HEIGHT):
            # 创建垂直渐变
            ratio = y / config.BOARD_HEIGHT
            color_variation = int(15 * (0.5 - abs(ratio - 0.5)))

            r = min(255, config.COLOR_BG[0] + color_variation)
            g = min(255, config.COLOR_BG[1] + color_variation)
            b = min(255, config.COLOR_BG[2] + color_variation)

            pygame.draw.line(self.board_texture, (r, g, b),
                           (0, y), (config.BOARD_WIDTH, y))

        # 添加木纹纹理效果
        import random
        random.seed(42)  # 固定随机种子，保证每次纹理一致
        for _ in range(200):
            x = random.randint(0, config.BOARD_WIDTH)
            y = random.randint(0, config.BOARD_HEIGHT)
            length = random.randint(20, 80)
            alpha = random.randint(10, 30)

            # 创建半透明线条
            s = pygame.Surface((length, 2), pygame.SRCALPHA)
            color = (*config.COLOR_BG_DARK, alpha)
            pygame.draw.line(s, color, (0, 1), (length, 1))
            self.board_texture.blit(s, (x, y))

    def _draw_background(self):
        """绘制棋盘背景"""
        # 绘制外边框阴影
        shadow_rect = pygame.Rect(
            self.offset_x + 5,
            self.offset_y + 5,
            config.BOARD_WIDTH,
            config.BOARD_HEIGHT
        )
        pygame.draw.rect(self.surface, (100, 100, 100, 50), shadow_rect)

        # 绘制棋盘纹理
        self.surface.blit(self.board_texture, (self.offset_x, self.offset_y))

        # 绘制装饰边框
        self._draw_decorative_border()

        # 绘制边框
        border_rect = pygame.Rect(
            self.offset_x,
            self.offset_y,
            config.BOARD_WIDTH,
            config.BOARD_HEIGHT
        )
        pygame.draw.rect(self.surface, config.COLOR_LINE, border_rect, 4)

    def _draw_decorative_border(self):
        """绘制装饰性边框"""
        # 绘制四角装饰
        corner_size = 30
        corner_color = (139, 69, 19)

        # 左上角
        self._draw_corner_decoration(self.offset_x, self.offset_y, corner_size, corner_color, 'top-left')

        # 右上角
        self._draw_corner_decoration(self.offset_x + config.BOARD_WIDTH, self.offset_y, corner_size, corner_color, 'top-right')

        # 左下角
        self._draw_corner_decoration(self.offset_x, self.offset_y + config.BOARD_HEIGHT, corner_size, corner_color, 'bottom-left')

        # 右下角
        self._draw_corner_decoration(self.offset_x + config.BOARD_WIDTH, self.offset_y + config.BOARD_HEIGHT, corner_size, corner_color, 'bottom-right')

    def _draw_corner_decoration(self, x, y, size, color, position):
        """绘制角落装饰"""
        if position == 'top-left':
            # 横线
            pygame.draw.line(self.surface, color, (x, y), (x + size, y), 6)
            # 竖线
            pygame.draw.line(self.surface, color, (x, y), (x, y + size), 6)
        elif position == 'top-right':
            pygame.draw.line(self.surface, color, (x, y), (x - size, y), 6)
            pygame.draw.line(self.surface, color, (x, y), (x, y + size), 6)
        elif position == 'bottom-left':
            pygame.draw.line(self.surface, color, (x, y), (x + size, y), 6)
            pygame.draw.line(self.surface, color, (x, y), (x, y - size), 6)
        elif position == 'bottom-right':
            pygame.draw.line(self.surface, color, (x, y), (x - size, y), 6)
            pygame.draw.line(self.surface, color, (x, y), (x, y - size), 6)

    def draw(self, game_manager):
        """
        绘制棋盘

        Args:
            game_manager: 游戏管理器
        """
        # 绘制背景和木纹效果
        self._draw_background()

        # 绘制棋盘线条
        self._draw_lines()

        # 绘制九宫格
        self._draw_palace()

        # 绘制河界
        self._draw_river()

        # 绘制最后一步走法高亮
        if game_manager.last_move:
            self._draw_last_move(game_manager.last_move)

        # 绘制合法走法提示
        if game_manager.selected_piece:
            self._draw_legal_moves(game_manager.legal_moves_for_selected)

        # 绘制选中棋子高亮
        if game_manager.selected_piece:
            self._draw_selected_piece(game_manager.selected_piece)

        # 绘制将军提示
        if game_manager.is_in_check():
            self._draw_check_indicator(game_manager.board, game_manager.current_color)

    def _draw_lines(self):
        """绘制棋盘线条"""
        # 横线
        for row in range(10):
            y = self.offset_y + self.margin + row * self.cell_size
            x_start = self.offset_x + self.margin
            x_end = self.offset_x + self.margin + 8 * self.cell_size
            pygame.draw.line(self.surface, config.COLOR_LINE,
                           (x_start, y), (x_end, y), 3)

        # 竖线（分两段，避开河界）
        for col in range(9):
            x = self.offset_x + self.margin + col * self.cell_size

            # 上半部分（黑方）
            y_start = self.offset_y + self.margin
            y_end = self.offset_y + self.margin + 4 * self.cell_size
            pygame.draw.line(self.surface, config.COLOR_LINE,
                           (x, y_start), (x, y_end), 3)

            # 下半部分（红方）
            y_start = self.offset_y + self.margin + 5 * self.cell_size
            y_end = self.offset_y + self.margin + 9 * self.cell_size
            pygame.draw.line(self.surface, config.COLOR_LINE,
                           (x, y_start), (x, y_end), 3)

    def _draw_palace(self):
        """绘制九宫格斜线"""
        # 黑方九宫格
        self._draw_palace_lines(0, 3)

        # 红方九宫格
        self._draw_palace_lines(7, 3)

    def _draw_palace_lines(self, start_row, start_col):
        """绘制九宫格的斜线"""
        x1 = self.offset_x + self.margin + start_col * self.cell_size
        y1 = self.offset_y + self.margin + start_row * self.cell_size
        x2 = self.offset_x + self.margin + (start_col + 2) * self.cell_size
        y2 = self.offset_y + self.margin + (start_row + 2) * self.cell_size

        # 左上到右下
        pygame.draw.line(self.surface, config.COLOR_LINE, (x1, y1), (x2, y2), 3)

        # 右上到左下
        pygame.draw.line(self.surface, config.COLOR_LINE, (x2, y1), (x1, y2), 3)

    def _draw_river(self):
        """绘制河界文字"""
        try:
            # macOS 使用系统中文字体
            font = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 40)
        except:
            try:
                font = pygame.font.SysFont('simhei', 40)
            except:
                font = pygame.font.Font(None, 40)

        # 河界背景
        river_y = self.offset_y + self.margin + 4 * self.cell_size
        river_rect = pygame.Rect(
            self.offset_x + self.margin,
            river_y,
            8 * self.cell_size,
            self.cell_size
        )
        # 绘制半透明河界背景
        river_surface = pygame.Surface((river_rect.width, river_rect.height), pygame.SRCALPHA)
        river_surface.fill((*config.COLOR_RIVER, 60))
        self.surface.blit(river_surface, river_rect.topleft)

        # 楚河 - 使用更优雅的字体颜色
        text_color = (101, 67, 33)  # 深棕色
        text = font.render("楚 河", True, text_color)
        x = self.offset_x + self.margin + 1.2 * self.cell_size
        y = self.offset_y + self.margin + 4.25 * self.cell_size
        self.surface.blit(text, (x, y))

        # 汉界
        text = font.render("汉 界", True, text_color)
        x = self.offset_x + self.margin + 5.2 * self.cell_size
        y = self.offset_y + self.margin + 4.25 * self.cell_size
        self.surface.blit(text, (x, y))

    def _draw_selected_piece(self, piece):
        """绘制选中棋子的高亮"""
        x, y = self.get_screen_pos(piece.row, piece.col)
        # 绘制发光效果
        for i in range(3):
            alpha = 150 - i * 40
            radius = config.PIECE_RADIUS + 8 + i * 3
            glow_surface = pygame.Surface((radius * 2 + 10, radius * 2 + 10), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*config.COLOR_SELECTED, alpha),
                             (radius + 5, radius + 5), radius, 3)
            self.surface.blit(glow_surface, (x - radius - 5, y - radius - 5))

    def _draw_legal_moves(self, legal_moves):
        """绘制合法走法提示"""
        for move in legal_moves:
            x, y = self.get_screen_pos(move.to_row, move.to_col)

            # 绘制脉动效果的圆圈
            for i in range(3):
                radius = config.PIECE_RADIUS // 3 + i * 2
                alpha = 120 - i * 30
                s = pygame.Surface((radius * 2 + 10, radius * 2 + 10), pygame.SRCALPHA)
                pygame.draw.circle(s, (*config.COLOR_LEGAL_MOVE, alpha),
                                 (radius + 5, radius + 5), radius)
                self.surface.blit(s, (x - radius - 5, y - radius - 5))

    def _draw_check_indicator(self, board, color):
        """绘制将军提示"""
        king = board.find_king(color)
        if king:
            x, y = self.get_screen_pos(king.row, king.col)
            # 绘制警告脉动效果
            for i in range(4):
                alpha = 200 - i * 40
                radius = config.PIECE_RADIUS + 10 + i * 4
                s = pygame.Surface((radius * 2 + 10, radius * 2 + 10), pygame.SRCALPHA)
                pygame.draw.circle(s, (*config.COLOR_CHECK, alpha),
                                 (radius + 5, radius + 5), radius, 4)
                self.surface.blit(s, (x - radius - 5, y - radius - 5))

    def _draw_last_move(self, move):
        """
        绘制最后一步走法的高亮

        Args:
            move: Move 对象
        """
        # 绘制起始位置（淡蓝色圆角方框）
        x_from, y_from = self.get_screen_pos(move.from_row, move.from_col)
        from_rect = pygame.Rect(x_from - 32, y_from - 32, 64, 64)
        self._draw_rounded_rect(self.surface, (100, 149, 237, 100), from_rect, 8, 3)

        # 绘制目标位置（深蓝色圆角方框）
        x_to, y_to = self.get_screen_pos(move.to_row, move.to_col)
        to_rect = pygame.Rect(x_to - 32, y_to - 32, 64, 64)
        self._draw_rounded_rect(self.surface, (65, 105, 225, 180), to_rect, 8, 4)

    def _draw_rounded_rect(self, surface, color, rect, radius, width):
        """绘制圆角矩形"""
        # 创建带透明度的surface
        s = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(s, color, (5, 5, rect.width, rect.height), width, radius)
        surface.blit(s, (rect.x - 5, rect.y - 5))

    def get_screen_pos(self, row, col):
        """
        将棋盘坐标转换为屏幕坐标

        Args:
            row: 行 (0-9)
            col: 列 (0-8)

        Returns:
            tuple: (x, y) 屏幕坐标
        """
        x = self.offset_x + self.margin + col * self.cell_size
        y = self.offset_y + self.margin + row * self.cell_size
        return x, y

    def get_board_pos(self, screen_x, screen_y):
        """
        将屏幕坐标转换为棋盘坐标

        Args:
            screen_x: 屏幕X坐标
            screen_y: 屏幕Y坐标

        Returns:
            tuple: (row, col) 棋盘坐标，如果不在棋盘上则返回 None
        """
        # 减去偏移和边距
        x = screen_x - self.offset_x - self.margin
        y = screen_y - self.offset_y - self.margin

        # 转换为行列
        col = round(x / self.cell_size)
        row = round(y / self.cell_size)

        # 检查是否在有效范围内
        if 0 <= row <= 9 and 0 <= col <= 8:
            # 检查是否足够接近交叉点
            actual_x = col * self.cell_size
            actual_y = row * self.cell_size
            distance = ((x - actual_x) ** 2 + (y - actual_y) ** 2) ** 0.5

            if distance < self.cell_size * 0.4:  # 在交叉点附近
                return row, col

        return None
