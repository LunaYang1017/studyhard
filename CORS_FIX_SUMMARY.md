# CORS问题解决方案总结

## 问题描述
前端运行在3007端口时遇到CORS跨域问题，无法正常与后端（8000端口）通信。

## 已完成的修改

### 1. 前端配置修改
- **文件**: `vite.config.js`
- **修改**: 指定前端使用3001端口
```javascript
server: {
  port: 3001,
  host: true
}
```

### 2. 后端CORS配置优化
- **文件**: `backend/main.py`
- **修改**: 明确允许所有常用端口，包括3001
```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost:3001", 
    "http://localhost:3002",
    "http://localhost:3003",
    "http://localhost:3004",
    "http://localhost:3005",
    "http://localhost:3006",
    "http://localhost:3007",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "*"  # 开发环境允许所有来源
],
allow_credentials=False,  # 当allow_origins包含"*"时必须为False
```

### 3. 前端API调用优化
- **文件**: `src/services/api.js`
- **修改**: 改进了sendMessageToAI函数
  - 添加了知识库内容获取逻辑
  - 改进了错误处理
  - 添加了详细的调试日志

### 4. 创建测试工具
- **文件**: `test_frontend.html` - 前后端交互测试页面
- **文件**: `test_backend_api.py` - 后端API测试脚本
- **文件**: `start_all.ps1` - 一键启动脚本

## 解决方案要点

### CORS配置关键点
1. **allow_origins**: 明确列出所有允许的源，包括localhost和127.0.0.1
2. **allow_credentials**: 当allow_origins包含"*"时，必须设置为False
3. **allow_methods**: 明确指定允许的HTTP方法
4. **allow_headers**: 允许所有请求头

### 前端端口配置
- 使用固定的3001端口，避免端口冲突
- 在vite.config.js中明确指定端口

### API调用优化
- 添加了知识库内容预获取
- 改进了错误处理和调试信息
- 确保answer字段为字符串类型

## 测试方法

### 1. 使用测试页面
访问 `http://localhost:3001/test_frontend.html` 进行功能测试

### 2. 使用测试脚本
运行 `python test_backend_api.py` 测试后端API

### 3. 浏览器控制台
查看前端控制台的详细调试信息

## 启动服务

### 方法1: 使用启动脚本
```powershell
powershell -ExecutionPolicy Bypass -File start_all.ps1
```

### 方法2: 手动启动
```powershell
# 启动后端
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 启动前端
npm run dev
```

## 验证步骤

1. **检查后端服务**: 访问 `http://localhost:8000/health`
2. **检查前端服务**: 访问 `http://localhost:3001`
3. **测试CORS**: 使用测试页面验证跨域请求
4. **测试聊天功能**: 发送消息验证AI响应
5. **测试文件上传**: 上传文件验证功能

## 常见问题解决

### 1. CORS错误
- 确保后端CORS配置正确
- 检查前端端口是否在允许列表中
- 重启后端服务应用新配置

### 2. 端口占用
- 使用 `netstat -an | findstr :8000` 检查端口占用
- 使用 `taskkill /f /im python.exe` 结束进程

### 3. API调用失败
- 检查后端服务是否正常运行
- 查看浏览器控制台错误信息
- 使用测试页面验证API功能

## 下一步建议

1. **生产环境配置**: 在生产环境中限制CORS来源
2. **错误监控**: 添加更完善的错误监控和日志
3. **性能优化**: 优化文件上传和API调用性能
4. **安全加固**: 添加API认证和授权机制 