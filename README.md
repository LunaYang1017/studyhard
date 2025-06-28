# 考试复习助手

一个基于大模型的智能考试复习网页应用，支持上传复习资料和考试题目，生成相似题目并提供基于知识库的解答。

## 功能特点

- 📚 **双知识库系统**：分别上传复习资料和考试题目
- 🤖 **智能题目生成**：基于知识库生成相似题型和知识点
- 💬 **对话式交互**：类似ChatGPT的对话界面
- 📖 **知识库引用**：解答中标注索引，可跳转到原知识库
- 📱 **响应式设计**：支持桌面和移动设备
- 🎨 **现代UI**：美观的用户界面

## 技术栈

- **前端框架**：React 18
- **构建工具**：Vite
- **样式框架**：Tailwind CSS
- **UI组件**：Lucide React Icons
- **文件上传**：React Dropzone
- **Markdown渲染**：React Markdown
- **HTTP客户端**：Axios

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

应用将在 `http://localhost:3000` 启动

### 3. 构建生产版本

```bash
npm run build
```

## 使用说明

### 上传资料

1. 点击"上传资料"标签页
2. 在左侧上传复习资料（知识库1）
3. 在右侧上传考试题目（知识库2）
4. 支持的文件格式：PDF、DOCX、TXT、MD

### 开始复习

1. 点击"开始复习"标签页
2. 在右侧聊天界面输入您的问题
3. 系统会基于您的知识库生成答案
4. 左侧可以查看知识库内容

### 示例问题

- "请生成一道关于机器学习的题目"
- "解释什么是深度学习"
- "提供解题思路"
- "生成模拟考试"

## API集成

当前使用模拟API进行演示。要集成真实的大模型API，请：

1. 在 `src/services/api.js` 中配置您的API端点
2. 在 `src/App.jsx` 中替换 `mockAPIResponse` 为真实的API调用
3. 确保API返回格式包含知识库引用信息

### API格式示例

```javascript
// 发送消息
const response = await sendMessageToAI(message, knowledgeBase1, knowledgeBase2)

// 预期响应格式
{
  "answer": "基于知识库的解答内容",
  "references": [
    {
      "file": "复习资料1.pdf",
      "page": 15,
      "content": "相关知识点内容"
    }
  ]
}
```

## 项目结构

```
src/
├── components/          # React组件
│   ├── FileUpload.jsx   # 文件上传组件
│   ├── ChatInterface.jsx # 聊天界面组件
│   └── KnowledgeBase.jsx # 知识库显示组件
├── services/            # API服务
│   └── api.js          # API调用函数
├── App.jsx             # 主应用组件
├── main.jsx            # 应用入口
└── index.css           # 全局样式
```

## 自定义配置

### 环境变量

创建 `.env` 文件：

```env
REACT_APP_API_BASE_URL=http://your-api-server.com
```

### 样式定制

在 `tailwind.config.js` 中修改主题配置：

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        50: '#eff6ff',
        500: '#3b82f6',
        600: '#2563eb',
        700: '#1d4ed8',
      }
    }
  },
}
```

## 开发说明

### 添加新功能

1. 在 `src/components/` 中创建新组件
2. 在 `src/services/api.js` 中添加新的API调用
3. 在 `src/App.jsx` 中集成新功能

### 调试

- 使用浏览器开发者工具查看控制台日志
- 检查网络请求和响应
- 验证文件上传和API调用

## 部署

### Vercel部署

1. 连接GitHub仓库到Vercel
2. 配置环境变量
3. 自动部署

### 其他平台

构建后，将 `dist` 目录部署到任何静态文件服务器。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

MIT License 