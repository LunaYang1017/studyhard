# 启动后端服务
Write-Host "启动后端服务..." -ForegroundColor Green
Set-Location backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload 