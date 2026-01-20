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

# 颜色配置 - 优雅的中国风配色
COLOR_BG = (235, 200, 140)  # 棋盘背景色 - 温暖的木色
COLOR_BG_DARK = (215, 180, 120)  # 棋盘深色背景
COLOR_LINE = (101, 67, 33)  # 棋盘线条色 - 深棕色
COLOR_SELECTED = (255, 215, 0)  # 选中棋子高亮色 - 金色
COLOR_LEGAL_MOVE = (46, 204, 113)  # 合法走法提示色 - 翡翠绿
COLOR_CHECK = (231, 76, 60)  # 将军提示色 - 朱红色
COLOR_TEXT = (44, 62, 80)  # 文字颜色 - 深灰蓝
COLOR_PANEL_BG = (250, 248, 245)  # 信息面板背景色 - 米白色
COLOR_BUTTON = (52, 152, 219)  # 按钮颜色 - 天蓝色
COLOR_BUTTON_HOVER = (41, 128, 185)  # 按钮悬停颜色 - 深天蓝
COLOR_RIVER = (176, 196, 222)  # 河界颜色 - 淡蓝色

# 棋子配置
PIECE_RADIUS = 38
PIECE_COLORS = {
    'red': (192, 57, 43),  # 深红色
    'black': (44, 62, 80)  # 深灰蓝
}
# 棋子背景色
PIECE_BG_COLORS = {
    'red': (255, 250, 240),  # 象牙白
    'black': (245, 245, 220)  # 米黄色
}
# 棋子边框色
PIECE_BORDER_COLORS = {
    'red': (139, 0, 0),  # 深红
    'black': (25, 25, 25)  # 深黑
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
