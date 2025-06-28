import React, { useState, useEffect } from 'react'
import FileUpload from './components/FileUpload'
import ChatInterface from './components/ChatInterface'
import KnowledgeBase from './components/KnowledgeBase'
import { BookOpen, MessageSquare, Upload, RefreshCw } from 'lucide-react'
import { sendMessageToAI, generateQuestions, mockAPIResponse, getAllKnowledgeBaseFiles, getKnowledgeBaseContent, createSession, getSessionId } from './services/api'

function App() {
  const [activeTab, setActiveTab] = useState('upload')
  const [knowledgeBase1, setKnowledgeBase1] = useState([])
  const [knowledgeBase2, setKnowledgeBase2] = useState([])
  const [chatHistory, setChatHistory] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const [sessionLoading, setSessionLoading] = useState(true)

  // 初始化会话
  useEffect(() => {
    const initSession = async () => {
      try {
        setSessionLoading(true)
        const id = await getSessionId()
        setSessionId(id)
        console.log('会话初始化成功:', id)
      } catch (error) {
        console.error('会话初始化失败:', error)
      } finally {
        setSessionLoading(false)
      }
    }
    
    initSession()
  }, [])

  // 获取知识库文件列表和内容
  const fetchKnowledgeBase = async () => {
    if (!sessionId) return
    
    try {
      setIsLoading(true)
      const response = await getAllKnowledgeBaseFiles()
      
      if (response.success) {
        // 获取文件列表
        const knowledgeFiles = response.knowledge_base_1 || []
        const questionFiles = response.knowledge_base_2 || []
        
        // 为每个文件获取实际内容
        const knowledgeWithContent = await Promise.all(
          knowledgeFiles.map(async (file) => {
            try {
              const contentResponse = await getKnowledgeBaseContent(file.id)
              return {
                ...file,
                content: contentResponse.content || '文件内容为空'
              }
            } catch (error) {
              console.error(`获取文件 ${file.name} 内容失败:`, error)
              return {
                ...file,
                content: '文件内容获取失败'
              }
            }
          })
        )
        
        const questionsWithContent = await Promise.all(
          questionFiles.map(async (file) => {
            try {
              const contentResponse = await getKnowledgeBaseContent(file.id)
              return {
                ...file,
                content: contentResponse.content || '文件内容为空'
              }
            } catch (error) {
              console.error(`获取文件 ${file.name} 内容失败:`, error)
              return {
                ...file,
                content: '文件内容获取失败'
              }
            }
          })
        )
        
        setKnowledgeBase1(knowledgeWithContent)
        setKnowledgeBase2(questionsWithContent)
      }
    } catch (error) {
      console.error('获取知识库失败:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // 组件加载时获取知识库
  useEffect(() => {
    if (sessionId) {
      fetchKnowledgeBase()
    }
  }, [sessionId])

  // 创建新会话
  const handleCreateNewSession = async () => {
    try {
      setSessionLoading(true)
      const newSessionId = await createSession()
      setSessionId(newSessionId)
      setKnowledgeBase1([])
      setKnowledgeBase2([])
      setChatHistory([])
      console.log('新会话创建成功:', newSessionId)
    } catch (error) {
      console.error('创建新会话失败:', error)
    } finally {
      setSessionLoading(false)
    }
  }

  const handleFileUpload = (files, type) => {
    // 直接刷新知识库
    fetchKnowledgeBase()
  }

  const handleChatMessage = async (message) => {
    try {
      // 检查是否是题目生成请求（明确要求生成新题目）
      const isQuestionGenerationRequest = (
        message.toLowerCase().includes('生成题目') || 
        message.toLowerCase().includes('出题') ||
        message.toLowerCase().includes('生成练习') ||
        message.toLowerCase().includes('创建题目') ||
        message.toLowerCase().includes('制作题目')
      ) && !(
        message.toLowerCase().includes('题目') && 
        (message.toLowerCase().includes('答案') || 
         message.toLowerCase().includes('解答') || 
         message.toLowerCase().includes('解析'))
      )
      
      let response
      
      if (isQuestionGenerationRequest) {
        // 题目生成请求
        try {
          const questionResponse = await generateQuestions(
            '考试复习', // 默认主题
            'medium',   // 默认难度
            3,          // 默认数量
            knowledgeBase1,
            knowledgeBase2
          )
          
          // 格式化题目显示
          const sourceType = questionResponse.source_type || '未知来源'
          const questions = questionResponse.questions || []
          
          let formattedResponse = `## 📝 为您生成的题目 (${sourceType})\n\n`
          
          questions.forEach((question, index) => {
            const source = question.source === 'extracted' ? '📚 来自题目库' : '🤖 基于知识点生成'
            formattedResponse += `### 题目 ${index + 1} ${source}\n\n`
            formattedResponse += `**题目：** ${question.question}\n\n`
            formattedResponse += `**答案：** ${question.answer}\n\n`
            formattedResponse += `**详细解释：** ${question.explanation}\n\n`
            
            if (question.references && question.references.length > 0) {
              formattedResponse += `**知识库引用：** ${question.references.join(', ')}\n\n`
            }
            
            formattedResponse += `---\n\n`
          })
          
          response = formattedResponse
        } catch (error) {
          console.log('题目生成API调用失败，使用模拟API:', error)
          response = await mockAPIResponse(message, knowledgeBase1, knowledgeBase2)
        }
      } else {
        // 普通聊天请求（包括询问题库内题目）
        try {
          console.log('调用真实API...')
          response = await sendMessageToAI(message, knowledgeBase1, knowledgeBase2)
          console.log('API调用成功，响应:', response)
        } catch (error) {
          console.log('真实API调用失败，使用模拟API:', error)
          response = await mockAPIResponse(message, knowledgeBase1, knowledgeBase2)
        }
      }
      
      setChatHistory(prev => [
        ...prev, 
        { role: 'user', content: message }, 
        { role: 'assistant', content: response }
      ])
    } catch (error) {
      console.error('发送消息失败:', error)
      setChatHistory(prev => [
        ...prev, 
        { role: 'user', content: message }, 
        { role: 'assistant', content: '抱歉，处理您的请求时出现了错误。请重试。' }
      ])
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 头部导航 */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <BookOpen className="h-8 w-8 text-primary-600" />
              <h1 className="ml-3 text-xl font-semibold text-gray-900">逢考必过</h1>
              {sessionId && (
                <div className="ml-4 flex items-center">
                  <span className="text-sm text-gray-500">会话ID:</span>
                  <span className="ml-1 text-sm font-mono text-gray-700 bg-gray-100 px-2 py-1 rounded">
                    {sessionId.substring(0, 8)}...
                  </span>
                </div>
              )}
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={handleCreateNewSession}
                disabled={sessionLoading}
                className="flex items-center px-3 py-2 rounded-md text-sm font-medium text-gray-500 hover:text-gray-700 disabled:opacity-50"
                title="创建新会话"
              >
                <RefreshCw className={`h-4 w-4 mr-2 ${sessionLoading ? 'animate-spin' : ''}`} />
                新会话
              </button>
              <nav className="flex space-x-8">
                <button
                  onClick={() => setActiveTab('upload')}
                  className={`flex items-center px-3 py-2 rounded-md text-sm font-medium ${
                    activeTab === 'upload'
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <Upload className="h-4 w-4 mr-2" />
                  上传资料
                </button>
                <button
                  onClick={() => setActiveTab('chat')}
                  className={`flex items-center px-3 py-2 rounded-md text-sm font-medium ${
                    activeTab === 'chat'
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <MessageSquare className="h-4 w-4 mr-2" />
                  开始复习
                </button>
              </nav>
            </div>
          </div>
        </div>
      </header>

      {/* 主要内容区域 */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'upload' ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <FileUpload
              title="上传复习资料"
              description="上传您的考试科目复习资料，作为知识库1"
              onUpload={(files) => handleFileUpload(files, 'knowledge')}
              acceptedFiles={['.pdf', '.docx', '.txt', '.md']}
              uploadedFiles={knowledgeBase1}
              knowledgeType="knowledge"
            />
            <FileUpload
              title="上传考试题目"
              description="上传考试题目，作为知识库2"
              onUpload={(files) => handleFileUpload(files, 'questions')}
              acceptedFiles={['.pdf', '.docx', '.txt', '.md']}
              uploadedFiles={knowledgeBase2}
              knowledgeType="questions"
            />
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* 左侧知识库 */}
            <div className="lg:col-span-1">
              <KnowledgeBase
                knowledgeBase1={knowledgeBase1}
                knowledgeBase2={knowledgeBase2}
                onRefresh={fetchKnowledgeBase}
                isLoading={isLoading}
              />
            </div>
            {/* 右侧聊天界面 */}
            <div className="lg:col-span-2">
              <ChatInterface
                chatHistory={chatHistory}
                onSendMessage={handleChatMessage}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App 