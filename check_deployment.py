#!/usr/bin/env python3
"""
部署检查脚本
用于验证考试复习助手的部署状态
"""

import requests
import json
import sys
import time
from urllib.parse import urljoin

def print_status(message, status="INFO"):
    """打印状态信息"""
    colors = {
        "INFO": "\033[94m",    # 蓝色
        "SUCCESS": "\033[92m", # 绿色
        "WARNING": "\033[93m", # 黄色
        "ERROR": "\033[91m",   # 红色
        "RESET": "\033[0m"     # 重置
    }
    
    status_icon = {
        "INFO": "ℹ️",
        "SUCCESS": "✅",
        "WARNING": "⚠️",
        "ERROR": "❌"
    }
    
    print(f"{colors[status]}{status_icon[status]} {message}{colors['RESET']}")

def check_url(url, timeout=10):
    """检查URL是否可访问"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200, response
    except requests.exceptions.RequestException as e:
        return False, str(e)

def check_backend_health(base_url):
    """检查后端健康状态"""
    health_url = urljoin(base_url, "/health")
    print_status(f"检查后端健康状态: {health_url}")
    
    success, response = check_url(health_url)
    if success:
        try:
            data = response.json()
            print_status(f"后端状态: {data.get('status', 'unknown')}", "SUCCESS")
            return True
        except json.JSONDecodeError:
            print_status("后端响应格式错误", "WARNING")
            return True
    else:
        print_status(f"后端健康检查失败: {response}", "ERROR")
        return False

def check_frontend(base_url):
    """检查前端状态"""
    print_status(f"检查前端状态: {base_url}")
    
    success, response = check_url(base_url)
    if success:
        print_status("前端访问正常", "SUCCESS")
        return True
    else:
        print_status(f"前端访问失败: {response}", "ERROR")
        return False

def check_api_endpoints(base_url):
    """检查API端点"""
    endpoints = [
        "/docs",
        "/knowledge-base",
        "/create-session"
    ]
    
    print_status("检查API端点...")
    
    for endpoint in endpoints:
        url = urljoin(base_url, endpoint)
        success, response = check_url(url)
        if success:
            print_status(f"✅ {endpoint} - 正常", "SUCCESS")
        else:
            print_status(f"❌ {endpoint} - 失败: {response}", "ERROR")

def test_file_upload(base_url):
    """测试文件上传功能"""
    print_status("测试文件上传功能...")
    
    # 创建测试会话
    session_url = urljoin(base_url, "/create-session")
    try:
        response = requests.post(session_url, timeout=10)
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data.get('session_id')
            print_status(f"创建会话成功: {session_id}", "SUCCESS")
            
            # 测试知识库获取
            kb_url = urljoin(base_url, f"/knowledge-base/{session_id}")
            kb_response = requests.get(kb_url, timeout=10)
            if kb_response.status_code == 200:
                print_status("知识库访问正常", "SUCCESS")
            else:
                print_status("知识库访问失败", "WARNING")
        else:
            print_status("创建会话失败", "ERROR")
    except Exception as e:
        print_status(f"测试文件上传时出错: {e}", "ERROR")

def check_cors(base_url):
    """检查CORS配置"""
    print_status("检查CORS配置...")
    
    try:
        # 发送预检请求
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options(urljoin(base_url, "/chat"), headers=headers, timeout=10)
        
        if response.status_code == 200:
            print_status("CORS配置正常", "SUCCESS")
            return True
        else:
            print_status(f"CORS配置异常: {response.status_code}", "WARNING")
            return False
    except Exception as e:
        print_status(f"CORS检查失败: {e}", "ERROR")
        return False

def main():
    """主函数"""
    print_status("🚀 考试复习助手部署检查", "INFO")
    print("=" * 50)
    
    # 获取检查URL
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = input("请输入您的应用URL (例如: http://localhost:8000 或 https://your-domain.com): ").strip()
    
    if not base_url:
        print_status("未提供URL，使用默认地址", "WARNING")
        base_url = "http://localhost:8000"
    
    # 确保URL格式正确
    if not base_url.startswith(('http://', 'https://')):
        base_url = f"http://{base_url}"
    
    print_status(f"开始检查: {base_url}", "INFO")
    print()
    
    # 执行检查
    checks = []
    
    # 检查后端健康状态
    backend_ok = check_backend_health(base_url)
    checks.append(("后端健康检查", backend_ok))
    print()
    
    # 检查前端（如果提供了前端URL）
    if "localhost" in base_url or "127.0.0.1" in base_url:
        frontend_url = base_url.replace(":8000", "").replace("8000", "3000")
        frontend_ok = check_frontend(frontend_url)
        checks.append(("前端检查", frontend_ok))
        print()
    
    # 检查API端点
    if backend_ok:
        check_api_endpoints(base_url)
        print()
        
        # 测试文件上传
        test_file_upload(base_url)
        print()
        
        # 检查CORS
        check_cors(base_url)
        print()
    
    # 总结
    print("=" * 50)
    print_status("检查结果总结:", "INFO")
    
    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    
    for name, ok in checks:
        status = "✅ 通过" if ok else "❌ 失败"
        print(f"  {name}: {status}")
    
    print()
    if passed == total:
        print_status(f"🎉 所有检查通过！({passed}/{total})", "SUCCESS")
        print_status("您的考试复习助手部署成功！", "SUCCESS")
    else:
        print_status(f"⚠️ 部分检查失败 ({passed}/{total})", "WARNING")
        print_status("请检查失败的项并修复问题", "WARNING")
    
    print()
    print_status("访问地址:", "INFO")
    print(f"  前端: {base_url.replace(':8000', '').replace('8000', '3000')}")
    print(f"  后端: {base_url}")
    print(f"  API文档: {urljoin(base_url, '/docs')}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_status("\n检查被用户中断", "WARNING")
    except Exception as e:
        print_status(f"检查过程中出现错误: {e}", "ERROR")
        sys.exit(1) 