import React, { useState, useRef, useEffect } from 'react'
import { Send, User, Bot, Loader2 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

// LaTeX公式转换为自然数学语言的函数
const convertLatexToNaturalLanguage = (text) => {
  if (!text) return text
  
  let converted = text
  
  // 数学符号转换
  const mathSymbols = {
    '\\alpha': 'α', '\\beta': 'β', '\\gamma': 'γ', '\\delta': 'δ',
    '\\theta': 'θ', '\\lambda': 'λ', '\\mu': 'μ', '\\pi': 'π',
    '\\sigma': 'σ', '\\phi': 'φ', '\\omega': 'ω', '\\infty': '∞',
    '\\sum': '求和', '\\prod': '连乘', '\\int': '积分', '\\sqrt': '根号',
    '\\frac': '分数', '\\times': '×', '\\div': '÷', '\\pm': '±',
    '\\leq': '≤', '\\geq': '≥', '\\neq': '≠', '\\approx': '≈',
    '\\sin': '正弦', '\\cos': '余弦', '\\tan': '正切', '\\log': '对数',
    '\\ln': '自然对数', '\\exp': '指数函数', '\\lim': '极限'
  }
  
  // 替换数学符号
  Object.entries(mathSymbols).forEach(([latex, natural]) => {
    const regex = new RegExp(latex.replace(/\\/g, '\\\\'), 'g')
    converted = converted.replace(regex, natural)
  })
  
  // 处理分数格式 \frac{a}{b} -> a/b
  converted = converted.replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, '($1)/($2)')
  
  // 处理根号 \sqrt{a} -> √a
  converted = converted.replace(/\\sqrt\{([^}]+)\}/g, '√($1)')
  
  // 处理上下标
  converted = converted.replace(/([a-zA-Z0-9])\^([a-zA-Z0-9]+)/g, '$1的$2次方')
  converted = converted.replace(/([a-zA-Z0-9])_([a-zA-Z0-9]+)/g, '$1的下标$2')
  
  // 处理数学公式
  converted = converted.replace(/\$([^$]+)\$/g, '【数学公式：$1】')
  converted = converted.replace(/\\\(([^)]+)\\\)/g, '【数学公式：$1】')
  converted = converted.replace(/\$\$([^$]+)\$\$/g, '【数学公式：$1】')
  converted = converted.replace(/\\\[([^\]]+)\\\]/g, '【数学公式：$1】')
  
  return converted
}

const ChatInterface = ({ chatHistory, onSendMessage }) => {
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [chatHistory])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!message.trim() || isLoading) return

    setIsLoading(true)
    try {
      await onSendMessage(message)
      setMessage('')
    } catch (error) {
      console.error('发送消息失败:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const renderMessage = (msg, index) => {
    const isUser = msg.role === 'user'
    
    return (
      <div
        key={index}
        className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
      >
        <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
          <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
            isUser ? 'bg-primary-500 text-white ml-2' : 'bg-gray-200 text-gray-600 mr-2'
          }`}>
            {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
          </div>
          <div className={`rounded-lg px-4 py-2 ${
            isUser 
              ? 'bg-primary-500 text-white' 
              : 'bg-white border border-gray-200 text-gray-900'
          }`}>
            {isUser ? (
              <p className="text-sm">{msg.content}</p>
            ) : (
              <div className="prose prose-sm max-w-none">
                <ReactMarkdown
                  components={{
                    // 自定义链接样式，用于知识库引用
                    a: ({ node, ...props }) => (
                      <a
                        {...props}
                        className="text-blue-600 hover:text-blue-800 underline cursor-pointer"
                        onClick={(e) => {
                          e.preventDefault()
                          // 这里可以添加跳转到知识库的逻辑
                          console.log('点击了知识库引用:', props.href)
                        }}
                      />
                    ),
                    // 自定义代码块样式
                    code: ({ node, inline, ...props }) => (
                      inline ? (
                        <code {...props} className="bg-gray-100 px-1 py-0.5 rounded text-sm" />
                      ) : (
                        <pre className="bg-gray-100 p-3 rounded-lg overflow-x-auto">
                          <code {...props} className="text-sm" />
                        </pre>
                      )
                    ),
                    // 自定义段落，处理LaTeX公式
                    p: ({ node, children, ...props }) => {
                      const text = children?.toString() || ''
                      const convertedText = convertLatexToNaturalLanguage(text)
                      return <p {...props}>{convertedText}</p>
                    },
                    // 自定义文本节点，处理LaTeX公式
                    text: ({ node, children, ...props }) => {
                      const text = children?.toString() || ''
                      const convertedText = convertLatexToNaturalLanguage(text)
                      return <span {...props}>{convertedText}</span>
                    }
                  }}
                >
                  {convertLatexToNaturalLanguage(msg.content)}
                </ReactMarkdown>
              </div>
            )}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border h-[600px] flex flex-col">
      {/* 聊天头部 */}
      <div className="border-b px-6 py-4">
        <h3 className="text-lg font-semibold text-gray-900">逢考必过</h3>
        <p className="text-sm text-gray-600">基于您的知识库生成题目和解答</p>
      </div>

      {/* 消息列表 */}
      <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
        {chatHistory.length === 0 ? (
          <div className="text-center text-gray-500 mt-8">
            <Bot className="mx-auto h-12 w-12 text-gray-300 mb-4" />
            <p className="text-lg font-medium">开始您的复习之旅</p>
            <p className="text-sm">您可以：</p>
            <ul className="text-sm mt-2 space-y-1">
              <li>• 询问题库中题目的答案和解析</li>
              <li>• 询问某个知识点的详细解释</li>
              <li>• 要求生成新的练习题（说"生成题目"）</li>
              <li>• 请求提供解题思路</li>
              <li>• 要求生成模拟考试</li>
            </ul>
            <div className="mt-4 p-3 bg-blue-50 rounded-lg">
              <p className="text-xs text-blue-700">
                💡 <strong>提示：</strong> 如果您想询问题库中已有题目的答案，直接问"这道题的答案是什么"；如果想生成新的练习题，请说"生成题目"。
              </p>
            </div>
          </div>
        ) : (
          chatHistory.map(renderMessage)
        )}
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="flex max-w-[80%]">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 text-gray-600 mr-2 flex items-center justify-center">
                <Bot className="w-4 h-4" />
              </div>
              <div className="bg-white border border-gray-200 rounded-lg px-4 py-2">
                <div className="flex items-center space-x-2">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span className="text-sm text-gray-600">正在思考...</span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* 输入框 */}
      <div className="border-t px-6 py-4">
        <form onSubmit={handleSubmit} className="flex space-x-4">
          <div className="flex-1">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="输入您的问题或要求..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows="2"
              disabled={isLoading}
            />
          </div>
          <button
            type="submit"
            disabled={!message.trim() || isLoading}
            className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  )
}

export default ChatInterface 