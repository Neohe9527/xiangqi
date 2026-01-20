"""
全局配置文件
"""

# 窗口配置
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
FPS = 30  # 降低帧率，减少闪烁

# 棋盘配置
BOARD_WIDTH = 800
BOARD_HEIGHT = 900
BOARD_MARGIN = 50
CELL_SIZE = 80

# 颜色配置
COLOR_BG = (245, 222, 179)  # 棋盘背景色
COLOR_LINE = (139, 69, 19)  # 棋盘线条色
COLOR_SELECTED = (255, 255, 0)  # 选中棋子高亮色
COLOR_LEGAL_MOVE = (0, 255, 0, 100)  # 合法走法提示色
COLOR_CHECK = (255, 0, 0)  # 将军提示色
COLOR_TEXT = (0, 0, 0)  # 文字颜色
COLOR_PANEL_BG = (240, 240, 240)  # 信息面板背景色
COLOR_BUTTON = (100, 149, 237)  # 按钮颜色
COLOR_BUTTON_HOVER = (70, 130, 220)  # 按钮悬停颜色

# 棋子配置
PIECE_RADIUS = 35
PIECE_COLORS = {
    'red': (220, 20, 60),
    'black': (0, 0, 0)
}

# 棋子类型
PIECE_TYPES = {
    'K': '将',  # King (红方)
    'k': '帅',  # King (黑方)
    'A': '士',  # Advisor
    'E': '象',  # Elephant
    'H': '马',  # Horse
    'R': '车',  # Rook
    'C': '炮',  # Cannon
    'P': '兵',  # Pawn (红方)
    'p': '卒'   # Pawn (黑方)
}

# 棋子价值
PIECE_VALUES = {
    'K': 10000,
    'R': 900,
    'C': 450,
    'H': 450,
    'A': 200,
    'E': 200,
    'P': 100
}

# AI 配置
AI_CONFIGS = {
    'random': {
        'name': '新手小卒',
        'difficulty': 1,
        'description': '随机走子，适合初学者'
    },
    'greedy': {
        'name': '贪心将军',
        'difficulty': 2,
        'description': '优先吃子，激进但缺乏规划'
    },
    'minimax': {
        'name': '谋略军师',
        'difficulty': 3,
        'description': 'Minimax算法，有战术深度',
        'depth': 3
    },
    'alphabeta': {
        'name': '深算国手',
        'difficulty': 4,
        'description': 'Alpha-Beta剪枝，接近高手水平',
        'depth': 5,
        'time_limit': 10
    }
}

# 字体配置
FONT_SIZE_LARGE = 36
FONT_SIZE_MEDIUM = 24
FONT_SIZE_SMALL = 18

# 游戏模式
MODE_HUMAN_VS_AI = 'human_vs_ai'
MODE_AI_VS_AI = 'ai_vs_ai'
MODE_SETUP = 'setup'

# 计时配置
DEFAULT_TIME_LIMIT = None  # None 表示无限时
