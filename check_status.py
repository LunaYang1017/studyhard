#!/usr/bin/env python3
"""
检查前后端服务状态的脚本
"""
import requests
import socket
import time

def check_port(host, port):
    """检查端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def check_backend_health():
    """检查后端健康状态"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"状态码: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"连接失败: {e}"

def main():
    print("=== 服务状态检查 ===")
    
    # 检查端口
    print("\n1. 端口检查:")
    backend_port = check_port("localhost", 8000)
    frontend_port_3000 = check_port("localhost", 3000)
    frontend_port_3001 = check_port("localhost", 3001)
    
    print(f"后端 (8000): {'✓ 运行中' if backend_port else '✗ 未运行'}")
    print(f"前端 (3000): {'✓ 运行中' if frontend_port_3000 else '✗ 未运行'}")
    print(f"前端 (3001): {'✓ 运行中' if frontend_port_3001 else '✗ 未运行'}")
    
    # 检查后端健康状态
    print("\n2. 后端健康检查:")
    if backend_port:
        healthy, result = check_backend_health()
        if healthy:
            print(f"✓ 后端健康: {result}")
        else:
            print(f"✗ 后端不健康: {result}")
    else:
        print("✗ 后端端口未开放，无法检查健康状态")
    
    # 总结
    print("\n=== 总结 ===")
    if backend_port and (frontend_port_3000 or frontend_port_3001):
        print("✓ 前后端服务都在运行！")
        frontend_url = "http://localhost:3001" if frontend_port_3001 else "http://localhost:3000"
        print(f"前端访问地址: {frontend_url}")
        print("后端API文档: http://localhost:8000/docs")
    else:
        print("✗ 服务未完全启动")
        if not backend_port:
            print("- 后端未启动，请运行: start_backend.bat")
        if not frontend_port_3000 and not frontend_port_3001:
            print("- 前端未启动，请运行: npm run dev")

if __name__ == "__main__":
    main() 