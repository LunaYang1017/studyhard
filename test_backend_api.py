#!/usr/bin/env python3
"""
测试后端API脚本
"""

import requests
import json
import time

# 后端API配置
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查通过: {data}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_chat_api():
    """测试聊天API"""
    print("🔍 测试聊天API...")
    try:
        payload = {
            "message": "你好，请简单介绍一下你自己",
            "knowledge_base_1": [],
            "knowledge_base_2": []
        }
        
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 聊天API正常")
            print(f"回答内容: {data.get('answer', '')[:200]}...")
            return True
        else:
            print(f"❌ 聊天API失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 聊天API异常: {e}")
        return False

def test_knowledge_base_api():
    """测试知识库API"""
    print("🔍 测试知识库API...")
    try:
        response = requests.get(f"{API_BASE_URL}/knowledge-base", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 知识库API正常")
            print(f"知识库1文件数: {len(data.get('knowledge_base_1', []))}")
            print(f"知识库2文件数: {len(data.get('knowledge_base_2', []))}")
            return True
        else:
            print(f"❌ 知识库API失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 知识库API异常: {e}")
        return False

def test_backend_api():
    """测试后端API调用"""
    base_url = "http://localhost:8000"
    
    # 测试健康检查
    print("1. 测试健康检查...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"健康检查失败: {e}")
        return
    
    # 测试CORS
    print("\n2. 测试CORS...")
    try:
        response = requests.get(f"{base_url}/test-cors")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"CORS测试失败: {e}")
    
    # 测试聊天API
    print("\n3. 测试聊天API...")
    try:
        payload = {
            "message": "你好，请介绍一下自己",
            "knowledge_base_1": [],
            "knowledge_base_2": []
        }
        response = requests.post(f"{base_url}/chat", json=payload)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"聊天API测试失败: {e}")
    
    # 测试知识库API
    print("\n4. 测试知识库API...")
    try:
        response = requests.get(f"{base_url}/knowledge-base")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"知识库API测试失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始API测试")
    print("=" * 50)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(3)
    
    tests = [
        test_health_check,
        test_knowledge_base_api,
        test_chat_api
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
        print("-" * 30)
    
    print("=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！API工作正常")
    else:
        print("⚠️  部分测试失败，请检查服务状态")
    
    print("=" * 50)

if __name__ == "__main__":
    test_backend_api() 