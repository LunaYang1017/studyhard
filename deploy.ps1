# 考试复习助手Windows部署脚本
# 支持PowerShell环境

param(
    [Parameter(Position=0)]
    [string]$Action = "menu"
)

# 颜色定义
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"
$White = "White"

# 打印带颜色的消息
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

function Write-Header {
    param([string]$Message)
    Write-Host "=================================" -ForegroundColor $Blue
    Write-Host "  $Message" -ForegroundColor $Blue
    Write-Host "=================================" -ForegroundColor $Blue
}

# 检查依赖
function Test-Dependencies {
    Write-Info "检查系统依赖..."
    
    # 检查Docker
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Error "Docker未安装，请先安装Docker Desktop"
        exit 1
    }
    
    # 检查Docker Compose
    if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
        Write-Error "Docker Compose未安装，请先安装Docker Compose"
        exit 1
    }
    
    # 检查Node.js
    if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
        Write-Error "Node.js未安装，请先安装Node.js"
        exit 1
    }
    
    # 检查npm
    if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
        Write-Error "npm未安装，请先安装npm"
        exit 1
    }
    
    Write-Info "所有依赖检查通过"
}

# 配置环境变量
function Set-Environment {
    Write-Info "配置环境变量..."
    
    if (-not (Test-Path ".env")) {
        if (Test-Path "env.example") {
            Copy-Item "env.example" ".env"
            Write-Warning "已创建.env文件，请编辑配置"
        } else {
            Write-Error "未找到环境变量模板文件"
            exit 1
        }
    } else {
        Write-Info ".env文件已存在"
    }
    
    # 提示用户编辑配置
    Write-Warning "请编辑.env文件，设置正确的API密钥和域名配置"
    Read-Host "编辑完成后按回车继续"
}

# 构建前端
function Build-Frontend {
    Write-Info "构建前端应用..."
    
    # 安装依赖
    npm ci
    
    # 构建
    npm run build
    
    Write-Info "前端构建完成"
}

# 构建Docker镜像
function Build-Docker {
    Write-Info "构建Docker镜像..."
    
    # 构建后端镜像
    docker build -t exam-review-backend ./backend
    
    # 构建前端镜像
    docker build -t exam-review-frontend .
    
    Write-Info "Docker镜像构建完成"
}

# 启动服务
function Start-Services {
    Write-Info "启动服务..."
    
    # 使用docker-compose启动
    docker-compose up -d
    
    Write-Info "服务启动完成"
}

# 检查服务状态
function Test-Services {
    Write-Info "检查服务状态..."
    
    # 等待服务启动
    Start-Sleep -Seconds 10
    
    # 检查后端健康状态
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Info "✅ 后端服务正常"
        } else {
            Write-Error "❌ 后端服务异常"
            return $false
        }
    } catch {
        Write-Error "❌ 后端服务异常: $($_.Exception.Message)"
        return $false
    }
    
    # 检查前端
    try {
        $response = Invoke-WebRequest -Uri "http://localhost" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Info "✅ 前端服务正常"
        } else {
            Write-Error "❌ 前端服务异常"
            return $false
        }
    } catch {
        Write-Error "❌ 前端服务异常: $($_.Exception.Message)"
        return $false
    }
    
    Write-Info "所有服务运行正常"
    return $true
}

# 显示访问信息
function Show-AccessInfo {
    Write-Header "部署完成！"
    Write-Host "前端地址: http://localhost" -ForegroundColor $Green
    Write-Host "后端API: http://localhost:8000" -ForegroundColor $Green
    Write-Host "API文档: http://localhost:8000/docs" -ForegroundColor $Green
    Write-Host "健康检查: http://localhost:8000/health" -ForegroundColor $Green
    Write-Host "=================================" -ForegroundColor $Blue
}

# 停止服务
function Stop-Services {
    Write-Info "停止服务..."
    docker-compose down
    Write-Info "服务已停止"
}

# 查看日志
function View-Logs {
    Write-Info "查看服务日志..."
    docker-compose logs -f
}

# 清理资源
function Clear-Resources {
    Write-Info "清理资源..."
    docker-compose down -v
    docker system prune -f
    Write-Info "清理完成"
}

# 主菜单
function Show-Menu {
    Write-Header "考试复习助手部署菜单"
    Write-Host "1. 完整部署（推荐）" -ForegroundColor $White
    Write-Host "2. 仅构建前端" -ForegroundColor $White
    Write-Host "3. 仅启动服务" -ForegroundColor $White
    Write-Host "4. 停止服务" -ForegroundColor $White
    Write-Host "5. 查看日志" -ForegroundColor $White
    Write-Host "6. 清理资源" -ForegroundColor $White
    Write-Host "7. 检查服务状态" -ForegroundColor $White
    Write-Host "0. 退出" -ForegroundColor $White
    Write-Host "=================================" -ForegroundColor $Blue
}

# 完整部署流程
function Start-FullDeploy {
    Write-Header "考试复习助手部署脚本"
    Test-Dependencies
    Set-Environment
    Build-Frontend
    Build-Docker
    Start-Services
    if (Test-Services) {
        Show-AccessInfo
    } else {
        Write-Error "部署失败，请检查日志"
        exit 1
    }
}

# 主函数
function Main {
    switch ($Action.ToLower()) {
        "deploy" {
            Start-FullDeploy
        }
        "build" {
            Build-Frontend
        }
        "start" {
            Start-Services
        }
        "stop" {
            Stop-Services
        }
        "logs" {
            View-Logs
        }
        "cleanup" {
            Clear-Resources
        }
        "status" {
            Test-Services
        }
        default {
            do {
                Show-Menu
                $choice = Read-Host "请选择操作 (0-7)"
                switch ($choice) {
                    "1" {
                        Start-FullDeploy
                        break
                    }
                    "2" {
                        Build-Frontend
                        break
                    }
                    "3" {
                        Start-Services
                        break
                    }
                    "4" {
                        Stop-Services
                        break
                    }
                    "5" {
                        View-Logs
                        break
                    }
                    "6" {
                        Clear-Resources
                        break
                    }
                    "7" {
                        Test-Services
                        break
                    }
                    "0" {
                        Write-Info "退出部署脚本"
                        exit 0
                    }
                    default {
                        Write-Error "无效选择，请重新输入"
                    }
                }
            } while ($true)
        }
    }
}

# 脚本入口
Main 