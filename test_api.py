#!/usr/bin/env python3
"""
测试API调用脚本
"""

import requests
import json
import os

# API配置
API_KEY = "5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4"
BASE_URL = "https://api.stepfun.com/v1"
MODEL_NAME = "step-1-8k"

def test_api_call():
    """测试API调用"""
    try:
        print("正在测试API调用...")
        print(f"API URL: {BASE_URL}/chat/completions")
        print(f"模型: {MODEL_NAME}")
        print(f"API密钥: {API_KEY[:10]}...")
        
        # 构建请求
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的考试复习助手。"
                },
                {
                    "role": "user",
                    "content": "你好，请简单介绍一下你自己。"
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        print("发送请求...")
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("API调用成功！")
            print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if "choices" in result and len(result["choices"]) > 0:
                answer = result["choices"][0]["message"]["content"]
                print(f"\nAI回答: {answer}")
            else:
                print("响应中没有找到choices字段")
        else:
            print(f"API调用失败，状态码: {response.status_code}")
            print(f"错误响应: {response.text}")
            
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")

if __name__ == "__main__":
    test_api_call() 