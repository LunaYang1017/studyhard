#!/usr/bin/env python3
"""
测试聊天API
"""

import requests
import json

def test_chat_api():
    """测试聊天API"""
    try:
        print("测试聊天API...")
        
        # 测试数据
        payload = {
            "message": "交流电机的原理与特性",
            "knowledge_base_1": [],
            "knowledge_base_2": []
        }
        
        # 发送请求
        response = requests.post(
            "http://localhost:8000/chat",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("API调用成功!")
            print(f"回答: {data.get('answer', '无回答')}")
        else:
            print(f"API调用失败: {response.text}")
            
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_chat_api() 