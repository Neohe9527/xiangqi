# 象棋游戏 Vercel 部署说明

## 前端部署状态

✅ **前端已成功部署到 Vercel**

- **生产环境 URL**: https://xiangqi-amber.vercel.app
- **项目**: xiangqi
- **框架**: React + Vite + TypeScript

## 完整使用方式

这个项目是前后端分离的架构。要完整运行游戏，需要同时运行前端和后端。

### 方式 1: 本地开发（推荐用于测试）

#### 启动后端服务
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 启动前端开发服务器
```bash
cd frontend
npm install
npm run dev
```

然后访问 `http://localhost:3000`

### 方式 2: 使用 Docker Compose（推荐用于生产）

```bash
docker-compose up
```

这将同时启动：
- 前端服务（端口 3000）
- 后端 API 服务（端口 8000）
- Nginx 反向代理（端口 80）

### 方式 3: 仅使用前端（当前 Vercel 部署）

当前 Vercel 部署只包含前端。要使其完全可用，需要：

1. **部署后端到云服务**（如 Railway、Render、Heroku 等）
2. **更新前端 API 配置**以指向部署的后端 URL

#### 更新 API 配置

编辑 `frontend/src/utils/api.ts`，将：
```typescript
const API_BASE = '/api/v1';
```

改为：
```typescript
const API_BASE = 'https://your-backend-url.com/api/v1';
```

然后重新部署前端。

## 后端部署选项

### 推荐方案：使用 Railway

1. 在 [Railway.app](https://railway.app) 上创建账户
2. 连接 GitHub 仓库
3. 创建新项目，选择 Python 环境
4. 配置环境变量和启动命令
5. 获取部署 URL

### 其他选项

- **Render**: https://render.com
- **Heroku**: https://www.heroku.com
- **AWS Lambda**: 需要额外配置
- **Google Cloud Run**: 需要 Docker 镜像

## 项目结构

```
xiangqi/
├── frontend/          # React + Vite 前端应用
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── backend/           # FastAPI 后端服务
│   ├── app/
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml # Docker 编排配置
└── vercel.json       # Vercel 部署配置
```

## 功能特性

- ✅ 完整的象棋游戏规则实现
- ✅ AI 对手（多种难度）
- ✅ 实时游戏状态同步
- ✅ 悔棋功能
- ✅ 游戏历史记录
- ✅ 响应式设计

## 下一步

1. **部署后端**: 选择合适的云服务部署后端 API
2. **更新 API 配置**: 在前端配置中指向部署的后端 URL
3. **重新部署前端**: 推送更新到 GitHub，Vercel 会自动重新部署

## 支持

如有问题，请查看：
- 前端日志: 浏览器开发者工具 (F12)
- 后端日志: 查看部署服务的日志
- 项目文档: 查看 README.md 和其他文档文件
