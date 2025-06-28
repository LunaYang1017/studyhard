# 考试复习助手公网部署指南

## 🚀 部署方案概览

本文档提供多种将考试复习助手部署到公网的方案，让所有人都能通过网址访问您的服务。

## 📋 部署前准备

### 1. 域名准备（可选但推荐）
- 购买域名（如：阿里云、腾讯云、GoDaddy等）
- 配置DNS解析

### 2. 服务器选择
- **云服务器**：阿里云、腾讯云、AWS、Azure等
- **容器平台**：Docker Hub、Kubernetes
- **PaaS平台**：Vercel、Netlify、Railway、Render等

## 🎯 推荐部署方案

### 方案一：Vercel + Railway（最简单）

#### 优势
- 免费额度充足
- 自动部署
- 无需服务器管理
- 支持自定义域名

#### 部署步骤

##### 1. 前端部署到Vercel

1. **准备前端代码**
```bash
# 构建生产版本
npm run build
```

2. **创建Vercel配置文件**
```javascript
// vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-backend-url.railway.app/$1"
    }
  ]
}
```

3. **部署到Vercel**
- 访问 [vercel.com](https://vercel.com)
- 连接GitHub仓库
- 自动部署

##### 2. 后端部署到Railway

1. **创建Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **创建railway.json**
```json
{
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

3. **部署到Railway**
- 访问 [railway.app](https://railway.app)
- 连接GitHub仓库
- 配置环境变量

### 方案二：Docker + 云服务器

#### 优势
- 完全控制
- 成本可控
- 适合高并发

#### 部署步骤

##### 1. 准备Docker配置

**创建docker-compose.yml**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - STEPFUN_API_KEY=your_api_key_here
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/data:/app/data
    restart: unless-stopped

  frontend:
    build: .
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: unless-stopped
```

**创建Dockerfile**
```dockerfile
# 多阶段构建
FROM node:18-alpine AS frontend-builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=frontend-builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**创建nginx.conf**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        # 前端静态文件
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }

        # API代理
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # 文件上传
        location /upload {
            proxy_pass http://backend/upload;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            client_max_body_size 10M;
        }

        # 健康检查
        location /health {
            proxy_pass http://backend/health;
        }
    }
}
```

##### 2. 服务器部署

1. **购买云服务器**
   - 推荐配置：2核4GB，带宽5Mbps以上
   - 操作系统：Ubuntu 20.04 LTS

2. **安装Docker**
```bash
# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **部署应用**
```bash
# 克隆代码
git clone your-repository-url
cd your-project

# 配置环境变量
cp .env.example .env
# 编辑.env文件，设置API密钥等

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 方案三：Serverless部署

#### 优势
- 按使用付费
- 自动扩缩容
- 无需服务器管理

#### 部署步骤

##### 1. 前端部署到Vercel

```bash
# 安装Vercel CLI
npm i -g vercel

# 部署
vercel --prod
```

##### 2. 后端部署到Vercel Functions

**创建api目录结构**
```
api/
├── chat.js
├── upload.js
├── health.js
└── _middleware.js
```

**示例API函数**
```javascript
// api/chat.js
import { createClient } from '@vercel/kv';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { message, session_id, knowledge_base_1, knowledge_base_2 } = req.body;
    
    // 调用大模型API
    const response = await fetch('https://api.stepfun.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.STEPFUN_API_KEY}`
      },
      body: JSON.stringify({
        model: 'step-1-8k',
        messages: [
          {
            role: 'user',
            content: `基于以下知识库回答问题：\n\n知识库1：${JSON.stringify(knowledge_base_1)}\n\n知识库2：${JSON.stringify(knowledge_base_2)}\n\n问题：${message}`
          }
        ]
      })
    });

    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
```

## 🔧 环境配置

### 1. 环境变量配置

**创建.env文件**
```env
# 服务器配置
HOST=0.0.0.0
PORT=8000
RELOAD=false

# API配置
STEPFUN_API_KEY=your_api_key_here
STEPFUN_BASE_URL=https://api.stepfun.com/v1
STEPFUN_MODEL=step-1-8k

# 安全配置
SECRET_KEY=your-secret-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 文件上传配置
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads

# 数据库配置（如果使用）
DATABASE_URL=your_database_url

# 域名配置
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

### 2. CORS配置更新

**更新backend/main.py中的CORS配置**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-domain.com",
        "https://www.your-domain.com",
        "https://your-app.vercel.app",
        # 开发环境
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

### 3. 前端配置更新

**更新src/config/api.js**
```javascript
export const API_CONFIG = {
  // 生产环境API地址
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'https://your-backend-domain.com',
  
  // 其他配置保持不变
  ENDPOINTS: {
    UPLOAD: '/upload',
    CHAT: '/chat',
    GENERATE_QUESTIONS: '/generate-questions',
    KNOWLEDGE_BASE: '/knowledge-base',
    SEARCH: '/search'
  },
  
  TIMEOUT: 30000,
  SUPPORTED_FILE_TYPES: {
    'application/pdf': ['.pdf'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    'text/plain': ['.txt'],
    'text/markdown': ['.md']
  },
  MAX_FILE_SIZE: 10 * 1024 * 1024,
}
```

## 🔒 安全配置

### 1. HTTPS配置

**使用Let's Encrypt免费SSL证书**
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自动续期
sudo crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. 防火墙配置

```bash
# 只开放必要端口
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 3. 安全头配置

**nginx安全头配置**
```nginx
# 在nginx.conf中添加
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

## 📊 监控和日志

### 1. 日志配置

**创建日志配置**
```python
# backend/logging_config.py
import logging
import logging.handlers
import os

def setup_logging():
    # 创建logs目录
    os.makedirs('logs', exist_ok=True)
    
    # 配置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 文件处理器
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
```

### 2. 健康检查

**添加健康检查端点**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "api": "ok",
            "file_storage": "ok"
        }
    }
```

## 🚀 自动化部署

### 1. GitHub Actions配置

**创建.github/workflows/deploy.yml**
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Vercel
      uses: amondnet/vercel-action@v25
      with:
        vercel-token: ${{ secrets.VERCEL_TOKEN }}
        vercel-org-id: ${{ secrets.ORG_ID }}
        vercel-project-id: ${{ secrets.PROJECT_ID }}
        vercel-args: '--prod'
    
    - name: Deploy Backend to Railway
      uses: bervProject/railway-deploy@v1.0.0
      with:
        railway_token: ${{ secrets.RAILWAY_TOKEN }}
        service: backend
```

### 2. 环境变量设置

在GitHub仓库的Settings > Secrets中添加：
- `VERCEL_TOKEN`
- `ORG_ID`
- `PROJECT_ID`
- `RAILWAY_TOKEN`
- `STEPFUN_API_KEY`

## 📈 性能优化

### 1. 前端优化

**代码分割**
```javascript
// 使用React.lazy进行代码分割
const ChatInterface = React.lazy(() => import('./components/ChatInterface'));
const FileUpload = React.lazy(() => import('./components/FileUpload'));
```

**图片优化**
```javascript
// 使用WebP格式
<img src="image.webp" alt="description" />
```

### 2. 后端优化

**缓存配置**
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```

**数据库连接池**
```python
from databases import Database

database = Database("postgresql://user:password@localhost/dbname")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
```

## 🔧 故障排除

### 常见问题

1. **CORS错误**
   - 检查CORS配置
   - 确认域名在允许列表中

2. **API调用失败**
   - 检查API密钥配置
   - 验证网络连接
   - 查看服务器日志

3. **文件上传失败**
   - 检查文件大小限制
   - 确认存储权限
   - 验证文件类型

4. **性能问题**
   - 启用缓存
   - 优化数据库查询
   - 使用CDN加速

## 📞 技术支持

如果在部署过程中遇到问题，请：

1. 查看服务器日志
2. 检查网络连接
3. 验证配置参数
4. 参考官方文档

## 🎯 下一步

部署完成后，建议：

1. 设置监控告警
2. 配置自动备份
3. 实施安全扫描
4. 优化用户体验
5. 收集用户反馈

---

**注意**：请根据您的具体需求和预算选择合适的部署方案。建议先在测试环境验证后再部署到生产环境。 