// API配置文件
// 请根据您提供的大模型API来修改这些配置

export const API_CONFIG = {
  // 基础URL - 请替换为您的大模型API地址
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  
  // API端点配置
  ENDPOINTS: {
    // 上传文件到知识库
    UPLOAD: '/upload',
    
    // 发送消息给大模型
    CHAT: '/chat',
    
    // 生成题目
    GENERATE_QUESTIONS: '/generate-questions',
    
    // 获取知识库内容
    KNOWLEDGE_BASE: '/knowledge-base',
    
    // 搜索知识库
    SEARCH: '/search'
  },
  
  // 请求超时时间（毫秒）
  TIMEOUT: 30000,
  
  // 支持的文件类型
  SUPPORTED_FILE_TYPES: {
    'application/pdf': ['.pdf'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    'text/plain': ['.txt'],
    'text/markdown': ['.md']
  },
  
  // 最大文件大小（字节）
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
}

// 大模型API请求格式示例
export const API_REQUEST_FORMATS = {
  // 发送消息格式
  CHAT_MESSAGE: {
    message: "用户输入的消息",
    knowledge_base_1: [
      {
        id: "file_id",
        name: "文件名.pdf",
        content: "文件内容或摘要"
      }
    ],
    knowledge_base_2: [
      {
        id: "file_id", 
        name: "题目文件.docx",
        content: "题目内容"
      }
    ],
    options: {
      generate_questions: true,
      include_references: true,
      max_length: 1000
    }
  },
  
  // 生成题目格式
  GENERATE_QUESTIONS: {
    topic: "机器学习",
    difficulty: "medium", // easy, medium, hard
    count: 5,
    question_type: "multiple_choice", // multiple_choice, essay, short_answer
    knowledge_base_1: [],
    knowledge_base_2: []
  }
}

// 大模型API响应格式示例
export const API_RESPONSE_FORMATS = {
  // 聊天响应格式
  CHAT_RESPONSE: {
    answer: "基于知识库的详细解答",
    questions_generated: [
      {
        question: "题目内容",
        answer: "参考答案",
        explanation: "详细解释",
        references: [
          {
            file: "复习资料1.pdf",
            page: 15,
            section: "1.2 重要概念",
            content: "相关知识点内容"
          }
        ]
      }
    ],
    references: [
      {
        file: "复习资料1.pdf",
        page: 15,
        section: "1.2 重要概念",
        content: "引用的具体内容"
      }
    ]
  },
  
  // 错误响应格式
  ERROR_RESPONSE: {
    error: "错误信息",
    code: "ERROR_CODE",
    details: "详细错误信息"
  }
}

// 如何集成您的大模型API
export const INTEGRATION_GUIDE = {
  steps: [
    "1. 修改 BASE_URL 为您的API服务器地址",
    "2. 根据您的API调整 ENDPOINTS 配置",
    "3. 修改 src/services/api.js 中的请求格式",
    "4. 确保响应格式包含知识库引用信息",
    "5. 测试文件上传和消息发送功能"
  ],
  
  // 常见API参数说明
  common_parameters: {
    "message": "用户输入的消息",
    "knowledge_base_1": "复习资料知识库",
    "knowledge_base_2": "考试题目知识库", 
    "topic": "题目主题",
    "difficulty": "题目难度",
    "count": "生成题目数量",
    "include_references": "是否包含知识库引用"
  }
} 