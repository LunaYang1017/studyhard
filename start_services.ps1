# 启动考试复习助手服务
Write-Host "🚀 启动考试复习助手服务..." -ForegroundColor Green

# 检查后端服务是否已运行
$backendRunning = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($backendRunning) {
    Write-Host "✅ 后端服务已在运行 (端口 8000)" -ForegroundColor Green
} else {
    Write-Host "🔄 启动后端服务..." -ForegroundColor Yellow
    Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" -WorkingDirectory "backend" -WindowStyle Minimized
    Start-Sleep 3
}

# 检查前端服务是否已运行
$frontendRunning = Get-NetTCPConnection -LocalPort 3001 -ErrorAction SilentlyContinue
if (-not $frontendRunning) {
    $frontendRunning = Get-NetTCPConnection -LocalPort 3002 -ErrorAction SilentlyContinue
}
if (-not $frontendRunning) {
    $frontendRunning = Get-NetTCPConnection -LocalPort 3003 -ErrorAction SilentlyContinue
}
if (-not $frontendRunning) {
    $frontendRunning = Get-NetTCPConnection -LocalPort 3004 -ErrorAction SilentlyContinue
}
if (-not $frontendRunning) {
    $frontendRunning = Get-NetTCPConnection -LocalPort 3005 -ErrorAction SilentlyContinue
}

if ($frontendRunning) {
    Write-Host "✅ 前端服务已在运行 (端口 $($frontendRunning.LocalPort))" -ForegroundColor Green
} else {
    Write-Host "🔄 启动前端服务..." -ForegroundColor Yellow
    Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WindowStyle Minimized
    Start-Sleep 3
}

# 等待服务完全启动
Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
Start-Sleep 5

# 测试后端服务
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        $data = $response.Content | ConvertFrom-Json
        Write-Host "✅ 后端服务运行正常" -ForegroundColor Green
        Write-Host "   状态: $($data.status)" -ForegroundColor Gray
        Write-Host "   文件数量: $($data.files_count.knowledge) 个知识库文件, $($data.files_count.questions) 个题目文件" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ 后端服务测试失败: $($_.Exception.Message)" -ForegroundColor Red
}

# 查找前端服务端口
$frontendPort = $null
for ($port = 3001; $port -le 3010; $port++) {
    $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($connection) {
        $frontendPort = $port
        break
    }
}

if ($frontendPort) {
    Write-Host "✅ 前端服务运行正常 (端口 $frontendPort)" -ForegroundColor Green
    Write-Host "🌐 前端地址: http://localhost:$frontendPort" -ForegroundColor Cyan
} else {
    Write-Host "❌ 前端服务未找到" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 服务启动完成！" -ForegroundColor Green
Write-Host "📝 现在可以:" -ForegroundColor White
Write-Host "   1. 打开浏览器访问前端页面" -ForegroundColor Gray
Write-Host "   2. 创建新会话" -ForegroundColor Gray
Write-Host "   3. 上传文件到个人知识库" -ForegroundColor Gray
Write-Host "   4. 开始聊天和生成题目" -ForegroundColor Gray
Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 