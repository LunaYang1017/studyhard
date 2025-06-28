#!/usr/bin/env python3
"""
简单的API测试脚本
"""

import requests
import json

def test_chat_api():
    """测试聊天API"""
    print("🔍 测试聊天API...")
    
    url = "http://localhost:8000/chat"
    payload = {
        "message": "请解释什么是机器学习？",
        "knowledge_base_1": [
            {
                "id": "test1",
                "name": "机器学习基础.pdf",
                "content": "机器学习是人工智能的一个分支，它使计算机能够在没有明确编程的情况下学习和改进。"
            }
        ],
        "knowledge_base_2": []
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 聊天API调用成功!")
            print(f"回答: {data.get('answer', '')[:200]}...")
            return True
        else:
            print(f"❌ 聊天API调用失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 聊天API异常: {e}")
        return False

def test_generate_questions_api():
    """测试生成题目API"""
    print("\n🔍 测试生成题目API...")
    
    url = "http://localhost:8000/generate-questions"
    payload = {
        "topic": "机器学习",
        "difficulty": "medium",
        "count": 2,
        "question_type": "multiple_choice",
        "knowledge_base_1": [
            {
                "id": "test1",
                "name": "机器学习基础.pdf",
                "content": "机器学习是人工智能的一个分支，它使计算机能够在没有明确编程的情况下学习和改进。"
            }
        ],
        "knowledge_base_2": [
            {
                "id": "test2",
                "name": "考试题目库.docx",
                "content": "机器学习的主要类型包括监督学习、无监督学习和强化学习。"
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 生成题目API调用成功!")
            questions = data.get('questions', [])
            print(f"生成了 {len(questions)} 个题目:")
            for i, q in enumerate(questions, 1):
                print(f"  题目{i}: {q.get('question', '')[:50]}...")
            return True
        else:
            print(f"❌ 生成题目API调用失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 生成题目API异常: {e}")
        return False

def main():
    print("🚀 开始简单API测试")
    print("=" * 50)
    
    # 测试聊天API
    chat_success = test_chat_api()
    
    # 测试生成题目API
    questions_success = test_generate_questions_api()
    
    print("\n" + "=" * 50)
    print("📊 测试结果:")
    print(f"聊天API: {'✅ 成功' if chat_success else '❌ 失败'}")
    print(f"生成题目API: {'✅ 成功' if questions_success else '❌ 失败'}")
    
    if chat_success and questions_success:
        print("\n🎉 所有API测试通过！系统可以正常使用")
    else:
        print("\n⚠️  部分API测试失败，请检查后端服务")

if __name__ == "__main__":
    main() 