import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, File, X, Loader, RefreshCw } from 'lucide-react'
import { uploadToKnowledgeBase, deleteFileFromKnowledgeBase, getAllKnowledgeBaseFiles } from '../services/api'

const FileUpload = ({ title, description, onUpload, acceptedFiles, uploadedFiles, knowledgeType }) => {
  const [uploading, setUploading] = useState(false)
  const [refreshing, setRefreshing] = useState(false)

  // 刷新文件列表
  const refreshFileList = useCallback(async () => {
    try {
      setRefreshing(true)
      const response = await getAllKnowledgeBaseFiles()
      const fileList = knowledgeType === 'knowledge' 
        ? response.knowledge_base_1 || []
        : response.knowledge_base_2 || []
      
      // 更新前端状态
      onUpload(fileList)
    } catch (error) {
      console.error('获取文件列表失败:', error)
    } finally {
      setRefreshing(false)
    }
  }, [knowledgeType, onUpload])

  // 手动刷新文件列表
  const handleManualRefresh = async () => {
    await refreshFileList()
  }

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return
    
    setUploading(true)
    try {
      console.log('开始上传文件:', acceptedFiles.length, '个文件')
      
      // 调用后端API上传文件
      const filesWithInfo = acceptedFiles.map(file => ({
        id: (window.crypto && window.crypto.randomUUID) ? window.crypto.randomUUID() : `${Date.now()}_${Math.random()}`,
        name: file.name,
        size: file.size,
        type: file.type,
        file: file
      }))
      
      const result = await uploadToKnowledgeBase(filesWithInfo, knowledgeType)
      console.log('文件上传成功:', result)
      
      // 上传成功后，从后端获取最新文件列表
      await refreshFileList()
    } catch (error) {
      console.error('文件上传失败:', error)
      alert('文件上传失败，请重试')
    } finally {
      setUploading(false)
    }
  }, [knowledgeType, refreshFileList])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
      'text/markdown': ['.md']
    },
    disabled: uploading
  })

  const removeFile = async (fileId) => {
    try {
      // 调用后端API删除文件
      await deleteFileFromKnowledgeBase(fileId, knowledgeType)
      console.log('文件删除成功:', fileId)
      
      // 删除成功后，从后端获取最新文件列表
      await refreshFileList()
    } catch (error) {
      console.error('文件删除失败:', error)
      alert('文件删除失败，请重试')
    }
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <button 
          onClick={handleManualRefresh} 
          disabled={refreshing || uploading}
          className="flex items-center text-sm text-gray-500 hover:text-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          title="刷新文件列表"
        >
          <RefreshCw className={`h-4 w-4 mr-1 ${refreshing ? 'animate-spin' : ''}`} />
          刷新
        </button>
      </div>
      <p className="text-sm text-gray-600 mb-4">{description}</p>
      
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
          uploading 
            ? 'border-gray-300 bg-gray-50 cursor-not-allowed'
            : isDragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400'
        }`}
      >
        <input {...getInputProps()} />
        {uploading ? (
          <div>
            <Loader className="mx-auto h-12 w-12 text-primary-500 mb-4 animate-spin" />
            <p className="text-primary-600">正在上传文件...</p>
          </div>
        ) : (
          <>
            <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            {isDragActive ? (
              <p className="text-primary-600">将文件拖放到这里...</p>
            ) : (
              <div>
                <p className="text-gray-600 mb-2">拖放文件到这里，或点击选择文件</p>
                <p className="text-xs text-gray-500">
                  支持的文件格式: {acceptedFiles.join(', ')}
                </p>
              </div>
            )}
          </>
        )}
      </div>

      {uploadedFiles.length > 0 && (
        <div className="mt-6">
          <h4 className="text-sm font-medium text-gray-900 mb-3">已上传的文件：</h4>
          <div className="space-y-2">
            {uploadedFiles.map((file, index) => (
              <div
                key={`${file.id}_${index}`}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center">
                  <File className="h-4 w-4 text-gray-400 mr-2" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{file.name}</p>
                    <p className="text-xs text-gray-500">{formatFileSize(file.size)}</p>
                  </div>
                </div>
                <button
                  onClick={() => removeFile(file.id)}
                  className="text-gray-400 hover:text-red-500 transition-colors"
                  disabled={uploading}
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default FileUpload 