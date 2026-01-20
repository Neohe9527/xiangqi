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

    def draw(self, game_manager):
        """
        绘制棋盘

        Args:
            game_manager: 游戏管理器
        """
        # 绘制背景
        board_rect = pygame.Rect(
            self.offset_x,
            self.offset_y,
            config.BOARD_WIDTH,
            config.BOARD_HEIGHT
        )
        pygame.draw.rect(self.surface, config.COLOR_BG, board_rect)

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
                           (x_start, y), (x_end, y), 2)

        # 竖线（分两段，避开河界）
        for col in range(9):
            x = self.offset_x + self.margin + col * self.cell_size

            # 上半部分（黑方）
            y_start = self.offset_y + self.margin
            y_end = self.offset_y + self.margin + 4 * self.cell_size
            pygame.draw.line(self.surface, config.COLOR_LINE,
                           (x, y_start), (x, y_end), 2)

            # 下半部分（红方）
            y_start = self.offset_y + self.margin + 5 * self.cell_size
            y_end = self.offset_y + self.margin + 9 * self.cell_size
            pygame.draw.line(self.surface, config.COLOR_LINE,
                           (x, y_start), (x, y_end), 2)

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
        pygame.draw.line(self.surface, config.COLOR_LINE, (x1, y1), (x2, y2), 2)

        # 右上到左下
        pygame.draw.line(self.surface, config.COLOR_LINE, (x2, y1), (x1, y2), 2)

    def _draw_river(self):
        """绘制河界文字"""
        try:
            # macOS 使用系统中文字体
            font = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 36)
        except:
            try:
                font = pygame.font.SysFont('simhei', 36)
            except:
                font = pygame.font.Font(None, 36)

        # 楚河
        text = font.render("楚河", True, config.COLOR_LINE)
        x = self.offset_x + self.margin + 1.5 * self.cell_size
        y = self.offset_y + self.margin + 4.3 * self.cell_size
        self.surface.blit(text, (x, y))

        # 汉界
        text = font.render("汉界", True, config.COLOR_LINE)
        x = self.offset_x + self.margin + 5.5 * self.cell_size
        y = self.offset_y + self.margin + 4.3 * self.cell_size
        self.surface.blit(text, (x, y))

    def _draw_selected_piece(self, piece):
        """绘制选中棋子的高亮"""
        x, y = self.get_screen_pos(piece.row, piece.col)
        pygame.draw.circle(self.surface, config.COLOR_SELECTED,
                         (x, y), config.PIECE_RADIUS + 5, 3)

    def _draw_legal_moves(self, legal_moves):
        """绘制合法走法提示"""
        for move in legal_moves:
            x, y = self.get_screen_pos(move.to_row, move.to_col)

            # 绘制半透明圆圈
            s = pygame.Surface((config.PIECE_RADIUS * 2, config.PIECE_RADIUS * 2))
            s.set_alpha(100)
            s.fill(config.COLOR_BG)
            pygame.draw.circle(s, config.COLOR_LEGAL_MOVE,
                             (config.PIECE_RADIUS, config.PIECE_RADIUS),
                             config.PIECE_RADIUS // 2)
            self.surface.blit(s, (x - config.PIECE_RADIUS, y - config.PIECE_RADIUS))

    def _draw_check_indicator(self, board, color):
        """绘制将军提示"""
        king = board.find_king(color)
        if king:
            x, y = self.get_screen_pos(king.row, king.col)
            pygame.draw.circle(self.surface, config.COLOR_CHECK,
                             (x, y), config.PIECE_RADIUS + 8, 4)

    def _draw_last_move(self, move):
        """
        绘制最后一步走法的高亮

        Args:
            move: Move 对象
        """
        # 绘制起始位置（浅蓝色方框）
        x_from, y_from = self.get_screen_pos(move.from_row, move.from_col)
        pygame.draw.rect(self.surface, (100, 149, 237),
                        (x_from - 30, y_from - 30, 60, 60), 3)

        # 绘制目标位置（深蓝色方框）
        x_to, y_to = self.get_screen_pos(move.to_row, move.to_col)
        pygame.draw.rect(self.surface, (65, 105, 225),
                        (x_to - 30, y_to - 30, 60, 60), 4)

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
