# 中国象棋游戏设计文档

## 项目概述

开发一个功能完整的中国象棋桌面游戏，使用 Python + Pygame 实现。支持人机对弈、AI vs AI 对弈、残局布置等功能，提供多个不同难度和策略的 AI 对手。

## 技术栈

- **语言**: Python 3.8+
- **UI 框架**: Pygame 2.x
- **数据结构**: NumPy（可选，用于加速数组操作）
- **测试**: pytest
- **代码质量**: black（格式化）、pylint（静态检查）

## 项目结构

```
xiangqi/
├── main.py                 # 程序入口
├── config.py              # 全局配置（窗口大小、颜色、路径等）
├── core/                  # 核心游戏逻辑
│   ├── __init__.py
│   ├── board.py          # 棋盘状态管理
│   ├── piece.py          # 棋子定义和移动规则
│   ├── rules.py          # 游戏规则（将军、胜负判定等）
│   └── move.py           # 走法表示和验证
├── ai/                    # AI 引擎
│   ├── __init__.py
│   ├── base_ai.py        # AI 基类接口
│   ├── random_ai.py      # 随机走子 AI
│   ├── greedy_ai.py      # 贪心算法 AI
│   ├── minimax_ai.py     # Minimax 算法 AI
│   ├── alphabeta_ai.py   # Alpha-Beta 剪枝 AI
│   ├── evaluator.py      # 局面评估函数
│   └── opening_book.py   # 开局库
├── ui/                    # 用户界面
│   ├── __init__.py
│   ├── game_window.py    # 主游戏窗口
│   ├── board_renderer.py # 棋盘渲染
│   ├── piece_renderer.py # 棋子渲染
│   ├── menu.py           # 菜单系统
│   ├── info_panel.py     # 信息面板（AI思考、评分等）
│   └── setup_mode.py     # 残局布置界面
├── game/                  # 游戏管理
│   ├── __init__.py
│   ├── game_manager.py   # 游戏状态管理
│   ├── player.py         # 玩家抽象（人类/AI）
│   ├── history.py        # 走棋历史记录
│   └── pgn.py            # 棋谱保存/加载
├── assets/               # 资源文件
│   ├── images/          # 棋子图片
│   ├── fonts/           # 字体
│   └── presets/         # 预设残局（可选扩展）
└── tests/               # 单元测试
    └── ...
```

## 架构设计

### 分层架构

**Core 层（核心逻辑）**
- 纯逻辑，不依赖 UI
- 可独立测试
- 包含：棋盘、棋子、移动规则、游戏规则

**AI 层（人工智能）**
- 实现各种策略
- 通过统一接口调用
- 依赖 Core 层的棋盘和规则

**UI 层（用户界面）**
- 负责渲染和用户交互
- 使用 Pygame 实现
- 依赖 Game 层

**Game 层（游戏管理）**
- 协调各层
- 管理游戏流程
- 处理玩家（人类/AI）交互

### 依赖方向

```
UI → Game → Core/AI
AI → Core
```

各层之间通过接口通信，降低耦合。

## AI 系统设计

### AI 角色定义

**1. 新手小卒（RandomAI）**
- **算法**: 完全随机选择合法走法
- **特点**: 不可预测，适合初学者建立信心
- **思考时间**: 即时（< 0.1秒）

**2. 贪心将军（GreedyAI）**
- **算法**: 评估所有走法，优先吃子 > 威胁对方 > 保护己方
- **评分规则**: 车=9, 马炮=4.5, 士象=2, 兵卒=1, 将帅=无穷
- **特点**: 激进，但缺乏长远规划
- **思考时间**: < 0.5秒

**3. 谋略军师（MinimaxAI）**
- **算法**: Minimax 搜索，深度 3-4 层
- **评估函数**: 子力价值 + 位置价值 + 灵活性
- **特点**: 有一定战术深度，能看到 2-3 步后的局面
- **思考时间**: 1-3秒

**4. 深算国手（AlphaBetaAI）**
- **算法**: Alpha-Beta 剪枝，深度 5-7 层（动态调整）
- **增强特性**:
  - 开局库（前 10 步使用经典开局）
  - 残局库（子力 ≤ 10 时使用残局定式）
  - 迭代加深（时间限制内尽可能深搜）
  - 置换表（缓存已评估局面）
  - 走法排序（优先搜索可能的好棋）
- **评估函数**: 子力 + 位置 + 控制力 + 将帅安全 + 子力协调
- **特点**: 接近业余高手水平
- **思考时间**: 3-10秒（可配置）

### AI 基类接口

```python
class BaseAI:
    def __init__(self, name, color, difficulty):
        self.name = name
        self.color = color  # 'red' or 'black'
        self.difficulty = difficulty
        self.thinking_info = {}  # 思考过程信息

    def get_move(self, board, time_limit=None):
        """返回最佳走法"""
        pass

    def get_thinking_info(self):
        """返回思考过程信息用于可视化"""
        return {
            'depth': 0,
            'nodes_evaluated': 0,
            'best_move': None,
            'score': 0,
            'principal_variation': [],  # 主要变化
            'candidate_moves': []  # [(move, score), ...]
        }
```

### 评估函数设计

**多维度评分系统**：
- **子力价值（40%）**: 基础子力分值
- **位置价值（25%）**: 棋子在不同位置的价值（如炮在中路更强）
- **灵活性（15%）**: 可走位置数量
- **将帅安全（10%）**: 是否被将军、逃跑路线
- **子力协调（10%）**: 马炮配合、车炮联动等

## UI 设计

### 主界面布局

```
┌─────────────────────────────────────────────────────────────┐
│  中国象棋 - Chinese Chess                    [_] [□] [X]     │
├─────────────────────────────────────────────────────────────┤
│  [新游戏] [悔棋] [布置残局] [保存] [加载] [设置]            │
├──────────────────────────┬──────────────────────────────────┤
│                          │  游戏信息                         │
│                          │  ────────────────                 │
│                          │  红方: 人类玩家                   │
│                          │  黑方: 深算国手 (AI)              │
│                          │                                   │
│      棋盘区域            │  当前回合: 红方                   │
│    (800x900 像素)        │  用时: 00:05:23                   │
│                          │                                   │
│                          │  AI 思考分析                      │
│                          │  ────────────────                 │
│                          │  搜索深度: 6 层                   │
│                          │  已评估: 12,458 个局面            │
│                          │  局面评分: +2.3 (红方优势)       │
│                          │  最佳走法: 炮八平五               │
│                          │                                   │
│                          │  主要变化:                        │
│                          │  1. 炮八平五 马2进3               │
│                          │  2. 车一平二 炮8平5               │
│                          │                                   │
│                          │  候选走法:                        │
│                          │  炮八平五 (+2.3)                  │
│                          │  车一进一 (+1.8)                  │
│                          │  马二进三 (+1.5)                  │
│                          │                                   │
│                          │  走棋历史                         │
│                          │  ────────────────                 │
│                          │  1. 炮二平五 炮8平5               │
│                          │  2. 马二进三 马8进7               │
│                          │  3. 车一平二 ...                  │
└──────────────────────────┴──────────────────────────────────┘
```

### 残局布置模式

进入布置模式后：
- 左侧显示棋子面板（红方和黑方各类棋子）
- 拖拽棋子到棋盘上放置
- 点击棋盘上的棋子可删除
- 验证按钮：检查布局是否合法（双方各有一个将/帅，不能对面等）
- 完成按钮：保存布局并开始游戏
- 取消按钮：返回正常模式

## 游戏流程

### 启动流程
1. 显示主菜单：人机对弈 / AI vs AI / 残局布置 / 加载棋谱
2. 选择对弈模式后，配置双方（人类/选择 AI）
3. 可设置计时规则（无限时/限时）

### 对弈流程
- **人类回合**: 点击棋子显示可走位置，点击目标位置完成移动
- **AI 回合**: 显示"思考中..."，实时更新思考信息，完成后自动走棋
- **每步棋后**: 更新棋盘、记录历史、检查胜负

### AI vs AI 模式
- 可设置每步思考时间
- 可暂停/继续/单步执行
- 实时显示双方的思考分析对比

### 功能按钮
- **悔棋**: 人机对弈时悔两步（人和 AI 各一步）
- **提示**: 显示 AI 推荐的走法
- **保存/加载**: 使用 PGN 格式保存棋谱
- **设置**: 调整 AI 难度、思考时间、界面主题等

## 核心数据结构

### 棋盘表示

```python
class Board:
    def __init__(self):
        # 10x9 二维数组，存储棋子对象或 None
        self.grid = [[None for _ in range(9)] for _ in range(10)]
        self.red_pieces = []  # 红方棋子列表
        self.black_pieces = []  # 黑方棋子列表
        self.hash_value = 0  # Zobrist 哈希值，用于置换表

    def get_piece(self, row, col):
        """获取指定位置的棋子"""

    def make_move(self, move):
        """执行走法，返回被吃的棋子（用于撤销）"""

    def undo_move(self, move, captured_piece):
        """撤销走法"""

    def get_legal_moves(self, color):
        """获取某方所有合法走法"""

    def is_in_check(self, color):
        """判断某方是否被将军"""

    def is_checkmate(self, color):
        """判断某方是否被将死"""
```

### 棋子表示

```python
class Piece:
    def __init__(self, piece_type, color, row, col):
        self.type = piece_type  # 'K'将, 'A'士, 'E'象, 'H'马, 'R'车, 'C'炮, 'P'兵
        self.color = color  # 'red' or 'black'
        self.row = row
        self.col = col

    def get_possible_moves(self, board):
        """返回该棋子的所有可能走法（不考虑是否送将）"""

    def get_legal_moves(self, board):
        """返回合法走法（过滤掉送将的走法）"""
```

### 走法表示

```python
class Move:
    def __init__(self, from_pos, to_pos, piece, captured=None):
        self.from_pos = (row, col)  # 起始位置
        self.to_pos = (row, col)    # 目标位置
        self.piece = piece           # 移动的棋子
        self.captured = captured     # 被吃的棋子（如果有）

    def to_chinese(self):
        """转换为中文记谱，如"炮二平五""""
```

## 关键算法

### 走法生成
- 为每种棋子实现特定的移动规则
- 马：日字，需检查蹩马腿
- 象：田字，不能过河
- 炮：隔子吃子
- 将/帅：九宫格内，不能对面
- 使用位运算优化边界检查

### Alpha-Beta 剪枝

```python
def alpha_beta(board, depth, alpha, beta, maximizing):
    # 查置换表
    if board.hash in transposition_table:
        return cached_value

    # 到达搜索深度或终局
    if depth == 0 or game_over:
        return evaluate(board)

    # 走法排序（提高剪枝效率）
    moves = order_moves(board.get_legal_moves())

    if maximizing:
        max_eval = -infinity
        for move in moves:
            board.make_move(move)
            eval = alpha_beta(board, depth-1, alpha, beta, False)
            board.undo_move(move)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta 剪枝
        return max_eval
    else:
        # 类似的最小化逻辑
```

### 局面评估

```python
def evaluate(board):
    score = 0

    # 子力价值
    piece_values = {'K': 10000, 'R': 900, 'C': 450, 'H': 450,
                    'A': 200, 'E': 200, 'P': 100}

    for piece in board.all_pieces:
        value = piece_values[piece.type]
        # 位置价值（使用位置价值表）
        value += position_value_table[piece.type][piece.row][piece.col]
        # 灵活性
        value += len(piece.get_legal_moves(board)) * 5

        score += value if piece.color == 'red' else -value

    # 将帅安全
    score += evaluate_king_safety(board)

    # 子力协调（如马炮配合）
    score += evaluate_piece_coordination(board)

    return score
```

### Zobrist 哈希
- 为每个棋子在每个位置预生成随机数
- 快速计算棋盘哈希值，用于置换表
- 增量更新：走棋时只需异或操作

## 测试策略

### 单元测试

```
tests/
├── test_board.py          # 棋盘操作测试
│   ├── test_piece_placement
│   ├── test_move_execution
│   ├── test_move_undo
│   └── test_hash_consistency
├── test_pieces.py         # 棋子移动规则测试
│   ├── test_rook_moves
│   ├── test_cannon_moves
│   ├── test_horse_moves
│   └── test_elephant_moves
├── test_rules.py          # 游戏规则测试
│   ├── test_check_detection
│   ├── test_checkmate_detection
│   ├── test_stalemate
│   └── test_illegal_moves
├── test_ai.py             # AI 算法测试
│   ├── test_minimax_correctness
│   ├── test_alphabeta_equivalence
│   ├── test_evaluation_function
│   └── test_move_ordering
└── test_pgn.py            # 棋谱保存/加载测试
```

### 集成测试
- 完整对局测试：从开局到终局
- AI vs AI 测试：验证不同 AI 能正常对弈
- 残局测试：加载经典残局，验证 AI 能找到正解

### 性能测试
- 走法生成速度：目标 > 100,000 局面/秒
- AI 搜索深度：在 5 秒内达到 6-7 层
- 内存使用：置换表大小控制

## 可扩展性设计

### 新增 AI 策略
- 继承 `BaseAI` 类
- 实现 `get_move()` 方法
- 在配置文件中注册新 AI

### 自定义评估函数
- 评估函数模块化，可插拔
- 支持加载外部评估参数文件
- 可通过机器学习训练评估参数

### 网络对弈扩展
- Core 层已与 UI 解耦，易于添加网络层
- 可实现：局域网对弈、在线对弈、观战模式

### 开局库和残局库扩展
- 使用标准格式存储（JSON/SQLite）
- 支持导入第三方开局库
- 用户可添加自定义开局

### UI 主题
- 棋盘和棋子样式可配置
- 支持多套皮肤（传统、现代、3D 等）

## 开发优先级

### Phase 1: 核心功能（2-3 周）
1. 实现棋盘、棋子、移动规则
2. 实现基本 UI（棋盘渲染、鼠标交互）
3. 实现随机 AI 和贪心 AI
4. 基本的人机对弈功能

### Phase 2: 高级 AI（2-3 周）
1. 实现 Minimax 和 Alpha-Beta 算法
2. 优化评估函数
3. 添加置换表和走法排序
4. 实现开局库

### Phase 3: 完整功能（1-2 周）
1. AI vs AI 模式
2. 残局布置功能
3. 走棋历史和悔棋
4. 棋谱保存/加载
5. AI 思考过程可视化

### Phase 4: 优化和扩展（1 周）
1. 性能优化
2. 完善 UI 和用户体验
3. 添加计时、统计等功能
4. 编写文档和测试

## 技术要点

### 性能优化
- 使用位运算优化边界检查
- 走法排序提高剪枝效率
- 置换表缓存已评估局面
- 迭代加深搜索

### 用户体验
- 流畅的动画效果
- 清晰的视觉反馈
- 直观的操作方式
- 详细的 AI 分析信息

### 代码质量
- 模块化设计
- 单元测试覆盖
- 代码注释和文档
- 遵循 PEP 8 规范

## 总结

本设计文档详细描述了中国象棋游戏的完整架构、功能设计和实现方案。通过模块化的架构设计，确保代码的可维护性和可扩展性。四个不同难度的 AI 对手提供了丰富的游戏体验，从初学者到高级玩家都能找到合适的挑战。完整的功能集包括人机对弈、AI vs AI、残局布置、棋谱管理等，满足各种使用场景。
