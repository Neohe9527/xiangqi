"""
Backend configuration
"""

# Piece values (copied from original config)
PIECE_VALUES = {
    'K': 10000,
    'R': 900,
    'C': 450,
    'H': 450,
    'A': 200,
    'E': 200,
    'P': 100
}

# AI configurations
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
        'description': 'Alpha-Beta剪枝，强大的求胜欲望',
        'depth': 8,
        'time_limit': 30
    },
    'master': {
        'name': '绝世棋圣',
        'difficulty': 5,
        'description': '最强AI，深度搜索+高级优化，挑战极限',
        'depth': 10,
        'time_limit': 60,
        'quiescence_depth': 8
    }
}

# Game session settings
SESSION_TIMEOUT = 3600  # 1 hour
MAX_SESSIONS = 1000
