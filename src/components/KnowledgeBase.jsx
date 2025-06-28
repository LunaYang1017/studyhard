import React, { useState } from 'react'
import { File, BookOpen, Search, ChevronDown, ChevronRight, RefreshCw } from 'lucide-react'

const KnowledgeBase = ({ knowledgeBase1, knowledgeBase2, onRefresh, isLoading }) => {
  const [activeTab, setActiveTab] = useState('knowledge')
  const [expandedFiles, setExpandedFiles] = useState({})
  const [searchTerm, setSearchTerm] = useState('')

  const toggleFileExpansion = (fileId) => {
    setExpandedFiles(prev => ({
      ...prev,
      [fileId]: !prev[fileId]
    }))
  }

  const handleRefresh = () => {
    if (onRefresh) {
      onRefresh()
    }
  }

  const renderFileContent = (file, type) => {
    // 显示实际的文件内容
    const content = file.content || '文件内容为空'
    
    return (
      <div className="mt-3 p-3 bg-gray-50 rounded-lg text-sm">
        <pre className="whitespace-pre-wrap font-mono text-xs text-gray-700 max-h-60 overflow-y-auto">
          {content}
        </pre>
      </div>
    )
  }

  const renderFileList = (files, type) => {
    if (files.length === 0) {
      return (
        <div className="text-center py-8 text-gray-500">
          <File className="mx-auto h-8 w-8 text-gray-300 mb-2" />
          <p className="text-sm">
            {type === 'questions' ? '暂无题库文件' : '暂无复习资料'}
          </p>
        </div>
      )
    }

    return (
      <div className="space-y-2">
        {files.map((file, idx) => (
          <div key={`${file.id || file.name}_${idx}_${type}`} className="border rounded-lg">
            <button
              onClick={() => toggleFileExpansion(file.id)}
              className="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center">
                <File className="h-4 w-4 text-gray-400 mr-2" />
                <div>
                  <p className="text-sm font-medium text-gray-900">{file.name}</p>
                  <p className="text-xs text-gray-500">
                    {(file.size / 1024).toFixed(1)} KB
                  </p>
                </div>
              </div>
              {expandedFiles[file.id] ? (
                <ChevronDown className="h-4 w-4 text-gray-400" />
              ) : (
                <ChevronRight className="h-4 w-4 text-gray-400" />
              )}
            </button>
            {expandedFiles[file.id] && renderFileContent(file, type)}
          </div>
        ))}
      </div>
    )
  }

  const filteredKnowledgeBase1 = knowledgeBase1.filter(file =>
    file.name.toLowerCase().includes(searchTerm.toLowerCase())
  )
  const filteredKnowledgeBase2 = knowledgeBase2.filter(file =>
    file.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="bg-white rounded-lg shadow-sm border h-[600px] flex flex-col">
      {/* 头部 */}
      <div className="border-b px-4 py-3">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-lg font-semibold text-gray-900">知识库</h3>
          <button
            onClick={handleRefresh}
            disabled={isLoading}
            className="flex items-center px-2 py-1 text-sm text-gray-600 hover:text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <RefreshCw className={`h-4 w-4 mr-1 ${isLoading ? 'animate-spin' : ''}`} />
            刷新
          </button>
        </div>
        
        {/* 搜索框 */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="搜索文件..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* 标签页 */}
      <div className="border-b">
        <div className="flex">
          <button
            onClick={() => setActiveTab('knowledge')}
            className={`flex-1 px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'knowledge'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            <BookOpen className="h-4 w-4 inline mr-1" />
            复习资料 ({knowledgeBase1.length})
          </button>
          <button
            onClick={() => setActiveTab('questions')}
            className={`flex-1 px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'questions'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            <File className="h-4 w-4 inline mr-1" />
            考试题目 ({knowledgeBase2.length})
          </button>
        </div>
      </div>

      {/* 内容区域 */}
      <div className="flex-1 overflow-y-auto p-4 scrollbar-hide">
        {activeTab === 'knowledge' ? (
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-3">复习资料库</h4>
            {renderFileList(filteredKnowledgeBase1, 'knowledge')}
          </div>
        ) : (
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-3">考试题目库</h4>
            {renderFileList(filteredKnowledgeBase2, 'questions')}
          </div>
        )}
      </div>

      {/* 底部统计 */}
      <div className="border-t px-4 py-3 bg-gray-50">
        <div className="flex justify-between text-xs text-gray-500">
          <span>总文件数: {knowledgeBase1.length + knowledgeBase2.length}</span>
          <span>总大小: {((knowledgeBase1.reduce((sum, f) => sum + f.size, 0) + 
                           knowledgeBase2.reduce((sum, f) => sum + f.size, 0)) / 1024).toFixed(1)} KB</span>
        </div>
      </div>
    </div>
  )
}

export default KnowledgeBase 