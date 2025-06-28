#!/usr/bin/env python3
"""
考试复习助手启动脚本
同时启动前端和后端服务
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

def run_command(command, cwd=None, name="Command"):
    """运行命令并实时输出日志"""
    print(f"🚀 启动 {name}...")
    print(f"📁 工作目录: {cwd or os.getcwd()}")
    print(f"💻 执行命令: {command}")
    print("-" * 50)
    
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # 实时输出日志
        for line in process.stdout:
            print(f"[{name}] {line.rstrip()}")
        
        return process
    except Exception as e:
        print(f"❌ 启动 {name} 失败: {e}")
        return None

def check_port_available(port):
    """检查端口是否可用"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def main():
    print("🎓 考试复习助手启动器")
    print("=" * 50)
    
    # 检查当前目录
    current_dir = Path.cwd()
    print(f"📂 当前目录: {current_dir}")
    
    # 检查必要的文件和目录
    backend_dir = current_dir / "backend"
    frontend_dir = current_dir
    
    if not backend_dir.exists():
        print("❌ 后端目录不存在: backend/")
        return 1
    
    if not (frontend_dir / "package.json").exists():
        print("❌ 前端package.json不存在")
        return 1
    
    # 检查端口可用性
    backend_port = 8000
    frontend_port = 3000
    
    if not check_port_available(backend_port):
        print(f"⚠️  后端端口 {backend_port} 已被占用")
        backend_port = 8001
        print(f"🔄 使用备用端口: {backend_port}")
    
    if not check_port_available(frontend_port):
        print(f"⚠️  前端端口 {frontend_port} 已被占用")
        frontend_port = 3001
        print(f"🔄 使用备用端口: {frontend_port}")
    
    processes = []
    
    try:
        # 启动后端服务
        backend_cmd = f"python main.py"
        backend_process = run_command(backend_cmd, cwd=backend_dir, name="后端服务")
        if backend_process:
            processes.append(backend_process)
        
        # 等待后端启动
        print("⏳ 等待后端服务启动...")
        time.sleep(3)
        
        # 启动前端服务
        frontend_cmd = f"npm run dev -- --port {frontend_port}"
        frontend_process = run_command(frontend_cmd, cwd=frontend_dir, name="前端服务")
        if frontend_process:
            processes.append(frontend_process)
        
        print("\n" + "=" * 50)
        print("🎉 服务启动完成!")
        print(f"🌐 前端地址: http://localhost:{frontend_port}")
        print(f"🔧 后端地址: http://localhost:{backend_port}")
        print("📖 API文档: http://localhost:8000/docs")
        print("=" * 50)
        print("💡 提示:")
        print("   - 按 Ctrl+C 停止所有服务")
        print("   - 前端会自动打开浏览器")
        print("   - 后端API密钥已配置")
        print("=" * 50)
        
        # 等待用户中断
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 收到停止信号，正在关闭服务...")
    
    except Exception as e:
        print(f"❌ 启动过程中出现错误: {e}")
        return 1
    
    finally:
        # 清理进程
        for process in processes:
            if process and process.poll() is None:
                print(f"🛑 停止进程: {process.pid}")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        
        print("✅ 所有服务已停止")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 