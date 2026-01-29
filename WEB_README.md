# 中国象棋 Web 版

前后端分离的中国象棋游戏，支持人机对弈。

## 技术栈

### 后端
- **FastAPI** - 高性能异步 Web 框架
- **WebSocket** - 实时游戏状态同步
- **Python 3.11+**

### 前端
- **React 18** + **TypeScript**
- **Vite** - 构建工具
- **Tailwind CSS** - 样式框架
- **Zustand** - 状态管理
- **Canvas API** - 棋盘渲染

### 部署
- **Docker** + **docker-compose**
- **Nginx** - 反向代理

## 项目结构

```
xiangqi/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # REST API 和 WebSocket
│   │   ├── core/           # 核心游戏逻辑
│   │   ├── ai/             # AI 引擎
│   │   ├── services/       # 业务服务
│   │   ├── config.py       # 配置
│   │   └── main.py         # 入口
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # 前端应用
│   ├── src/
│   │   ├── components/     # React 组件
│   │   ├── hooks/          # 自定义 Hooks
│   │   ├── stores/         # Zustand 状态
│   │   ├── types/          # TypeScript 类型
│   │   └── utils/          # 工具函数
│   ├── Dockerfile
│   └── package.json
├── nginx/                   # Nginx 配置
├── docker-compose.yml       # 容器编排
└── README.md
```

## 快速开始

### 本地开发

#### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000

### Docker 部署

```bash
# 构建并启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

访问 http://localhost

## API 文档

启动后端后访问 http://localhost:8000/docs 查看 Swagger 文档。

### REST API

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/v1/games | 创建新游戏 |
| GET | /api/v1/games/{id} | 获取游戏状态 |
| POST | /api/v1/games/{id}/moves | 走棋 |
| POST | /api/v1/games/{id}/ai-move | AI 走棋 |
| POST | /api/v1/games/{id}/undo | 悔棋 |
| POST | /api/v1/games/{id}/legal-moves | 获取合法走法 |

### WebSocket

连接: `ws://localhost:8000/ws/games/{game_id}`

消息类型:
- `move` - 走棋
- `request_ai_move` - 请求 AI 走棋
- `undo` - 悔棋
- `get_legal_moves` - 获取合法走法

## AI 难度

| 名称 | 算法 | 描述 |
|------|------|------|
| 新手小卒 | Random | 随机走子，适合初学者 |
| 贪心将军 | Greedy | 优先吃子，激进但缺乏规划 |
| 谋略军师 | Minimax | 有战术深度 |
| 深算国手 | Alpha-Beta | 最强 AI，深度搜索 |

## 云部署指南

### 阿里云 ECS

1. 购买 ECS 实例（推荐 2核4G 以上）
2. 安装 Docker 和 docker-compose
3. 上传代码或 git clone
4. 运行 `docker-compose up -d`
5. 配置安全组开放 80 端口

### 百度云 BCC

1. 购买 BCC 实例
2. 安装 Docker 环境
3. 部署步骤同上

### HTTPS 配置（可选）

使用 Let's Encrypt 免费证书：

```bash
# 安装 certbot
apt install certbot python3-certbot-nginx

# 获取证书
certbot --nginx -d your-domain.com
```

## 开发说明

### 添加新 AI

1. 在 `backend/app/ai/` 创建新的 AI 类
2. 继承 `BaseAI` 并实现 `get_move` 方法
3. 在 `config.py` 的 `AI_CONFIGS` 中注册
4. 在 `game_service.py` 的 `get_ai` 方法中添加实例化逻辑

### 前端组件

- `GameBoard` - 棋盘主组件
- `BoardCanvas` - Canvas 渲染
- `InfoPanel` - 游戏信息面板
- `ControlPanel` - 控制按钮

## License

MIT
