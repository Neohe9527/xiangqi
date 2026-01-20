"""
棋子图片资源生成器
"""
import pygame
import os
import config


class PieceImageGenerator:
    """生成高质量的棋子图片"""

    def __init__(self):
        """初始化图片生成器"""
        self.piece_images = {}
        self.piece_size = config.PIECE_RADIUS * 2
        self._generate_all_pieces()

    def _generate_all_pieces(self):
        """生成所有棋子图片"""
        piece_types = {
            'red': ['K', 'A', 'E', 'H', 'R', 'C', 'P'],
            'black': ['k', 'A', 'E', 'H', 'R', 'C', 'p']
        }

        for color in ['red', 'black']:
            for piece_type in piece_types[color]:
                key = f"{color}_{piece_type}"
                self.piece_images[key] = self._generate_piece_image(color, piece_type)

    def _generate_piece_image(self, color, piece_type):
        """
        生成单个棋子图片

        Args:
            color: 棋子颜色 ('red' or 'black')
            piece_type: 棋子类型

        Returns:
            pygame.Surface: 棋子图片
        """
        size = self.piece_size + 20  # 额外空间用于阴影
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        center_x = size // 2
        center_y = size // 2
        radius = config.PIECE_RADIUS

        # 获取颜色
        piece_color = config.PIECE_COLORS[color]
        bg_color = config.PIECE_BG_COLORS[color]
        border_color = config.PIECE_BORDER_COLORS[color]

        # 绘制阴影
        shadow_offset = 4
        for i in range(5):
            alpha = 40 - i * 8
            shadow_radius = radius - i
            shadow_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(shadow_surface, (0, 0, 0, alpha),
                             (center_x + shadow_offset, center_y + shadow_offset),
                             shadow_radius)
            surface.blit(shadow_surface, (0, 0))

        # 绘制渐变背景
        for i in range(radius, 0, -1):
            ratio = i / radius
            # 从中心到边缘的渐变
            r = int(bg_color[0] * ratio + 255 * (1 - ratio) * 0.15)
            g = int(bg_color[1] * ratio + 255 * (1 - ratio) * 0.15)
            b = int(bg_color[2] * ratio + 255 * (1 - ratio) * 0.15)
            pygame.draw.circle(surface, (r, g, b), (center_x, center_y), i)

        # 绘制高光效果
        highlight_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        highlight_offset_x = -radius // 4
        highlight_offset_y = -radius // 4
        highlight_radius = radius // 2
        for i in range(highlight_radius, 0, -1):
            alpha = int(60 * (i / highlight_radius))
            pygame.draw.circle(highlight_surface, (255, 255, 255, alpha),
                             (center_x + highlight_offset_x, center_y + highlight_offset_y), i)
        surface.blit(highlight_surface, (0, 0))

        # 绘制外边框（三层）
        pygame.draw.circle(surface, border_color, (center_x, center_y), radius, 5)
        pygame.draw.circle(surface, (220, 200, 160), (center_x, center_y), radius - 5, 2)
        pygame.draw.circle(surface, border_color, (center_x, center_y), radius - 8, 1)

        # 绘制文字
        text = self._get_piece_text(piece_type)
        self._draw_text_on_surface(surface, text, piece_color, center_x, center_y)

        return surface

    def _get_piece_text(self, piece_type):
        """获取棋子文字"""
        piece_names = {
            'K': '帅', 'k': '将',
            'A': '士', 'E': '相',
            'H': '马', 'R': '车',
            'C': '炮', 'P': '兵', 'p': '卒'
        }
        return piece_names.get(piece_type, piece_type)

    def _draw_text_on_surface(self, surface, text, color, x, y):
        """在surface上绘制文字"""
        try:
            # macOS 使用系统中文字体
            font = pygame.font.Font('/System/Library/Fonts/STHeiti Medium.ttc', 36)
        except:
            try:
                font = pygame.font.SysFont('simhei', 36)
            except:
                font = pygame.font.Font(None, 40)

        # 文字阴影
        shadow_text = font.render(text, True, (0, 0, 0, 120))
        shadow_rect = shadow_text.get_rect(center=(x + 2, y + 2))
        surface.blit(shadow_text, shadow_rect)

        # 主文字
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, text_rect)

        # 文字描边效果
        outline_color = (255, 255, 255, 100) if color == config.PIECE_COLORS['black'] else (0, 0, 0, 50)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            outline_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            outline_text = font.render(text, True, outline_color)
            outline_rect = outline_text.get_rect(center=(x + dx, y + dy))
            surface.blit(outline_text, outline_rect)

    def get_piece_image(self, color, piece_type):
        """
        获取棋子图片

        Args:
            color: 棋子颜色
            piece_type: 棋子类型

        Returns:
            pygame.Surface: 棋子图片
        """
        key = f"{color}_{piece_type}"
        return self.piece_images.get(key)
