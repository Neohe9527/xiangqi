# 百度云部署检查清单

## 第一步：准备工作
- [ ] 注册百度云账号
- [ ] 实名认证
- [ ] 充值账户余额

## 第二步：购买云服务器
- [ ] 选择配置：Ubuntu 20.04 LTS, 2核CPU, 4GB内存, 50GB SSD
- [ ] 完成支付
- [ ] 记录服务器 IP 地址

## 第三步：连接到服务器
- [ ] SSH 连接到服务器
- [ ] 更新系统：`sudo apt update && sudo apt upgrade -y`

## 第四步：安装 Docker
- [ ] 安装 Docker
- [ ] 验证安装：`docker --version`

## 第五步：安装 Docker Compose
- [ ] 下载并安装 Docker Compose
- [ ] 验证安装：`docker-compose --version`

## 第六步：克隆项目
- [ ] 安装 Git：`sudo apt install git -y`
- [ ] 克隆项目：`git clone https://github.com/Neohe9527/xiangqi.git`

## 第七步：启动应用
- [ ] 进入项目目录：`cd xiangqi`
- [ ] 启动容器：`docker-compose up -d --build`
- [ ] 验证运行：`docker-compose ps`

## 第八步：配置域名（可选）
- [ ] 购买域名
- [ ] 在百度云 DNS 中添加 A 记录
- [ ] 等待 DNS 生效

## 第九步：配置 HTTPS
- [ ] 安装 Certbot
- [ ] 获取证书：`sudo certbot certonly --standalone -d yourdomain.com`
- [ ] 更新 Nginx 配置
- [ ] 重启应用

## 第十步：验证部署
- [ ] 检查后端：`curl https://yourdomain.com/health`
- [ ] 访问前端：`https://yourdomain.com`
- [ ] 查看 API 文档：`https://yourdomain.com/docs`

## 快速参考命令

```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 重启应用
docker-compose restart

# 停止应用
docker-compose down

# 更新应用
git pull && docker-compose up -d --build
```

## 常见问题

### 连接超时
- 检查安全组规则（开放 80、443 端口）
- 检查防火墙设置

### 应用无法启动
- 查看日志：`docker-compose logs`
- 检查端口占用：`sudo netstat -tlnp`
- 检查磁盘空间：`df -h`

### 域名无法解析
- 等待 DNS 生效（可能需要几小时）
- 使用 `dig` 命令检查 DNS 记录

## 支持资源

- 百度云文档：https://cloud.baidu.com/doc
- Docker 文档：https://docs.docker.com
- 项目 GitHub：https://github.com/Neohe9527/xiangqi
