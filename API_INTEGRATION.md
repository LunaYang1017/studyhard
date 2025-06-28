# 大模型API集成指南

本文档说明如何将您的大模型API集成到考试复习助手中。

## 当前状态

应用目前使用模拟API进行演示。要集成真实的大模型API，请按照以下步骤操作：

## 1. 配置API端点

### 方法1：环境变量（推荐）

创建 `.env` 文件：

```env
VITE_API_BASE_URL=http://your-api-server.com
```

### 方法2：直接修改配置

编辑 `src/config/api.js`：

```javascript
export const API_CONFIG = {
  BASE_URL: 'http://your-api-server.com', // 替换为您的API地址
  // ... 其他配置
}
```

## 2. 修改API调用

### 替换模拟API

在 `src/App.jsx` 中，将：

```javascript
const response = await mockAPIResponse(message, knowledgeBase1, knowledgeBase2)
```

替换为：

```javascript
const response = await sendMessageToAI(message, knowledgeBase1, knowledgeBase2)
```

### 更新API服务

在 `src/services/api.js` 中，根据您的API格式修改请求：

```javascript
export const sendMessageToAI = async (message, knowledgeBase1, knowledgeBase2) => {
  try {
    const payload = {
      message,
      knowledge_base_1: knowledgeBase1.map(file => ({
        id: file.id,
        name: file.name,
        content: file.content // 需要从文件中提取内容
      })),
      knowledge_base_2: knowledgeBase2.map(file => ({
        id: file.id,
        name: file.name,
        content: file.content
      })),
      // 根据您的API添加其他参数
      options: {
        generate_questions: true,
        include_references: true,
        max_length: 1000
      }
    }

    const response = await api.post(`${API_BASE_URL}/chat`, payload)
    return response.data.answer // 根据您的API响应格式调整
  } catch (error) {
    console.error('发送消息失败:', error)
    throw new Error('无法连接到AI服务，请检查网络连接')
  }
}
```

## 3. 文件内容提取

### 当前实现

应用目前显示模拟文件内容。要显示真实文件内容，需要：

1. **PDF文件**：使用 `pdf.js` 或后端API提取文本
2. **DOCX文件**：使用 `mammoth.js` 或后端API提取文本
3. **TXT/MD文件**：直接读取文本内容

### 示例实现

```javascript
// 在 FileUpload 组件中添加文件内容提取
const extractFileContent = async (file) => {
  if (file.type === 'text/plain' || file.type === 'text/markdown') {
    const text = await file.text()
    return text
  }
  
  // 对于PDF和DOCX，需要特殊处理
  // 可以调用后端API或使用前端库
  return '文件内容提取中...'
}
```

## 4. 知识库引用格式

### 期望的引用格式

在AI回答中，知识库引用应该使用以下格式：

```markdown
**知识库引用：**
- [复习资料1.pdf (第15页)](#knowledge-1-15)
- [考试题目库.docx (第3题)](#questions-1-3)
```

### 实现引用跳转

在 `ChatInterface.jsx` 中，点击引用链接时：

```javascript
const handleReferenceClick = (reference) => {
  // 在左侧知识库中高亮显示相关内容
  // 可以滚动到对应位置
  console.log('跳转到引用:', reference)
}
```

## 5. API响应格式要求

### 基本响应格式

```json
{
  "answer": "基于知识库的详细解答内容，包含Markdown格式",
  "references": [
    {
      "file": "复习资料1.pdf",
      "page": 15,
      "section": "1.2 重要概念",
      "content": "引用的具体内容"
    }
  ],
  "questions_generated": [
    {
      "question": "生成的题目",
      "answer": "参考答案",
      "explanation": "详细解释",
      "references": [...]
    }
  ]
}
```

### 错误处理

```json
{
  "error": "错误信息",
  "code": "ERROR_CODE",
  "details": "详细错误信息"
}
```

## 6. 测试步骤

1. **启动应用**：`npm run dev`
2. **上传测试文件**：上传一些测试用的PDF或TXT文件
3. **发送测试消息**：在聊天界面输入测试问题
4. **检查响应**：验证AI回答和知识库引用是否正确
5. **测试引用跳转**：点击引用链接，检查是否正确跳转

## 7. 常见问题

### CORS错误

如果遇到跨域问题，需要在您的API服务器上配置CORS：

```javascript
// Express.js 示例
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}))
```

### 文件上传失败

检查文件大小限制和文件类型支持：

```javascript
// 在 FileUpload 组件中
const maxSize = 10 * 1024 * 1024 // 10MB
const acceptedTypes = ['application/pdf', 'text/plain', ...]
```

### API响应格式不匹配

确保您的API响应格式与前端期望的格式一致。如果不一致，需要在前端进行格式转换。

## 8. 性能优化

### 文件处理

- 大文件分块上传
- 文件内容缓存
- 异步文件内容提取

### API调用

- 请求去重
- 响应缓存
- 错误重试机制

## 9. 部署注意事项

### 环境变量

确保在生产环境中正确设置API地址：

```bash
# 生产环境
VITE_API_BASE_URL=https://your-production-api.com
```

### 安全考虑

- API密钥安全存储
- 请求频率限制
- 文件上传安全检查

## 10. 联系支持

如果您在集成过程中遇到问题，请：

1. 检查浏览器控制台的错误信息
2. 验证API端点是否可访问
3. 确认请求和响应格式是否正确
4. 查看网络请求的详细信息

---

完成以上步骤后，您的考试复习助手就可以与真实的大模型API进行交互了！ 