# 安装指南

## 系统要求

- Windows 10 或更高版本
- 至少 4GB RAM
- 至少 1GB 可用磁盘空间

## 1. 安装 Node.js

### 方法1：官方安装包（推荐）

1. 访问 [Node.js 官网](https://nodejs.org/)
2. 下载 LTS 版本（推荐）
3. 运行安装程序，按照提示完成安装
4. 安装完成后重启命令提示符或PowerShell

### 方法2：使用包管理器

如果您有 Chocolatey：
```powershell
choco install nodejs
```

如果您有 Scoop：
```powershell
scoop install nodejs
```

### 验证安装

安装完成后，打开新的命令提示符或PowerShell，运行：

```bash
node --version
npm --version
```

应该显示版本号，例如：
```
v18.17.0
9.6.7
```

## 2. 安装项目依赖

在项目目录中运行：

```bash
npm install
```

## 3. 启动开发服务器

```bash
npm run dev
```

应用将在 `http://localhost:3000` 启动

## 4. 构建生产版本

```bash
npm run build
```

## 常见问题

### Node.js 未找到

如果提示 "node 不是内部或外部命令"：

1. 确保已正确安装 Node.js
2. 重启命令提示符或PowerShell
3. 检查环境变量 PATH 是否包含 Node.js 路径
4. 通常路径为：`C:\Program Files\nodejs\`

### npm 安装失败

如果 npm install 失败：

1. 检查网络连接
2. 尝试使用国内镜像：
   ```bash
   npm config set registry https://registry.npmmirror.com
   ```
3. 清除 npm 缓存：
   ```bash
   npm cache clean --force
   ```

### 端口被占用

如果 3000 端口被占用：

1. 查找占用端口的进程：
   ```bash
   netstat -ano | findstr :3000
   ```
2. 终止进程或修改端口

## 开发工具推荐

### 代码编辑器

- **Visual Studio Code**（推荐）
  - 下载地址：https://code.visualstudio.com/
  - 推荐插件：
    - ES7+ React/Redux/React-Native snippets
    - Tailwind CSS IntelliSense
    - Prettier - Code formatter

### 浏览器

- **Chrome** 或 **Edge**（推荐）
- 安装 React Developer Tools 扩展

## 下一步

安装完成后，请查看：

1. [README.md](./README.md) - 项目说明
2. [API_INTEGRATION.md](./API_INTEGRATION.md) - API集成指南

## 技术支持

如果遇到安装问题，请：

1. 检查 Node.js 版本是否为 16 或更高
2. 确保网络连接正常
3. 尝试以管理员身份运行命令提示符
4. 查看错误信息并搜索解决方案 