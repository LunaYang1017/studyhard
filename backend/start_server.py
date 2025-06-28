#!/usr/bin/env python3
"""
考试复习助手后端启动脚本
"""

import uvicorn
import os
import sys
from pathlib import Path

def main():
    """启动后端服务器"""
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 检查依赖
    try:
        import fastapi
        import uvicorn
        import aiofiles
        import requests
        import pydantic
    except ImportError as e:
        print(f"错误: 缺少依赖包 {e}")
        print("请运行: pip install -r requirements.txt")
        sys.exit(1)
    
    # 创建必要的目录
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # 配置服务器
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"🚀 启动考试复习助手后端服务器...")
    print(f"📍 地址: http://{host}:{port}")
    print(f"🔄 热重载: {'开启' if reload else '关闭'}")
    print(f"📁 上传目录: {os.path.abspath('uploads')}")
    print(f"📋 API文档: http://{host}:{port}/docs")
    print("=" * 50)
    
    # 启动服务器
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main() 