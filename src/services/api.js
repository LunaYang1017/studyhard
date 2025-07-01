import axios from 'axios'

// 配置axios默认设置
const api = axios.create({
  timeout: 60000, // 60秒超时
  headers: {
    'Content-Type': 'application/json',
  },
})

// 后端API地址 - 优先使用环境变量
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// 会话管理
let currentSessionId = localStorage.getItem('session_id')

// 创建新会话
export const createSession = async () => {
  try {
    const response = await api.post(`${API_BASE_URL}/create-session`)
    if (response.data.success) {
      currentSessionId = response.data.session_id
      localStorage.setItem('session_id', currentSessionId)
      return currentSessionId
    }
    throw new Error('创建会话失败')
  } catch (error) {
    console.error('创建会话失败:', error)
    throw new Error('无法创建会话')
  }
}

// 获取当前会话ID，如果不存在则创建新会话
export const getSessionId = async () => {
  if (!currentSessionId) {
    await createSession()
  }
  return currentSessionId
}

// 发送消息给大模型并获取回复
export const sendMessageToAI = async (message, knowledgeBase1, knowledgeBase2) => {
  try {
    console.log('开始调用sendMessageToAI...')
    console.log('API地址:', API_BASE_URL)
    console.log('消息:', message)
    console.log('知识库1文件数:', knowledgeBase1.length)
    console.log('知识库2文件数:', knowledgeBase2.length)
    
    const sessionId = await getSessionId()
    
    // 首先获取知识库内容
    console.log('获取知识库内容...')
    let knowledgeFiles = []
    let questionFiles = []
    
    try {
      const knowledgeResponse = await api.get(`${API_BASE_URL}/knowledge-base-content/${sessionId}`)
      console.log('知识库响应:', knowledgeResponse.data)
      const allFiles = knowledgeResponse.data.files || []
      
      // 根据文件类型分类
      knowledgeFiles = allFiles.filter(file => 
        knowledgeBase1.some(kb => kb.id === file.id)
      )
      questionFiles = allFiles.filter(file => 
        knowledgeBase2.some(kb => kb.id === file.id)
      )
      
      console.log('过滤后的知识库文件:', knowledgeFiles.length)
      console.log('过滤后的题目文件:', questionFiles.length)
    } catch (knowledgeError) {
      console.error('获取知识库内容失败:', knowledgeError)
      // 如果获取知识库内容失败，使用原始数据
      knowledgeFiles = knowledgeBase1
      questionFiles = knowledgeBase2
    }
    
    // 获取apiKey
    const apiKey = localStorage.getItem('api_key') || ''
    
    // 调用聊天接口
    const payload = {
      message,
      session_id: sessionId,
      knowledge_base_1: knowledgeFiles,
      knowledge_base_2: questionFiles
    }
    // 只有apiKey有值且非空字符串时才传递
    if (apiKey && apiKey.trim() !== '') {
      payload.api_key = apiKey
    }

    console.log('发送聊天请求...')
    console.log('请求载荷:', payload)
    
    const response = await api.post(`${API_BASE_URL}/chat`, payload)
    console.log('聊天API响应:', response.data)
    
    let answer = response.data.answer
    // 保证answer为字符串
    if (typeof answer !== 'string') {
      console.log('answer不是字符串，转换为JSON字符串')
      answer = JSON.stringify(answer, null, 2)
    }
    
    console.log('最终answer:', answer)
    return answer
  } catch (error) {
    console.error('发送消息失败:', error)
    console.error('错误详情:', error.response?.data || error.message)
    console.error('错误状态码:', error.response?.status)
    console.error('错误头信息:', error.response?.headers)
    
    if (error.code === 'ERR_NETWORK') {
      throw new Error('网络连接失败，请检查后端服务是否运行')
    } else if (error.response?.status === 0) {
      throw new Error('CORS错误，请检查后端CORS配置')
    } else {
      throw new Error(`API调用失败: ${error.response?.data?.detail || error.message}`)
    }
  }
}

// 上传文件到知识库
export const uploadToKnowledgeBase = async (files, knowledgeType) => {
  try {
    const sessionId = await getSessionId()
    const formData = new FormData()
    files.forEach((file, index) => {
      formData.append(`files`, file.file)
      formData.append(`file_info`, JSON.stringify({
        id: file.id,
        name: file.name,
        type: knowledgeType
      }))
    })
    formData.append(`session_id`, sessionId)

    const response = await api.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    return response.data
  } catch (error) {
    console.error('上传文件失败:', error)
    throw new Error('文件上传失败，请重试')
  }
}

// 生成题目
export const generateQuestions = async (topic, difficulty, count, knowledgeBase1, knowledgeBase2) => {
  try {
    const sessionId = await getSessionId()
    
    // 首先获取知识库内容
    const knowledgeResponse = await api.get(`${API_BASE_URL}/knowledge-base-content/${sessionId}`)
    const allFiles = knowledgeResponse.data.files || []
    
    // 根据文件类型分类
    const knowledgeFiles = allFiles.filter(file => 
      knowledgeBase1.some(kb => kb.id === file.id)
    )
    const questionFiles = allFiles.filter(file => 
      knowledgeBase2.some(kb => kb.id === file.id)
    )
    
    const payload = {
      topic,
      session_id: sessionId,
      difficulty,
      count,
      question_type: "multiple_choice",
      knowledge_base_1: knowledgeFiles,
      knowledge_base_2: questionFiles
    }

    const response = await api.post(`${API_BASE_URL}/generate-questions`, payload)
    return response.data
  } catch (error) {
    console.error('生成题目失败:', error)
    throw new Error('生成题目失败，请重试')
  }
}

// 获取知识库内容
export const getKnowledgeBaseContent = async (fileId) => {
  try {
    const sessionId = await getSessionId()
    const response = await api.get(`${API_BASE_URL}/knowledge-base/${sessionId}/${fileId}`)
    return response.data
  } catch (error) {
    console.error('获取知识库内容失败:', error)
    throw new Error('无法获取知识库内容')
  }
}

// 获取所有知识库文件列表
export const getAllKnowledgeBaseFiles = async () => {
  try {
    const sessionId = await getSessionId()
    const response = await api.get(`${API_BASE_URL}/knowledge-base/${sessionId}`)
    return response.data
  } catch (error) {
    console.error('获取知识库文件列表失败:', error)
    throw new Error('无法获取知识库文件列表')
  }
}

// 模拟API响应（用于开发测试）
export const mockAPIResponse = async (message, knowledgeBase1, knowledgeBase2) => {
  // 模拟网络延迟
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))

  const responses = [
    `基于您的知识库，我为您生成了以下题目：

**题目：**
请解释什么是机器学习？

**参考答案：**
机器学习是人工智能的一个分支，它使计算机能够在没有明确编程的情况下学习和改进。

**知识库引用：**
- [复习资料1.pdf (第15页)](#knowledge-1-15)
- [考试题目库.docx (第3题)](#questions-1-3)

您可以在左侧查看相关的知识库内容。`,

    `根据您的知识库，我为您提供以下解答：

**问题：** 什么是深度学习？

**答案：**
深度学习是机器学习的一个子集，使用多层神经网络来模拟人脑的学习过程。

**详细解释：**
1. 神经网络结构
2. 反向传播算法
3. 激活函数的作用

**知识库引用：**
- [人工智能基础.pdf (第8章)](#knowledge-2-8)
- [深度学习题目集.docx (第12题)](#questions-2-12)`,

    `基于您的复习资料，我为您生成了一道模拟题：

**题目类型：** 选择题

**题目：**
以下哪个不是机器学习的主要类型？
A. 监督学习
B. 无监督学习
C. 强化学习
D. 规则学习

**正确答案：** D

**解析：**
机器学习主要分为监督学习、无监督学习和强化学习三种类型。

**知识库引用：**
- [机器学习基础.pdf (第3页)](#knowledge-3-3)
- [历年真题.docx (第5题)](#questions-3-5)`
  ]

  return responses[Math.floor(Math.random() * responses.length)]
}

// 删除文件从知识库
export const deleteFileFromKnowledgeBase = async (fileId, knowledgeType) => {
  try {
    const sessionId = await getSessionId()
    const response = await api.delete(`${API_BASE_URL}/delete-file/${sessionId}/${fileId}?knowledge_type=${knowledgeType}`)
    return response.data
  } catch (error) {
    console.error('删除文件失败:', error)
    throw new Error('文件删除失败，请重试')
  }
}

// axios请求拦截器，自动加上api_key
api.interceptors.request.use(config => {
  const apiKey = localStorage.getItem('api_key')
  const model = localStorage.getItem('model')
  // 只在非 default 时传递
  if (model && model !== 'default') {
    if (apiKey) config.headers['x-api-key'] = apiKey
    config.headers['x-model'] = model
    if (config.data && typeof config.data === 'object') {
      config.data.api_key = apiKey
      config.data.model = model
    }
  }
  return config
})

export default api 