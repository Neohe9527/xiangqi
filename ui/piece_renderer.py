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
        bg_color = (255, 255, 220) if piece.color == 'red' else (50, 50, 50)
        border_color = (0, 0, 0)

        # 绘制棋子圆形背景
        pygame.draw.circle(self.surface, bg_color,
                         (x, y), config.PIECE_RADIUS)

        # 绘制棋子边框
        pygame.draw.circle(self.surface, border_color,
                         (x, y), config.PIECE_RADIUS, 3)

        # 绘制棋子文字
        text = piece.get_chinese_name()
        font = self.font_large if len(text) == 1 else self.font_medium

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
        bg_color = (255, 255, 220) if piece.color == 'red' else (50, 50, 50)
        border_color = (0, 0, 0)

        # 绘制半透明效果
        s = pygame.Surface((config.PIECE_RADIUS * 2, config.PIECE_RADIUS * 2))
        s.set_alpha(200)
        s.fill(config.COLOR_BG)

        pygame.draw.circle(s, bg_color,
                         (config.PIECE_RADIUS, config.PIECE_RADIUS),
                         config.PIECE_RADIUS)
        pygame.draw.circle(s, border_color,
                         (config.PIECE_RADIUS, config.PIECE_RADIUS),
                         config.PIECE_RADIUS, 3)

        self.surface.blit(s, (mouse_x - config.PIECE_RADIUS,
                             mouse_y - config.PIECE_RADIUS))

        # 绘制文字
        text = piece.get_chinese_name()
        font = self.font_large if len(text) == 1 else self.font_medium
        text_surface = font.render(text, True, piece_color)
        text_rect = text_surface.get_rect(center=(mouse_x, mouse_y))
        self.surface.blit(text_surface, text_rect)
