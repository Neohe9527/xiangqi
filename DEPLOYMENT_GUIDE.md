# 百度云部署指南

## 1. 购买云服务器

### 推荐配置
- **操作系统**: Ubuntu 20.04 LTS
- **CPU**: 2核
- **内存**: 4GB
- **存储**: 50GB SSD
- **带宽**: 5Mbps

### 购买步骤
1. 登录 [百度云控制台](https://console.bce.baidu.com)
2. 进入 BCC (云服务器) 页面
3. 点击"创建实例"
4. 选择上述配置
5. 完成支付

## 2. 连接到服务器

```bash
# 使用 SSH 连接
ssh -i your_key.pem ubuntu@your_server_ip

# 或使用密码连接
ssh ubuntu@your_server_ip
```

## 3. 安装 Docker

```bash
# 更新系统
sudo apt update
sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 添加当前用户到 docker 组
sudo usermod -aG docker $USER
newgrp docker

# 验证安装
docker --version
```

## 4. 安装 Docker Compose

```bash
# 下载 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 添加执行权限
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker-compose --version
```

## 5. 克隆项目

```bash
# 安装 Git
sudo apt install git -y

# 克隆项目
git clone https://github.com/Neohe9527/xiangqi.git
cd xiangqi
```

## 6. 配置环境

```bash
# 创建 .env 文件（如需要）
cat > .env << 'ENVEOF'
# 后端配置
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# 前端配置
FRONTEND_HOST=0.0.0.0
FRONTEND_PORT=80
ENVEOF
```

## 7. 启动应用

```bash
# 构建并启动容器
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 检查容器状态
docker-compose ps
```

## 8. 配置域名（可选）

### 在百度云 DNS 中添加记录

1. 登录百度云控制台
2. 进入 DNS 服务
3. 添加 A 记录：
   - 主机记录: `xiangqi` (或 `@` 表示根域名)
   - 记录类型: `A`
   - 记录值: 你的服务器 IP

### 验证域名

```bash
# 等待 DNS 生效（可能需要几分钟到几小时）
nslookup xiangqi.yourdomain.com
```

## 9. 配置 HTTPS（使用 Let's Encrypt）

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot certonly --standalone -d xiangqi.yourdomain.com

# 证书位置
# /etc/letsencrypt/live/xiangqi.yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/xiangqi.yourdomain.com/privkey.pem
```

## 10. 更新 Nginx 配置

编辑 `nginx/nginx.conf`：

```nginx
server {
    listen 443 ssl http2;
    server_name xiangqi.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/xiangqi.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xiangqi.yourdomain.com/privkey.pem;

    # ... 其他配置
}

# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name xiangqi.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## 11. 重启应用

```bash
# 重新构建并启动
docker-compose down
docker-compose up -d --build

# 查看日志
docker-compose logs -f
```

## 12. 验证部署

```bash
# 检查后端
curl https://xiangqi.yourdomain.com/health

# 检查前端
curl https://xiangqi.yourdomain.com/

# 查看 API 文档
# 访问 https://xiangqi.yourdomain.com/docs
```

## 13. 配置自动续期证书

```bash
# 创建续期脚本
sudo crontab -e

# 添加以下行（每月检查一次）
0 0 1 * * certbot renew --quiet && docker-compose -f /path/to/docker-compose.yml restart
```

## 14. 监控和维护

```bash
# 查看容器日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 查看资源使用
docker stats

# 更新应用
cd /path/to/xiangqi
git pull
docker-compose up -d --build
```

## 常见问题

### 1. 连接超时
- 检查安全组规则，确保开放了 80 和 443 端口
- 检查防火墙设置

### 2. 域名无法解析
- 等待 DNS 生效（可能需要几小时）
- 使用 `nslookup` 或 `dig` 命令检查

### 3. HTTPS 证书错误
- 确保域名正确
- 检查证书文件路径
- 重新生成证书

### 4. 应用无法启动
- 查看 Docker 日志：`docker-compose logs`
- 检查端口是否被占用
- 检查磁盘空间

## 性能优化

```bash
# 增加 Docker 内存限制
# 编辑 docker-compose.yml
services:
  backend:
    mem_limit: 2g
  frontend:
    mem_limit: 1g
```

## 备份和恢复

```bash
# 备份数据
docker-compose exec backend tar czf - /app > backup.tar.gz

# 恢复数据
tar xzf backup.tar.gz
```

## 安全建议

1. 定期更新系统和依赖
2. 使用强密码
3. 配置 SSH 密钥认证
4. 启用防火墙
5. 定期备份数据
6. 监控日志文件

