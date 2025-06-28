# API密钥配置说明

## 您的API密钥已配置

您的API密钥 `5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4` 已经配置到后端代码中。

## 配置位置

### 后端配置
- **文件**: `backend/main.py`
- **位置**: 第25-26行
```python
API_KEY = "5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4"
API_BASE_URL = "http://localhost:8000/api"  # 您的大模型API地址
```

## 使用方法

### 1. 启动服务
```bash
# 方法1: 使用启动脚本（推荐）
python start_app.py

# 方法2: 分别启动
# 终端1 - 启动后端
cd backend
python main.py

# 终端2 - 启动前端
npm run dev
```

### 2. 访问应用
- **前端**: http://localhost:3000 或 http://localhost:3001
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

### 3. 功能说明

#### 上传知识库
1. 点击"上传资料"标签
2. 上传复习资料到知识库1
3. 上传考试题目到知识库2

#### 开始复习
1. 点击"开始复习"标签
2. 在聊天界面输入问题
3. AI会基于您的知识库生成答案和题目

## API调用流程

1. **前端发送消息** → `POST /chat`
2. **后端处理** → 调用您的大模型API
3. **返回结果** → 包含答案和知识库引用

## 故障排除

### 如果API调用失败
- 检查网络连接
- 确认API密钥正确
- 查看后端日志输出
- 系统会自动使用模拟API作为备用方案

### 端口冲突
- 如果3000端口被占用，会自动使用3001
- 如果8000端口被占用，会自动使用8001

## 安全注意事项

⚠️ **重要**: 您的API密钥已经硬编码在代码中，仅用于开发测试。在生产环境中，请使用环境变量来存储敏感信息。

## 下一步

1. 确保您的大模型API服务正在运行
2. 修改 `API_BASE_URL` 为您的实际API地址
3. 测试上传文件和聊天功能
4. 根据需要调整API调用参数

## 联系支持

如果您在使用过程中遇到问题，请检查：
1. 后端控制台日志
2. 前端浏览器控制台
3. 网络连接状态
4. API密钥有效性 