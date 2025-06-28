"""
配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置"""
    
    # 服务器配置
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    RELOAD = os.getenv("RELOAD", "true").lower() == "true"
    
    # 大模型API配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    CUSTOM_AI_API_KEY = os.getenv("CUSTOM_AI_API_KEY")
    CUSTOM_AI_API_URL = os.getenv("CUSTOM_AI_API_URL")
    
    # 文件上传配置
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    
    # 安全配置
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # 支持的文件类型
    SUPPORTED_FILE_TYPES = {
        "application/pdf": [".pdf"],
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
        "text/plain": [".txt"],
        "text/markdown": [".md"]
    }
    
    # CORS配置
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite默认端口
        "http://127.0.0.1:5173"
    ]
    
    @classmethod
    def validate(cls):
        """验证配置"""
        errors = []
        
        # 检查必要的配置
        if not cls.SECRET_KEY or cls.SECRET_KEY == "your-secret-key-change-this":
            errors.append("请设置SECRET_KEY")
        
        # 检查至少有一个AI API配置
        ai_apis = [
            cls.OPENAI_API_KEY,
            cls.CLAUDE_API_KEY,
            cls.CUSTOM_AI_API_KEY
        ]
        if not any(ai_apis):
            errors.append("请至少配置一个大模型API密钥")
        
        if errors:
            raise ValueError(f"配置错误: {'; '.join(errors)}")
        
        return True 