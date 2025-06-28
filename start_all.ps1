# 启动所有服务
Write-Host "启动考试复习助手服务..." -ForegroundColor Green

# 启动后端服务
Write-Host "启动后端服务..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location backend; python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

# 等待后端启动
Write-Host "等待后端服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# 启动前端服务
Write-Host "启动前端服务..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"

Write-Host "服务启动完成！" -ForegroundColor Green
Write-Host "后端地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host "前端地址: http://localhost:3001" -ForegroundColor Cyan
Write-Host "测试页面: http://localhost:3001/test_frontend.html" -ForegroundColor Cyan 