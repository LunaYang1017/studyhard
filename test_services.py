import requests
import time
import subprocess
import sys

def test_backend():
    """测试后端服务"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ 后端服务运行正常")
            print(f"   状态: {data.get('status')}")
            print(f"   文件数量: {data.get('files_count')}")
            print(f"   API密钥配置: {data.get('api_key_configured')}")
            return True
        else:
            print(f"❌ 后端服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 后端服务连接失败: {e}")
        return False

def test_session_creation():
    """测试会话创建"""
    try:
        response = requests.post("http://localhost:8000/create-session", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ 会话创建功能正常")
            print(f"   会话ID: {data.get('session_id')}")
            return data.get('session_id')
        else:
            print(f"❌ 会话创建失败: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 会话创建连接失败: {e}")
        return None

def test_frontend():
    """测试前端服务"""
    try:
        response = requests.get("http://localhost:3001", timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务运行正常 (端口3001)")
            return True
        else:
            print(f"❌ 前端服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        try:
            response = requests.get("http://localhost:3002", timeout=5)
            if response.status_code == 200:
                print("✅ 前端服务运行正常 (端口3002)")
                return True
            else:
                print(f"❌ 前端服务响应异常: {response.status_code}")
                return False
        except requests.exceptions.RequestException:
            try:
                response = requests.get("http://localhost:3003", timeout=5)
                if response.status_code == 200:
                    print("✅ 前端服务运行正常 (端口3003)")
                    return True
                else:
                    print(f"❌ 前端服务响应异常: {response.status_code}")
                    return False
            except requests.exceptions.RequestException:
                try:
                    response = requests.get("http://localhost:3004", timeout=5)
                    if response.status_code == 200:
                        print("✅ 前端服务运行正常 (端口3004)")
                        return True
                    else:
                        print(f"❌ 前端服务响应异常: {response.status_code}")
                        return False
                except requests.exceptions.RequestException as e:
                    print(f"❌ 前端服务连接失败: {e}")
                    return False

def main():
    print("🔍 检查服务状态...")
    print("=" * 50)
    
    # 测试后端
    backend_ok = test_backend()
    print()
    
    # 测试会话创建
    if backend_ok:
        session_id = test_session_creation()
        print()
    
    # 测试前端
    frontend_ok = test_frontend()
    print()
    
    print("=" * 50)
    if backend_ok and frontend_ok:
        print("🎉 所有服务运行正常！")
        print("📝 现在可以:")
        print("   1. 打开浏览器访问前端页面")
        print("   2. 创建新会话")
        print("   3. 上传文件到个人知识库")
        print("   4. 开始聊天和生成题目")
    else:
        print("⚠️  部分服务存在问题，请检查启动日志")

if __name__ == "__main__":
    main() 