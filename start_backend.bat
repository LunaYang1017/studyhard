@echo off
echo 正在启动后端服务...
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause 