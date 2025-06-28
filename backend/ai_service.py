"""
大模型API服务
这里提供了几种常见大模型API的集成示例
"""

import asyncio
import json
import requests
from typing import Dict, List, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    """大模型API服务基类"""
    
    def __init__(self):
        self.api_key = None
        self.base_url = None
    
    async def call_api(self, message: str, knowledge_base_1: List, knowledge_base_2: List) -> Dict[str, Any]:
        """调用大模型API"""
        raise NotImplementedError("子类必须实现此方法")

class OpenAIService(AIService):
    """OpenAI API服务"""
    
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    async def call_api(self, message: str, knowledge_base_1: List, knowledge_base_2: List) -> Dict[str, Any]:
        """调用OpenAI API"""
        if not self.api_key:
            raise ValueError("OpenAI API密钥未设置")
        
        # 构建知识库上下文
        context = self._build_context(knowledge_base_1, knowledge_base_2)
        
        # 构建提示词
        prompt = f"""
你是一个专业的考试复习助手。请基于以下知识库内容回答用户的问题：

知识库1（复习资料）：
{context['knowledge']}

知识库2（考试题目）：
{context['questions']}

用户问题：{message}

请提供详细的解答，并在回答中标注知识库引用。回答格式应该包含：
1. 直接回答用户问题
2. 详细解释
3. 知识库引用（格式：[文件名 (页码)](#引用ID)）

请用中文回答。
"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "你是一个专业的考试复习助手。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            
            return {
                "answer": answer,
                "references": self._extract_references(answer)
            }
        
        except Exception as e:
            raise Exception(f"OpenAI API调用失败: {str(e)}")
    
    def _build_context(self, knowledge_base_1: List, knowledge_base_2: List) -> Dict[str, str]:
        """构建知识库上下文"""
        knowledge_context = "\n".join([
            f"- {file.get('name', 'Unknown')}: {file.get('content', '')[:500]}..."
            for file in knowledge_base_1
        ])
        
        questions_context = "\n".join([
            f"- {file.get('name', 'Unknown')}: {file.get('content', '')[:500]}..."
            for file in knowledge_base_2
        ])
        
        return {
            "knowledge": knowledge_context or "暂无复习资料",
            "questions": questions_context or "暂无考试题目"
        }
    
    def _extract_references(self, answer: str) -> List[Dict[str, str]]:
        """从回答中提取引用"""
        references = []
        # 这里可以添加引用提取逻辑
        return references

class ClaudeService(AIService):
    """Claude API服务"""
    
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("CLAUDE_API_KEY")
        self.base_url = "https://api.anthropic.com/v1/messages"
    
    async def call_api(self, message: str, knowledge_base_1: List, knowledge_base_2: List) -> Dict[str, Any]:
        """调用Claude API"""
        if not self.api_key:
            raise ValueError("Claude API密钥未设置")
        
        # 构建知识库上下文
        context = self._build_context(knowledge_base_1, knowledge_base_2)
        
        # 构建提示词
        prompt = f"""
你是一个专业的考试复习助手。请基于以下知识库内容回答用户的问题：

知识库1（复习资料）：
{context['knowledge']}

知识库2（考试题目）：
{context['questions']}

用户问题：{message}

请提供详细的解答，并在回答中标注知识库引用。回答格式应该包含：
1. 直接回答用户问题
2. 详细解释
3. 知识库引用（格式：[文件名 (页码)](#引用ID)）

请用中文回答。
"""
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 2000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            answer = result["content"][0]["text"]
            
            return {
                "answer": answer,
                "references": self._extract_references(answer)
            }
        
        except Exception as e:
            raise Exception(f"Claude API调用失败: {str(e)}")
    
    def _build_context(self, knowledge_base_1: List, knowledge_base_2: List) -> Dict[str, str]:
        """构建知识库上下文"""
        knowledge_context = "\n".join([
            f"- {file.get('name', 'Unknown')}: {file.get('content', '')[:500]}..."
            for file in knowledge_base_1
        ])
        
        questions_context = "\n".join([
            f"- {file.get('name', 'Unknown')}: {file.get('content', '')[:500]}..."
            for file in knowledge_base_2
        ])
        
        return {
            "knowledge": knowledge_context or "暂无复习资料",
            "questions": questions_context or "暂无考试题目"
        }
    
    def _extract_references(self, answer: str) -> List[Dict[str, str]]:
        """从回答中提取引用"""
        references = []
        # 这里可以添加引用提取逻辑
        return references

class CustomAIService(AIService):
    """自定义大模型API服务"""
    
    def __init__(self, api_url: str, api_key: str = None):
        super().__init__()
        self.base_url = api_url
        self.api_key = api_key or os.getenv("CUSTOM_AI_API_KEY")
    
    async def call_api(self, message: str, knowledge_base_1: List, knowledge_base_2: List) -> Dict[str, Any]:
        """调用自定义大模型API"""
        # 构建请求数据
        request_data = {
            "message": message,
            "knowledge_base_1": knowledge_base_1,
            "knowledge_base_2": knowledge_base_2,
            "options": {
                "include_references": True,
                "max_length": 2000
            }
        }
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            response = requests.post(self.base_url, headers=headers, json=request_data)
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "answer": result.get("answer", ""),
                "references": result.get("references", [])
            }
        
        except Exception as e:
            raise Exception(f"自定义AI API调用失败: {str(e)}")

# 工厂函数
def create_ai_service(service_type: str = "openai", **kwargs) -> AIService:
    """创建AI服务实例"""
    if service_type == "openai":
        return OpenAIService()
    elif service_type == "claude":
        return ClaudeService()
    elif service_type == "custom":
        return CustomAIService(**kwargs)
    else:
        raise ValueError(f"不支持的AI服务类型: {service_type}")

# 使用示例
async def example_usage():
    """使用示例"""
    # 创建AI服务
    ai_service = create_ai_service("openai")  # 或 "claude", "custom"
    
    # 模拟知识库数据
    knowledge_base_1 = [
        {"name": "机器学习基础.pdf", "content": "机器学习是人工智能的一个分支..."}
    ]
    knowledge_base_2 = [
        {"name": "考试题目.docx", "content": "请解释什么是深度学习？"}
    ]
    
    # 调用API
    try:
        result = await ai_service.call_api(
            "请生成一道关于机器学习的题目",
            knowledge_base_1,
            knowledge_base_2
        )
        print("API调用成功:", result)
    except Exception as e:
        print("API调用失败:", str(e))

if __name__ == "__main__":
    asyncio.run(example_usage()) 