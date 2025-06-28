#!/usr/bin/env python3
"""
测试后端配置的脚本
"""
import sys
import os

def test_imports():
    """测试必要的模块是否能正常导入"""
    try:
        print("测试导入 FastAPI...")
        from fastapi import FastAPI
        print("✓ FastAPI 导入成功")
        
        print("测试导入 uvicorn...")
        import uvicorn
        print("✓ uvicorn 导入成功")
        
        print("测试导入 requests...")
        import requests
        print("✓ requests 导入成功")
        
        print("测试导入 PyPDF2...")
        import PyPDF2
        print("✓ PyPDF2 导入成功")
        
        print("测试导入 docx...")
        from docx import Document
        print("✓ python-docx 导入成功")
        
        return True
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_backend_file():
    """测试后端文件是否存在"""
    backend_path = os.path.join(os.getcwd(), "backend", "main.py")
    if os.path.exists(backend_path):
        print(f"✓ 后端文件存在: {backend_path}")
        return True
    else:
        print(f"✗ 后端文件不存在: {backend_path}")
        return False

def main():
    print("=== 后端配置测试 ===")
    
    # 测试导入
    imports_ok = test_imports()
    
    # 测试文件
    file_ok = test_backend_file()
    
    print("\n=== 测试结果 ===")
    if imports_ok and file_ok:
        print("✓ 所有测试通过！后端应该可以正常启动")
        print("\n启动命令:")
        print("1. 进入 backend 目录: cd backend")
        print("2. 启动服务: python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        print("\n或者使用提供的脚本:")
        print("- Windows: start_backend.bat")
        print("- PowerShell: .\\start_backend.ps1")
    else:
        print("✗ 测试失败，请检查配置")
        if not imports_ok:
            print("请运行: pip install -r backend/requirements.txt")
        if not file_ok:
            print("请检查 backend/main.py 文件是否存在")

if __name__ == "__main__":
    main() 