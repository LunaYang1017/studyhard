# 考试复习助手启动指南

## 🚀 快速启动

### 1. 启动后端服务
```bash
cd backend
python main.py
```

**预期输出：**
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 2. 启动前端服务（新开一个终端）
```bash
npm run dev
```

**预期输出：**
```
VITE v5.4.19  ready in 335 ms
➜  Local:   http://localhost:3001/
```

### 3. 访问应用
- **前端页面**: http://localhost:3001
- **后端API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 🔧 API配置说明

### 您的API密钥已配置
- **密钥**: `5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4`
- **位置**: `backend/main.py` 第25行

### API调用流程
1. **前端发送请求** → 后端API
2. **后端调用大模型** → 使用您的API密钥
3. **返回结果** → 包含知识库引用的答案

## 🧪 测试API功能

### 运行测试脚本
```bash
python test_api.py
```

### 手动测试
1. **健康检查**: `GET http://localhost:8000/health`
2. **聊天测试**: `POST http://localhost:8000/chat`
3. **生成题目**: `POST http://localhost:8000/generate-questions`

## 📝 功能说明

### 已修复的问题
✅ **题目生成**: 现在会调用大模型API生成基于知识库的题目  
✅ **知识库内容**: 正确读取和传递文件内容  
✅ **API调用**: 使用您的API密钥调用大模型  
✅ **错误处理**: 如果API失败，会使用模拟响应  

### 核心功能
1. **上传知识库**: 支持PDF、DOCX、TXT、MD文件
2. **智能问答**: 基于知识库内容回答问题
3. **题目生成**: 根据知识库生成相关题目
4. **知识库引用**: 答案中包含来源文件引用

## 🔍 故障排除

### 后端启动失败
- 检查Python版本: `python --version`
- 安装依赖: `pip install -r backend/requirements.txt`
- 检查端口占用: `netstat -ano | findstr :8000`

### 前端启动失败
- 检查Node.js版本: `node --version`
- 安装依赖: `npm install`
- 检查端口占用: `netstat -ano | findstr :3000`

### API调用失败
- 检查后端是否运行: `curl http://localhost:8000/health`
- 查看后端日志输出
- 确认API密钥正确

## 📊 预期结果

### 成功启动后
- 后端显示: "Application startup complete"
- 前端显示: "VITE ready"
- 浏览器能访问: http://localhost:3001

### 功能测试
- 上传文件到知识库
- 在聊天界面提问
- 生成基于知识库的题目
- 查看答案中的知识库引用

## 🆘 获取帮助

如果遇到问题，请：
1. 查看控制台错误信息
2. 运行测试脚本: `python test_api.py`
3. 检查API文档: http://localhost:8000/docs
4. 提供详细的错误日志

## 🎯 下一步

1. 确保您的大模型API服务正在运行
2. 修改 `API_BASE_URL` 为您的实际API地址
3. 测试上传文件和聊天功能
4. 根据需要调整API调用参数 