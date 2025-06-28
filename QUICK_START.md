# 快速启动指南

## 问题解决

### 1. 前端 PostCSS 配置问题
如果遇到 PostCSS 配置错误，请确保 `postcss.config.js` 使用 CommonJS 语法：

```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### 2. 后端启动问题
**重要：必须在 backend 目录下启动后端服务！**

#### 方法一：使用提供的脚本（推荐）
```bash
# Windows 批处理
start_backend.bat

# PowerShell
.\start_backend.ps1
```

#### 方法二：手动启动
```bash
# 1. 进入 backend 目录
cd backend

# 2. 启动服务
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 方法三：使用测试脚本
```bash
# 先测试配置
python test_backend.py
```

## 完整启动流程

### 1. 启动前端
```bash
npm run dev
```
前端将在 http://localhost:3000 或 http://localhost:3001 启动

### 2. 启动后端
```bash
# 使用脚本（推荐）
start_backend.bat

# 或手动
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
后端将在 http://localhost:8000 启动

### 3. 验证服务
- 前端：访问 http://localhost:3000 或 http://localhost:3001
- 后端：访问 http://localhost:8000/docs 查看 API 文档

## 常见问题

### Q: 为什么后端启动失败？
A: 确保在 backend 目录下启动，不要在根目录启动。

### Q: 前端端口被占用怎么办？
A: Vite 会自动切换到下一个可用端口（如 3001）。

### Q: 上传文件失败？
A: 确保后端服务正在运行，并检查浏览器控制台的网络请求。

### Q: PowerShell 不支持 && 命令？
A: 使用提供的脚本文件，或分步执行命令。

## 文件结构
```
nanckathon/
├── backend/           # 后端代码
│   ├── main.py       # 主服务文件
│   └── requirements.txt
├── src/              # 前端代码
├── start_backend.bat # Windows 启动脚本
├── start_backend.ps1 # PowerShell 启动脚本
└── test_backend.py   # 后端测试脚本
``` 