from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
import json
import asyncio
from datetime import datetime
import aiofiles
import requests
import PyPDF2
from docx import Document
import io
import re
import uuid
from pathlib import Path

# 创建FastAPI应用
app = FastAPI(
    title="考试复习助手API",
    description="基于大模型的考试复习助手后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "http://localhost:3005",
        "http://localhost:3006",
        "http://localhost:3007",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "*"  # 开发环境允许所有来源
    ],
    allow_credentials=False,  # 改为False，因为allow_origins=["*"]时不能为True
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 明确指定允许的方法
    allow_headers=["*"],  # 允许所有请求头
    expose_headers=["*"],  # 暴露所有响应头
)

# 数据存储目录
DATA_DIR = Path("data")
USERS_DIR = DATA_DIR / "users"
DATA_DIR.mkdir(exist_ok=True)
USERS_DIR.mkdir(exist_ok=True)

# 用户会话管理
user_sessions = {}

def get_user_session(session_id: str):
    """获取或创建用户会话"""
    if session_id not in user_sessions:
        user_sessions[session_id] = {
            "knowledge": [],
            "questions": [],
            "file_id_counter": 0
        }
    return user_sessions[session_id]

def save_user_data(session_id: str):
    """保存用户数据到文件"""
    user_data = user_sessions.get(session_id, {})
    user_file = USERS_DIR / f"{session_id}.json"
    try:
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存用户数据失败: {e}")

def load_user_data(session_id: str):
    """从文件加载用户数据"""
    user_file = USERS_DIR / f"{session_id}.json"
    if user_file.exists():
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                user_sessions[session_id] = data
                return data
        except Exception as e:
            print(f"加载用户数据失败: {e}")
    return None

def generate_session_id():
    """生成唯一的会话ID"""
    return str(uuid.uuid4())

# 测试CORS的端点
@app.get("/test-cors")
async def test_cors():
    return {"message": "CORS is working!", "timestamp": datetime.now().isoformat()}

# 添加OPTIONS预检请求处理
@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return {"message": "OPTIONS request handled"}

# 数据模型
class ChatMessage(BaseModel):
    message: str
    session_id: str
    knowledge_base_1: List[Dict[str, Any]] = []
    knowledge_base_2: List[Dict[str, Any]] = []
    options: Optional[Dict[str, Any]] = {}

class QuestionRequest(BaseModel):
    topic: str
    session_id: str
    difficulty: str = "medium"
    count: int = 5
    question_type: str = "multiple_choice"
    knowledge_base_1: List[Dict[str, Any]] = []
    knowledge_base_2: List[Dict[str, Any]] = []

class FileInfo(BaseModel):
    id: str
    name: str
    type: str
    session_id: str

class SessionRequest(BaseModel):
    session_id: Optional[str] = None

# 存储上传的文件信息
uploaded_files = {
    "knowledge": [],
    "questions": []
}

# 用于生成唯一ID的计数器
file_id_counter = 0

# 扫描uploads目录并重建文件信息
def scan_uploads_directory():
    """扫描uploads目录，重建文件信息"""
    global uploaded_files, file_id_counter
    
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        return
    
    print("正在扫描uploads目录...")
    
    # 重置计数器
    file_id_counter = 0
    
    # 清空现有文件信息
    uploaded_files = {
        "knowledge": [],
        "questions": []
    }
    
    # 扫描目录中的所有文件
    for filename in os.listdir(uploads_dir):
        file_path = os.path.join(uploads_dir, filename)
        if os.path.isfile(file_path):
            # 获取文件信息
            file_size = os.path.getsize(file_path)
            file_stat = os.stat(file_path)
            
            # 生成文件ID
            file_id_counter += 1
            file_id = f"file_{file_id_counter}_{int(file_stat.st_mtime)}"
            
            # 确定文件类型
            file_type = "knowledge"  # 默认为知识库类型
            
            # 根据文件名判断类型（可以根据需要调整规则）
            if any(keyword in filename.lower() for keyword in ['题目', '题', 'question', 'test', 'exam']):
                file_type = "questions"
            
            # 确定MIME类型
            mime_type = "application/octet-stream"
            if filename.lower().endswith('.pdf'):
                mime_type = "application/pdf"
            elif filename.lower().endswith('.docx'):
                mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            elif filename.lower().endswith('.txt'):
                mime_type = "text/plain"
            elif filename.lower().endswith('.md'):
                mime_type = "text/markdown"
            
            # 创建文件信息
            file_data = {
                "id": file_id,
                "name": filename,
                "size": file_size,
                "type": mime_type,
                "path": file_path,
                "upload_time": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
            }
            
            # 添加到对应的知识库
            uploaded_files[file_type].append(file_data)
            print(f"重建文件信息: {filename} -> {file_type}")
    
    print(f"扫描完成，知识库文件: {len(uploaded_files['knowledge'])} 个，题目文件: {len(uploaded_files['questions'])} 个")

# 在应用启动时扫描uploads目录
scan_uploads_directory()

# 您的API密钥配置
API_KEY = os.getenv("STEPFUN_API_KEY", "5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4")
BASE_URL = os.getenv("STEPFUN_BASE_URL", "https://api.stepfun.com/v1")
MODEL_NAME = os.getenv("STEPFUN_MODEL", "step-1-8k")

def latex_to_natural(text):
    # 替换 $$...$$、\[...\]、\(...\) 为自然语言
    text = re.sub(r'\$\$(.*?)\$\$', lambda m: f"【公式内容：{m.group(1).strip()}，请结合上下文理解】", text, flags=re.DOTALL)
    text = re.sub(r'\\\[(.*?)\\\]', lambda m: f"【公式内容：{m.group(1).strip()}，请结合上下文理解】", text, flags=re.DOTALL)
    text = re.sub(r'\\\((.*?)\\\)', lambda m: f"【公式内容：{m.group(1).strip()}，请结合上下文理解】", text, flags=re.DOTALL)
    return text

# 调用大模型API
async def call_large_model_api(message: str, knowledge_base_1: List, knowledge_base_2: List) -> Dict[str, Any]:
    """
    调用阶跃星辰大模型API的函数
    使用您提供的API密钥
    """
    try:
        # 题号正则（如2-2、2_2、2．2、2.2、2题2小题等）
        question_no_match = re.search(r'(\d+[\-_.．、]?[\d]+)', message)
        if question_no_match and knowledge_base_2:
            qno = question_no_match.group(1)
            # 在题库内容中查找题号
            for file in knowledge_base_2:
                content = file.get('content', '')
                # 常见题号格式匹配
                pattern = rf'(题目[\s\S]{{0,20}}{qno}[\s\S]{{0,2000}}?)(答案[\s\S]{{0,1000}}?)(解析[\s\S]{{0,1000}}?)?(---|$)'
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    question_part = match.group(1).strip()
                    answer_part = match.group(2).strip() if match.group(2) else ''
                    explain_part = match.group(3).strip() if match.group(3) else ''
                    result = f"【题目内容】\n{question_part}\n\n【答案】\n{answer_part}\n\n【解析】\n{explain_part}"
                    return {
                        "answer": result,
                        "references": [{"file": file.get('name', ''), "content": question_part[:200] + '...'}]
                    }
        
        # 检查是否是询问题库内题目的请求
        is_question_query = any(keyword in message.lower() for keyword in [
            '题目', '题', '答案', '解答', '解析', '这道题', '这个题', '第几题'
        ])
        
        # 构建知识库上下文
        knowledge_context = "\n".join([
            f"- {file.get('name', 'Unknown')}: {file.get('content', '')[:500]}..."
            for file in knowledge_base_1
        ])
        
        questions_context = "\n".join([
            f"- {file.get('name', 'Unknown')}: {file.get('content', '')[:500]}..."
            for file in knowledge_base_2
        ])
        
        # 根据请求类型构建不同的系统提示词
        if is_question_query and knowledge_base_2:
            # 用户询问题库内题目，优先从题库中查找
            system_prompt = f"""你是一个专业的考试复习助手，专门回答题库中的题目。

用户的知识库包含以下内容：

**复习资料：**
{knowledge_context or "暂无复习资料"}

**考试题目库：**
{questions_context or "暂无考试题目"}

用户正在询问题库中的题目，请：

1. **优先从考试题目库中查找相关题目**
2. **如果找到相关题目，提供完整的题目内容、答案和详细解析**
3. **如果题目库中没有相关内容，基于复习资料提供相关知识点的解答**
4. **在回答中明确标注题目来源（来自题库 或 基于知识点）**
5. **提供详细的解题思路和步骤**

回答格式：
- 题目内容（如果来自题库）
- 答案
- 详细解析
- 解题思路
- 知识库引用

请确保回答准确、详细，并标注知识库引用。"""

            user_message = f"""用户问题：{message}

请从我的题库中查找相关题目并提供详细解答。如果题库中没有相关内容，请基于复习资料提供相关知识点的解答。"""
        else:
            # 普通知识问答
            system_prompt = f"""你是一个专业的考试复习助手，擅长基于用户提供的知识库内容回答问题。

用户的知识库包含以下内容：

**复习资料：**
{knowledge_context or "暂无复习资料"}

**考试题目：**
{questions_context or "暂无考试题目"}

请基于以上知识库内容回答用户的问题，并在回答中标注知识库引用。如果知识库中没有相关信息，请明确说明。

回答要求：
1. 准确回答用户问题
2. 基于知识库内容
3. 标注知识库引用
4. 如果可能，生成相关的练习题
5. 拒绝黄赌毒、暴力恐怖主义等内容"""

            user_message = f"用户问题：{message}\n\n请基于我的知识库内容回答这个问题，并在回答中标注知识库引用。"
        
        print(f"正在调用API，URL: {BASE_URL}/chat/completions")
        print(f"API密钥: {API_KEY[:10]}...")
        print(f"模型: {MODEL_NAME}")
        
        # 调用阶跃星辰API
        completion = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ],
                "max_tokens": 2000,
                "temperature": 0.7
            },
            timeout=30
        )
        
        print(f"API响应状态码: {completion.status_code}")
        
        if completion.status_code != 200:
            print(f"API调用失败，状态码: {completion.status_code}")
            print(f"响应内容: {completion.text}")
            raise Exception(f"API调用失败，状态码: {completion.status_code}")
        
        # 提取回答
        response_data = completion.json()
        print(f"API响应数据: {response_data}")
        
        answer = response_data["choices"][0]["message"]["content"]
        
        # 提取引用（简单解析）
        references = []
        for file in knowledge_base_1 + knowledge_base_2:
            if file.get('name', '') in answer:
                references.append({
                    "file": file.get('name', ''),
                    "content": file.get('content', '')[:200] + "..."
                })
        
        # 将公式转换为自然语言
        answer = latex_to_natural(answer)
        
        # 确保references是字符串格式，避免前端显示[object Object]
        if references:
            # 将references格式化为字符串，添加到answer中
            references_text = "\n\n**知识库引用：**\n"
            for ref in references:
                references_text += f"- {ref['file']}: {ref['content']}\n"
            answer += references_text
            # 清空references数组，因为已经添加到answer中了
            references = []
        
        return {
            "answer": answer,
            "references": references
        }
        
    except Exception as e:
        print(f"API调用失败: {e}")
        print(f"错误类型: {type(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")
        # 如果API调用失败，返回错误信息而不是默认提示
        return {
            "answer": f"抱歉，AI服务调用失败: {str(e)}。请检查网络连接或稍后重试。",
            "references": []
        }

# 调用大模型API生成题目
async def call_large_model_for_questions(topic: str, difficulty: str, count: int, question_type: str, knowledge_base_1: List, knowledge_base_2: List) -> Dict[str, Any]:
    """
    调用阶跃星辰大模型API生成题目的函数
    优先从考试题目知识库中提取题目，或基于知识点生成同类型题目
    """
    try:
        # 构建知识库上下文
        knowledge_context = "\n".join([
            f"- {file.get('name', 'Unknown')}: {file.get('content', '')[:500]}..."
            for file in knowledge_base_1
        ])
        
        questions_context = "\n".join([
            f"- {file.get('name', 'Unknown')}: {file.get('content', '')[:500]}..."
            for file in knowledge_base_2
        ])
        
        # 构建系统提示词 - 优先从考试题目库提取题目
        system_prompt = f"""你是一个专业的考试题目助手，擅长从考试题目库中提取题目或基于知识点生成同类型题目。

用户的知识库包含以下内容：

**复习资料：**
{knowledge_context or "暂无复习资料"}

**考试题目库：**
{questions_context or "暂无考试题目"}

请按照以下优先级处理：

1. **优先从考试题目库提取**：如果考试题目库中有关于"{topic}"的题目，请直接提取并返回这些题目
2. **基于知识点生成同类型题目**：如果没有直接相关的题目，请基于复习资料中的知识点，参考考试题目库中的题目类型和风格，生成同类型的题目

题目要求：
1. 题目类型：{question_type}
2. 难度级别：{difficulty}
3. 数量：{count}道题目
4. 基于知识库内容
5. 包含详细答案和解释
6. 标注知识库引用
7. 拒绝黄赌毒、暴力恐怖主义等内容

请以JSON格式返回，格式如下：
{{
    "questions": [
        {{
            "question": "题目内容",
            "answer": "答案",
            "explanation": "详细解释",
            "difficulty": "{difficulty}",
            "type": "{question_type}",
            "references": ["引用文件1", "引用文件2"],
            "source": "extracted" 或 "generated"
        }}
    ],
    "total": {count},
    "source_type": "从题目库提取" 或 "基于知识点生成"
}}"""

        # 构建用户消息
        user_message = f"""请为"{topic}"生成{count}道{difficulty}难度的{question_type}题目。

要求：
1. 优先从考试题目库中提取相关题目
2. 如果没有直接相关题目，请基于复习资料中的知识点，参考题目库的题型风格生成同类型题目
3. 每道题都要标注来源（提取自题目库 或 基于知识点生成）
4. 包含详细答案和解释"""

        # 调用阶跃星辰API
        completion = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ],
                "max_tokens": 4000,
                "temperature": 0.7
            }
        )
        
        # 提取回答
        response_text = completion.json()["choices"][0]["message"]["content"]
        
        # 将公式转换为自然语言
        response_text = latex_to_natural(response_text)
        
        # 尝试解析JSON
        try:
            # 查找JSON部分
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
                return {
                    "questions": result.get("questions", []),
                    "total": len(result.get("questions", [])),
                    "source_type": result.get("source_type", "未知")
                }
        except:
            pass
        
        # 如果JSON解析失败，使用模拟响应
        print("JSON解析失败，使用模拟响应")
        return await mock_questions_response(topic, difficulty, count, question_type, knowledge_base_1, knowledge_base_2)
        
    except Exception as e:
        print(f"题目生成API调用失败: {e}")
        # 如果API调用失败，返回模拟响应
        return await mock_questions_response(topic, difficulty, count, question_type, knowledge_base_1, knowledge_base_2)

# 模拟API响应（备用方案）
async def mock_api_response(message: str, knowledge_base_1: List, knowledge_base_2: List) -> Dict[str, Any]:
    return {
        "answer": "抱歉，当前AI服务不可用，请稍后重试。",
        "references": []
    }

# 模拟题目生成响应（备用方案）
async def mock_questions_response(topic: str, difficulty: str, count: int, question_type: str, knowledge_base_1: List, knowledge_base_2: List) -> Dict[str, Any]:
    """模拟题目生成响应，当真实API不可用时使用"""
    await asyncio.sleep(1)
    
    # 基于知识库内容生成更真实的题目
    knowledge_files = [f.get('name', '') for f in knowledge_base_1]
    question_files = [f.get('name', '') for f in knowledge_base_2]
    
    # 检查是否有考试题目库
    if question_files:
        # 模拟从题目库提取题目
        source_type = "从题目库提取"
        questions = [
            {
                "question": f"从您的考试题目库中提取的关于{topic}的题目：请解释{topic}的核心概念。",
                "answer": f"{topic}的核心概念包括...",
                "explanation": f"这道题来自您的考试题目库，{topic}是一个重要的概念，涉及多个方面...",
                "difficulty": difficulty,
                "type": question_type,
                "references": question_files[:2],
                "source": "extracted"
            },
            {
                "question": f"题目库中的{topic}相关题目：{topic}在实际应用中的主要优势是什么？",
                "answer": f"主要优势包括...",
                "explanation": f"根据您的考试题目库，{topic}在实际应用中具有以下优势...",
                "difficulty": difficulty,
                "type": question_type,
                "references": question_files[:2],
                "source": "extracted"
            }
        ]
    else:
        # 基于知识点生成题目
        source_type = "基于知识点生成"
        questions = [
            {
                "question": f"基于您的复习资料，请解释{topic}的核心概念是什么？",
                "answer": f"{topic}的核心概念包括...",
                "explanation": f"根据您上传的复习资料，{topic}是一个重要的概念，涉及多个方面...",
                "difficulty": difficulty,
                "type": question_type,
                "references": knowledge_files[:2] if knowledge_files else [],
                "source": "generated"
            },
            {
                "question": f"在{topic}领域，最重要的技术或方法是什么？",
                "answer": f"最重要的技术包括...",
                "explanation": f"根据您的复习资料，{topic}领域有多种重要技术...",
                "difficulty": difficulty,
                "type": question_type,
                "references": knowledge_files[:2] if knowledge_files else [],
                "source": "generated"
            }
        ]
    
    # 如果题目数量不够，添加更多题目
    while len(questions) < count:
        if question_files:
            # 继续从题目库提取
            questions.append({
                "question": f"题目库中的{topic}题目{len(questions) + 1}：请分析{topic}的某个特定方面。",
                "answer": f"分析结果：...",
                "explanation": f"这道题来自您的考试题目库，分析了{topic}的特定方面...",
                "difficulty": difficulty,
                "type": question_type,
                "references": question_files[:2],
                "source": "extracted"
            })
        else:
            # 继续基于知识点生成
            questions.append({
                "question": f"基于复习资料生成的{topic}题目{len(questions) + 1}：如何评估{topic}的性能？",
                "answer": f"评估方法包括...",
                "explanation": f"根据您的复习资料，评估{topic}性能的方法有...",
                "difficulty": difficulty,
                "type": question_type,
                "references": knowledge_files[:2] if knowledge_files else [],
                "source": "generated"
            })
    
    return {
        "questions": questions[:count],
        "total": count,
        "source_type": source_type
    }

# 文件内容解析函数
async def extract_file_content(file_path: str, file_type: str) -> str:
    """提取文件内容"""
    try:
        if not os.path.exists(file_path):
            return f"文件不存在: {file_path}"
        
        if file_type == "application/pdf":
            # 提取PDF内容
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    content = ""
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        # 处理Unicode编码问题
                        if page_text:
                            try:
                                # 尝试修复编码问题
                                page_text = page_text.encode('utf-8', errors='ignore').decode('utf-8')
                                content += page_text + "\n"
                            except UnicodeError:
                                # 如果还有问题，跳过这一页
                                continue
                    return content.strip()
            except Exception as e:
                return f"PDF解析失败: {str(e)}"
                
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # 提取DOCX内容
            try:
                doc = Document(file_path)
                content = ""
                for paragraph in doc.paragraphs:
                    text = paragraph.text
                    # 处理Unicode编码问题
                    if text:
                        try:
                            text = text.encode('utf-8', errors='ignore').decode('utf-8')
                            content += text + "\n"
                        except UnicodeError:
                            continue
                return content.strip()
            except Exception as e:
                return f"DOCX解析失败: {str(e)}"
                
        elif file_type in ["text/plain", "text/markdown"]:
            # 提取文本文件内容
            try:
                async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = await file.read()
                    # 确保内容可以正确编码
                    content = content.encode('utf-8', errors='ignore').decode('utf-8')
                    return content.strip()
            except Exception as e:
                # 如果UTF-8失败，尝试其他编码
                try:
                    async with aiofiles.open(file_path, 'r', encoding='gbk', errors='ignore') as file:
                        content = await file.read()
                        content = content.encode('utf-8', errors='ignore').decode('utf-8')
                        return content.strip()
                except:
                    return f"文本文件解析失败: {str(e)}"
        else:
            # 对于其他类型的文件，尝试作为二进制文件读取
            try:
                with open(file_path, 'rb') as file:
                    binary_content = file.read()
                    # 尝试解码为UTF-8
                    try:
                        return binary_content.decode('utf-8', errors='ignore').strip()
                    except:
                        return f"无法解析文件内容: {os.path.basename(file_path)}"
            except Exception as e:
                return f"文件读取失败: {str(e)}"
                        
    except Exception as e:
        print(f"文件内容提取失败 {file_path}: {e}")
        return f"文件内容提取失败: {str(e)}"

# API路由

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "考试复习助手API服务正在运行", 
        "version": "1.0.0",
        "api_key_configured": bool(API_KEY),
        "api_base_url": BASE_URL
    }

@app.post("/create-session")
async def create_session():
    """创建新的用户会话"""
    session_id = generate_session_id()
    get_user_session(session_id)  # 初始化会话
    save_user_data(session_id)    # 保存到文件
    return {
        "success": True,
        "session_id": session_id,
        "message": "会话创建成功"
    }

@app.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """获取会话信息"""
    user_data = load_user_data(session_id)
    if user_data:
        return {
            "success": True,
            "session_id": session_id,
            "files_count": {
                "knowledge": len(user_data.get("knowledge", [])),
                "questions": len(user_data.get("questions", []))
            }
        }
    else:
        return {
            "success": False,
            "message": "会话不存在"
        }

@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    file_info: str = Form(...),
    session_id: str = Form(...)
):
    """上传文件到知识库"""
    try:
        file_info_data = json.loads(file_info)
        uploaded_file_list = []
        
        # 获取用户会话
        user_session = get_user_session(session_id)
        
        # 创建用户专属的上传目录
        user_uploads_dir = DATA_DIR / "uploads" / str(session_id)
        user_uploads_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            # 保存文件到用户专属目录
            file_path = user_uploads_dir / file.filename
            os.makedirs(user_uploads_dir, exist_ok=True)
            
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # 创建文件信息，确保ID唯一
            user_session["file_id_counter"] += 1
            
            file_data = {
                "id": f"file_{user_session['file_id_counter']}_{int(datetime.now().timestamp())}",
                "name": file.filename,
                "size": len(content),
                "type": file.content_type,
                "path": str(file_path),
                "upload_time": datetime.now().isoformat(),
                "session_id": session_id
            }
            
            # 根据类型存储到不同的知识库
            if file_info_data.get("type") == "knowledge":
                user_session["knowledge"].append(file_data)
            elif file_info_data.get("type") == "questions":
                user_session["questions"].append(file_data)
            
            uploaded_file_list.append(file_data)
        
        # 保存用户数据
        save_user_data(session_id)
        
        return {
            "success": True,
            "message": f"成功上传 {len(files)} 个文件",
            "files": uploaded_file_list
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@app.post("/chat")
async def chat_with_ai(request: ChatMessage):
    """与AI聊天"""
    try:
        # 调用大模型API
        response = await call_large_model_api(
            request.message,
            request.knowledge_base_1,
            request.knowledge_base_2
        )
        
        return {
            "success": True,
            "answer": response["answer"],
            "references": response.get("references", [])
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI服务调用失败: {str(e)}")

@app.post("/generate-questions")
async def generate_questions(request: QuestionRequest):
    """生成题目"""
    try:
        # 调用大模型API生成基于知识库的题目
        response = await call_large_model_for_questions(
            request.topic,
            request.difficulty,
            request.count,
            request.question_type,
            request.knowledge_base_1,
            request.knowledge_base_2
        )
        
        return {
            "success": True,
            "questions": response["questions"],
            "total": response["total"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成题目失败: {str(e)}")

@app.get("/knowledge-base/{session_id}")
async def get_knowledge_base(session_id: str):
    """获取知识库文件列表"""
    user_data = load_user_data(session_id)
    if not user_data:
        return {
            "success": True,
            "knowledge_base_1": [],
            "knowledge_base_2": []
        }
    
    return {
        "success": True,
        "knowledge_base_1": user_data.get("knowledge", []),
        "knowledge_base_2": user_data.get("questions", [])
    }

@app.get("/knowledge-base/{session_id}/{file_id}")
async def get_file_content(session_id: str, file_id: str):
    """获取文件内容"""
    try:
        user_data = load_user_data(session_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        # 查找文件
        all_files = user_data.get("knowledge", []) + user_data.get("questions", [])
        file_info = None
        
        for file in all_files:
            if file["id"] == file_id:
                file_info = file
                break
        
        if not file_info:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 使用新的文件内容提取函数
        content = await extract_file_content(file_info["path"], file_info["type"])
        
        # 更新文件信息中的内容
        file_info["content"] = content
        
        return {
            "success": True,
            "file": file_info,
            "content": content
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件内容失败: {str(e)}")

@app.get("/knowledge-base-content/{session_id}")
async def get_all_knowledge_base_content(session_id: str):
    """获取所有知识库文件的内容"""
    try:
        user_data = load_user_data(session_id)
        if not user_data:
            return {
                "success": True,
                "files": []
            }
        
        all_files = user_data.get("knowledge", []) + user_data.get("questions", [])
        files_with_content = []
        
        for file_info in all_files:
            # 使用新的文件内容提取函数
            content = await extract_file_content(file_info["path"], file_info["type"])
            
            file_with_content = file_info.copy()
            file_with_content["content"] = content
            files_with_content.append(file_with_content)
        
        return {
            "success": True,
            "files": files_with_content
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取知识库内容失败: {str(e)}")

@app.delete("/delete-file/{session_id}/{file_id}")
async def delete_file(session_id: str, file_id: str, knowledge_type: str = Query(..., description="知识库类型：knowledge 或 questions")):
    """删除文件"""
    try:
        user_data = load_user_data(session_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        # 查找文件
        file_list = user_data.get(knowledge_type, [])
        file_info = None
        file_index = -1
        
        for i, file in enumerate(file_list):
            if str(file["id"]) == str(file_id):  # 强制转为字符串比较
                file_info = file
                file_index = i
                break
        
        if not file_info:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 删除物理文件
        try:
            if os.path.exists(file_info["path"]):
                os.remove(file_info["path"])
        except Exception as e:
            print(f"删除物理文件失败: {e}")
        
        # 从内存中删除文件信息
        user_data[knowledge_type].pop(file_index)
        
        # 保存用户数据
        save_user_data(session_id)
        
        return {
            "success": True,
            "message": f"文件 {file_info['name']} 删除成功"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文件失败: {str(e)}")

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "files_count": {
            "knowledge": len(uploaded_files["knowledge"]),
            "questions": len(uploaded_files["questions"])
        },
        "api_key_configured": bool(API_KEY)
    }

@app.post("/rescan-files")
async def rescan_files():
    """重新扫描uploads目录，重建文件信息"""
    try:
        scan_uploads_directory()
        return {
            "success": True,
            "message": "文件扫描完成",
            "files_count": {
                "knowledge": len(uploaded_files["knowledge"]),
                "questions": len(uploaded_files["questions"])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"重新扫描文件失败: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 