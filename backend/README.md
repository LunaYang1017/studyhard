# 考试复习助手 - Python后端

这是考试复习助手的Python后端API服务，使用FastAPI框架构建。

## 功能特点

- 🚀 **FastAPI框架**：高性能异步Web框架
- 🤖 **大模型集成**：支持OpenAI、Claude等大模型API
- 📁 **文件上传**：支持PDF、DOCX、TXT、MD文件
- 🔒 **安全配置**：CORS、文件验证、API密钥管理
- 📊 **API文档**：自动生成的Swagger文档
- 🔄 **热重载**：开发时自动重启服务

## 快速开始

### 1. 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
# 服务器配置
HOST=0.0.0.0
PORT=8000
RELOAD=true

# 大模型API配置（至少配置一个）
OPENAI_API_KEY=your_openai_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here
CUSTOM_AI_API_KEY=your_custom_ai_api_key_here

# 安全配置
SECRET_KEY=your_secret_key_here
```

### 3. 启动服务器

```bash
python start_server.py
```

或者直接运行：

```bash
python main.py
```

服务器将在 `http://localhost:8000` 启动

## API端点

### 基础端点

- `GET /` - 根路径，检查服务状态
- `GET /health` - 健康检查
- `GET /docs` - API文档（Swagger UI）

### 文件管理

- `POST /upload` - 上传文件到知识库
- `GET /knowledge-base` - 获取知识库文件列表
- `GET /knowledge-base/{file_id}` - 获取文件内容

### AI服务

- `POST /chat` - 与AI聊天
- `POST /generate-questions` - 生成题目

## 大模型API集成

### 支持的API

1. **OpenAI API**
   - 模型：GPT-3.5-turbo, GPT-4
   - 配置：`OPENAI_API_KEY`

2. **Claude API**
   - 模型：Claude-3-sonnet
   - 配置：`CLAUDE_API_KEY`

3. **自定义API**
   - 支持任意大模型API
   - 配置：`CUSTOM_AI_API_KEY`, `CUSTOM_AI_API_URL`

### 集成步骤

1. **获取API密钥**
   - OpenAI: https://platform.openai.com/api-keys
   - Claude: https://console.anthropic.com/

2. **配置环境变量**
   ```env
   OPENAI_API_KEY=sk-your-api-key-here
   ```

3. **重启服务器**
   ```bash
   python start_server.py
   ```

## 文件上传

### 支持的文件类型

- PDF文件 (`.pdf`)
- Word文档 (`.docx`)
- 文本文件 (`.txt`)
- Markdown文件 (`.md`)

### 文件大小限制

默认最大10MB，可在配置中修改：

```env
MAX_FILE_SIZE=10485760  # 10MB
```

## 开发指南

### 项目结构

```
backend/
├── main.py              # 主应用文件
├── ai_service.py        # 大模型API服务
├── config.py            # 配置文件
├── start_server.py      # 启动脚本
├── requirements.txt     # Python依赖
├── README.md           # 说明文档
├── uploads/            # 文件上传目录
└── logs/               # 日志目录
```

### 添加新的AI服务

1. 在 `ai_service.py` 中创建新的服务类：

```python
class NewAIService(AIService):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("NEW_AI_API_KEY")
        self.base_url = "https://api.new-ai.com/v1/chat"
    
    async def call_api(self, message: str, knowledge_base_1: List, knowledge_base_2: List) -> Dict[str, Any]:
        # 实现API调用逻辑
        pass
```

2. 在工厂函数中添加支持：

```python
def create_ai_service(service_type: str = "openai", **kwargs) -> AIService:
    if service_type == "new_ai":
        return NewAIService()
    # ... 其他服务
```

### 自定义配置

修改 `config.py` 中的配置类：

```python
class Config:
    # 添加新的配置项
    NEW_AI_API_KEY = os.getenv("NEW_AI_API_KEY")
    NEW_AI_BASE_URL = os.getenv("NEW_AI_BASE_URL")
```

## 部署

### 开发环境

```bash
python start_server.py
```

### 生产环境

1. **使用Gunicorn**：
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **使用Docker**：
   ```dockerfile
   FROM python:3.9
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "start_server.py"]
   ```

3. **使用systemd服务**：
   ```ini
   [Unit]
   Description=Exam Review Assistant API
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/backend
   Environment=PATH=/path/to/venv/bin
   ExecStart=/path/to/venv/bin/python start_server.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查找占用端口的进程
   netstat -tulpn | grep :8000
   # 终止进程
   kill -9 <PID>
   ```

2. **依赖安装失败**
   ```bash
   # 升级pip
   pip install --upgrade pip
   # 使用国内镜像
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

3. **API密钥错误**
   - 检查环境变量是否正确设置
   - 验证API密钥是否有效
   - 检查网络连接

4. **文件上传失败**
   - 检查文件大小是否超限
   - 验证文件类型是否支持
   - 确保上传目录有写权限

### 日志查看

```bash
# 查看实时日志
tail -f logs/app.log

# 查看错误日志
grep ERROR logs/app.log
```

## API文档

启动服务器后，访问 `http://localhost:8000/docs` 查看完整的API文档。

## 许可证

MIT License 