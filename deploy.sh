#!/bin/bash

# 考试复习助手一键部署脚本
# 支持多种部署方案

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  考试复习助手部署脚本${NC}"
    echo -e "${BLUE}================================${NC}"
}

# 检查依赖
check_dependencies() {
    print_message "检查系统依赖..."
    
    # 检查Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker未安装，请先安装Docker"
        exit 1
    fi
    
    # 检查Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose未安装，请先安装Docker Compose"
        exit 1
    fi
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js未安装，请先安装Node.js"
        exit 1
    fi
    
    # 检查npm
    if ! command -v npm &> /dev/null; then
        print_error "npm未安装，请先安装npm"
        exit 1
    fi
    
    print_message "所有依赖检查通过"
}

# 配置环境变量
setup_environment() {
    print_message "配置环境变量..."
    
    if [ ! -f .env ]; then
        if [ -f env.example ]; then
            cp env.example .env
            print_warning "已创建.env文件，请编辑配置"
        else
            print_error "未找到环境变量模板文件"
            exit 1
        fi
    else
        print_message ".env文件已存在"
    fi
    
    # 提示用户编辑配置
    print_warning "请编辑.env文件，设置正确的API密钥和域名配置"
    read -p "编辑完成后按回车继续..."
}

# 构建前端
build_frontend() {
    print_message "构建前端应用..."
    
    # 安装依赖
    npm ci
    
    # 构建
    npm run build
    
    print_message "前端构建完成"
}

# 构建Docker镜像
build_docker() {
    print_message "构建Docker镜像..."
    
    # 构建后端镜像
    docker build -t exam-review-backend ./backend
    
    # 构建前端镜像
    docker build -t exam-review-frontend .
    
    print_message "Docker镜像构建完成"
}

# 启动服务
start_services() {
    print_message "启动服务..."
    
    # 使用docker-compose启动
    docker-compose up -d
    
    print_message "服务启动完成"
}

# 检查服务状态
check_services() {
    print_message "检查服务状态..."
    
    # 等待服务启动
    sleep 10
    
    # 检查后端健康状态
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_message "✅ 后端服务正常"
    else
        print_error "❌ 后端服务异常"
        return 1
    fi
    
    # 检查前端
    if curl -f http://localhost > /dev/null 2>&1; then
        print_message "✅ 前端服务正常"
    else
        print_error "❌ 前端服务异常"
        return 1
    fi
    
    print_message "所有服务运行正常"
}

# 显示访问信息
show_access_info() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  部署完成！${NC}"
    echo -e "${BLUE}================================${NC}"
    echo -e "${GREEN}前端地址:${NC} http://localhost"
    echo -e "${GREEN}后端API:${NC} http://localhost:8000"
    echo -e "${GREEN}API文档:${NC} http://localhost:8000/docs"
    echo -e "${GREEN}健康检查:${NC} http://localhost:8000/health"
    echo -e "${BLUE}================================${NC}"
}

# 停止服务
stop_services() {
    print_message "停止服务..."
    docker-compose down
    print_message "服务已停止"
}

# 查看日志
view_logs() {
    print_message "查看服务日志..."
    docker-compose logs -f
}

# 清理资源
cleanup() {
    print_message "清理资源..."
    docker-compose down -v
    docker system prune -f
    print_message "清理完成"
}

# 主菜单
show_menu() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  考试复习助手部署菜单${NC}"
    echo -e "${BLUE}================================${NC}"
    echo "1. 完整部署（推荐）"
    echo "2. 仅构建前端"
    echo "3. 仅启动服务"
    echo "4. 停止服务"
    echo "5. 查看日志"
    echo "6. 清理资源"
    echo "7. 检查服务状态"
    echo "0. 退出"
    echo -e "${BLUE}================================${NC}"
}

# 完整部署流程
full_deploy() {
    print_header
    check_dependencies
    setup_environment
    build_frontend
    build_docker
    start_services
    check_services
    show_access_info
}

# 主函数
main() {
    case "$1" in
        "deploy")
            full_deploy
            ;;
        "build")
            build_frontend
            ;;
        "start")
            start_services
            ;;
        "stop")
            stop_services
            ;;
        "logs")
            view_logs
            ;;
        "cleanup")
            cleanup
            ;;
        "status")
            check_services
            ;;
        *)
            while true; do
                show_menu
                read -p "请选择操作 (0-7): " choice
                case $choice in
                    1)
                        full_deploy
                        break
                        ;;
                    2)
                        build_frontend
                        break
                        ;;
                    3)
                        start_services
                        break
                        ;;
                    4)
                        stop_services
                        break
                        ;;
                    5)
                        view_logs
                        break
                        ;;
                    6)
                        cleanup
                        break
                        ;;
                    7)
                        check_services
                        break
                        ;;
                    0)
                        print_message "退出部署脚本"
                        exit 0
                        ;;
                    *)
                        print_error "无效选择，请重新输入"
                        ;;
                esac
            done
            ;;
    esac
}

# 脚本入口
main "$@" 