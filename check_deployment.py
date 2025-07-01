#!/usr/bin/env python3
"""
Railway部署检查脚本
用于验证部署是否成功
"""

import requests
import json
import sys
from urllib.parse import urljoin

def check_deployment(base_url):
    """检查部署状态"""
    print(f"🔍 检查部署状态: {base_url}")
    
    # 检查健康状态
    try:
        health_url = urljoin(base_url, "/health")
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            print("✅ 健康检查通过")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False
    
    # 检查API文档
    try:
        docs_url = urljoin(base_url, "/docs")
        response = requests.get(docs_url, timeout=10)
        if response.status_code == 200:
            print("✅ API文档可访问")
        else:
            print(f"❌ API文档不可访问: {response.status_code}")
    except Exception as e:
        print(f"❌ API文档检查异常: {e}")
    
    # 检查知识库端点
    try:
        kb_url = urljoin(base_url, "/knowledge-base")
        response = requests.get(kb_url, timeout=10)
        if response.status_code == 200:
            print("✅ 知识库端点正常")
        else:
            print(f"❌ 知识库端点异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 知识库检查异常: {e}")
    
    print("\n🎉 部署检查完成！")
    print(f"📝 API文档地址: {urljoin(base_url, '/docs')}")
    print(f"🔧 健康检查地址: {urljoin(base_url, '/health')}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python check_deployment.py <railway-url>")
        print("示例: python check_deployment.py https://your-app.railway.app")
        sys.exit(1)
    
    base_url = sys.argv[1]
    if not base_url.startswith(('http://', 'https://')):
        base_url = f"https://{base_url}"
    
    success = check_deployment(base_url)
    sys.exit(0 if success else 1) 