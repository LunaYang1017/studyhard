@echo off
setlocal

echo 启动考试复习助手服务...

echo 启动后端服务...
start "Backend Server" cmd /k "set PYTHONPATH=%cd% && python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

echo 等待后端服务启动...
timeout /t 3 /nobreak > nul

echo 启动前端服务...
start "Frontend Server" cmd /k "npm run dev"

echo 服务启动完成！
echo 后端地址: http://localhost:8000
echo 前端地址: http://localhost:3000 (或自动分配的端口)
echo.
echo 按任意键退出...
pause > nul 