"""
棋子渲染器
"""
import pygame
import config


class PieceRenderer:
    """棋子渲染"""

    def __init__(self, surface, board_renderer):
        """
        初始化棋子渲染器

        Args:
            surface: Pygame surface
            board_renderer: 棋盘渲染器（用于获取坐标）
        """
        self.surface = surface
        self.board_renderer = board_renderer
        self._init_fonts()

    def _init_fonts(self):
        """初始化字体"""
        try:
            # macOS 使用系统中文字体
            self.font_large = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 32)
            self.font_medium = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 28)
        except:
            try:
                # 尝试使用中文字体
                self.font_large = pygame.font.SysFont('simhei', 32)
                self.font_medium = pygame.font.SysFont('simhei', 28)
            except:
                # 如果没有中文字体，使用默认字体
                self.font_large = pygame.font.Font(None, 36)
                self.font_medium = pygame.font.Font(None, 32)

    def draw(self, board):
        """
        绘制所有棋子

        Args:
            board: 棋盘对象
        """
        for piece in board.get_all_pieces():
            self._draw_piece(piece)

    def _draw_piece(self, piece):
        """
        绘制单个棋子

        Args:
            piece: 棋子对象
        """
        x, y = self.board_renderer.get_screen_pos(piece.row, piece.col)

        # 棋子颜色
        piece_color = config.PIECE_COLORS[piece.color]
        bg_color = config.PIECE_BG_COLORS[piece.color]
        border_color = config.PIECE_BORDER_COLORS[piece.color]

        # 绘制阴影
        shadow_offset = 3
        shadow_surface = pygame.Surface((config.PIECE_RADIUS * 2 + 10, config.PIECE_RADIUS * 2 + 10), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 60),
                         (config.PIECE_RADIUS + 5, config.PIECE_RADIUS + 5), config.PIECE_RADIUS)
        self.surface.blit(shadow_surface, (x - config.PIECE_RADIUS - 5 + shadow_offset,
                                          y - config.PIECE_RADIUS - 5 + shadow_offset))

        # 绘制棋子圆形背景（带渐变效果）
        for i in range(config.PIECE_RADIUS, 0, -2):
            ratio = i / config.PIECE_RADIUS
            # 创建从中心到边缘的渐变
            r = int(bg_color[0] * ratio + 255 * (1 - ratio) * 0.1)
            g = int(bg_color[1] * ratio + 255 * (1 - ratio) * 0.1)
            b = int(bg_color[2] * ratio + 255 * (1 - ratio) * 0.1)
            pygame.draw.circle(self.surface, (r, g, b), (x, y), i)

        # 绘制外边框（双层）
        pygame.draw.circle(self.surface, border_color,
                         (x, y), config.PIECE_RADIUS, 4)
        pygame.draw.circle(self.surface, (200, 180, 140),
                         (x, y), config.PIECE_RADIUS - 4, 2)

        # 绘制棋子文字
        text = piece.get_chinese_name()
        font = self.font_large if len(text) == 1 else self.font_medium

        # 文字阴影
        shadow_text = font.render(text, True, (0, 0, 0, 100))
        shadow_rect = shadow_text.get_rect(center=(x + 1, y + 1))
        self.surface.blit(shadow_text, shadow_rect)

        # 主文字
        text_surface = font.render(text, True, piece_color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.surface.blit(text_surface, text_rect)

    def draw_dragging_piece(self, piece, mouse_x, mouse_y):
        """
        绘制正在拖拽的棋子（用于残局布置）

        Args:
            piece: 棋子对象
            mouse_x: 鼠标X坐标
            mouse_y: 鼠标Y坐标
        """
        piece_color = config.PIECE_COLORS[piece.color]
        bg_color = config.PIECE_BG_COLORS[piece.color]
        border_color = config.PIECE_BORDER_COLORS[piece.color]

        # 绘制阴影
        shadow_surface = pygame.Surface((config.PIECE_RADIUS * 2 + 20, config.PIECE_RADIUS * 2 + 20), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 80),
                         (config.PIECE_RADIUS + 10, config.PIECE_RADIUS + 10), config.PIECE_RADIUS + 2)
        self.surface.blit(shadow_surface, (mouse_x - config.PIECE_RADIUS - 10 + 5,
                                          mouse_y - config.PIECE_RADIUS - 10 + 5))

        # 绘制棋子背景
        pygame.draw.circle(self.surface, bg_color,
                         (mouse_x, mouse_y), config.PIECE_RADIUS)

        # 绘制边框
        pygame.draw.circle(self.surface, border_color,
                         (mouse_x, mouse_y), config.PIECE_RADIUS, 4)

        # 绘制文字
        text = piece.get_chinese_name()
        font = self.font_large if len(text) == 1 else self.font_medium
        text_surface = font.render(text, True, piece_color)
        text_rect = text_surface.get_rect(center=(mouse_x, mouse_y))
        self.surface.blit(text_surface, text_rect)
