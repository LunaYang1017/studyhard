#!/usr/bin/env python3
import requests
import json

def test_cors():
    """测试CORS配置"""
    base_url = "http://localhost:8000"
    
    # 测试CORS端点
    print("测试CORS端点...")
    try:
        response = requests.get(f"{base_url}/test-cors", 
                              headers={"Origin": "http://localhost:3005"})
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"CORS测试失败: {e}")
    
    # 测试知识库内容端点
    print("\n测试知识库内容端点...")
    try:
        response = requests.get(f"{base_url}/knowledge-base-content",
                              headers={"Origin": "http://localhost:3005"})
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text[:200]}...")
    except Exception as e:
        print(f"知识库内容测试失败: {e}")

if __name__ == "__main__":
    test_cors() 