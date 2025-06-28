# 🚀 快速部署指南

## 📋 部署前准备

### 1. 选择部署方案

**推荐方案（按难度排序）：**

1. **Vercel + Railway（最简单）** - 免费，无需服务器
2. **Docker + 云服务器** - 完全控制，适合生产环境
3. **Serverless部署** - 按使用付费，自动扩缩容

### 2. 准备域名（可选）

- 购买域名（阿里云、腾讯云、GoDaddy等）
- 配置DNS解析

## 🎯 方案一：Vercel + Railway（推荐新手）

### 步骤1：准备代码

1. **确保代码已提交到GitHub**
```bash
git add .
git commit -m "准备部署"
git push origin main
```

2. **检查API密钥配置**
确保 `backend/main.py` 中的API密钥正确：
```python
API_KEY = "5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4"
```

### 步骤2：部署后端到Railway

1. **访问 [railway.app](https://railway.app)**
2. **使用GitHub登录**
3. **点击 "New Project"**
4. **选择 "Deploy from GitHub repo"**
5. **选择您的仓库**
6. **配置环境变量：**
   ```
   STEPFUN_API_KEY=5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4
   STEPFUN_BASE_URL=https://api.stepfun.com/v1
   STEPFUN_MODEL=step-1-8k
   ```
7. **等待部署完成，记录生成的URL**

### 步骤3：部署前端到Vercel

1. **访问 [vercel.com](https://vercel.com)**
2. **使用GitHub登录**
3. **点击 "New Project"**
4. **导入您的GitHub仓库**
5. **配置环境变量：**
   ```
   VITE_API_BASE_URL=https://your-backend-url.railway.app
   ```
6. **点击 "Deploy"**

### 步骤4：配置域名（可选）

1. **在Vercel项目设置中添加自定义域名**
2. **在域名提供商处配置DNS解析**
3. **等待DNS生效**

## 🐳 方案二：Docker + 云服务器

### 步骤1：购买云服务器

**推荐配置：**
- 阿里云/腾讯云 2核4GB
- 操作系统：Ubuntu 20.04 LTS
- 带宽：5Mbps以上

### 步骤2：连接服务器

```bash
ssh root@your-server-ip
```

### 步骤3：安装Docker

```bash
# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 步骤4：部署应用

```bash
# 克隆代码
git clone https://github.com/your-username/your-repo.git
cd your-repo

# 配置环境变量
cp env.example .env
nano .env  # 编辑配置

# 启动服务
chmod +x deploy.sh
./deploy.sh deploy
```

### 步骤5：配置域名和SSL

```bash
# 安装Nginx和Certbot
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx

# 配置域名
sudo nano /etc/nginx/sites-available/exam-review
# 添加域名配置

# 启用站点
sudo ln -s /etc/nginx/sites-available/exam-review /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com
```

## 🔧 方案三：一键部署脚本

### Windows用户

```powershell
# 运行PowerShell脚本
.\deploy.ps1 deploy
```

### Linux/Mac用户

```bash
# 运行Bash脚本
chmod +x deploy.sh
./deploy.sh deploy
```

## ✅ 部署验证

### 1. 检查服务状态

```bash
# 检查后端
curl http://your-domain.com/health

# 检查前端
curl http://your-domain.com
```

### 2. 功能测试

1. **访问前端页面**
2. **上传测试文件**
3. **测试聊天功能**
4. **验证文件管理**

### 3. 性能测试

```bash
# 压力测试（可选）
ab -n 100 -c 10 http://your-domain.com/health
```

## 🔒 安全配置

### 1. 防火墙设置

```bash
# 只开放必要端口
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 2. 安全头配置

确保nginx配置包含安全头：
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
```

### 3. API密钥保护

- 使用环境变量存储敏感信息
- 定期轮换API密钥
- 监控API使用情况

## 📊 监控和维护

### 1. 日志监控

```bash
# 查看应用日志
docker-compose logs -f

# 查看系统日志
sudo journalctl -u docker
```

### 2. 性能监控

- 监控CPU、内存使用率
- 监控磁盘空间
- 监控网络流量

### 3. 备份策略

```bash
# 备份数据
docker-compose exec backend tar -czf backup.tar.gz uploads/ data/

# 定期备份
crontab -e
# 添加：0 2 * * * /path/to/backup.sh
```

## 🚨 故障排除

### 常见问题

1. **CORS错误**
   - 检查CORS配置
   - 确认域名在允许列表中

2. **API调用失败**
   - 检查API密钥
   - 验证网络连接
   - 查看服务器日志

3. **文件上传失败**
   - 检查文件大小限制
   - 确认存储权限
   - 验证文件类型

4. **服务无法启动**
   - 检查端口占用
   - 验证配置文件
   - 查看错误日志

### 获取帮助

如果遇到问题：
1. 查看部署日志
2. 检查配置文件
3. 验证网络连接
4. 参考官方文档

## 🎯 下一步

部署完成后：

1. **设置监控告警**
2. **配置自动备份**
3. **实施安全扫描**
4. **优化用户体验**
5. **收集用户反馈**

---

**恭喜！** 您的考试复习助手已成功部署到公网，所有人都可以通过网址访问了！

**访问地址：** https://your-domain.com 