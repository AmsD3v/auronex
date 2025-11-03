# Sistema RoboTrader - Inicialização Estável
# PowerShell Script - Mais confiável que BAT

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INICIANDO SISTEMA ROBOTRADER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Matar processos antigos
Write-Host "Limpando processos antigos..." -ForegroundColor Yellow
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3
Write-Host "✅ Sistema limpo!" -ForegroundColor Green
Write-Host ""

# Definir variáveis
$RoboPath = "I:\Robo"
$VenvPython = "I:\Robo\venv\Scripts\python.exe"
$VenvActivate = "I:\Robo\venv\Scripts\Activate.ps1"

# Verificar se venv existe
if (!(Test-Path $VenvPython)) {
    Write-Host "❌ ERRO: Virtual environment não encontrado!" -ForegroundColor Red
    Write-Host "Caminho esperado: $VenvPython" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Iniciando componentes..." -ForegroundColor Yellow
Write-Host ""

# 1. Django com Waitress (mais estável que runserver)
Write-Host "1/4 Iniciando Django (Waitress)..." -ForegroundColor Cyan
$django = Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$RoboPath\saas'; & '$VenvActivate'; `$env:PYTHONPATH='$RoboPath'; waitress-serve --port=8001 --host=0.0.0.0 saas.wsgi:application"
) -PassThru -WindowStyle Normal

Start-Sleep -Seconds 5
Write-Host "✅ Django iniciado (PID: $($django.Id))" -ForegroundColor Green
Write-Host ""

# 2. Celery Worker
Write-Host "2/4 Iniciando Celery Worker..." -ForegroundColor Cyan
$worker = Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$RoboPath\saas'; & '$VenvActivate'; `$env:PYTHONPATH='$RoboPath'; celery -A saas worker --pool=solo --loglevel=info"
) -PassThru -WindowStyle Normal

Start-Sleep -Seconds 5
Write-Host "✅ Celery Worker iniciado (PID: $($worker.Id))" -ForegroundColor Green
Write-Host ""

# 3. Celery Beat
Write-Host "3/4 Iniciando Celery Beat..." -ForegroundColor Cyan
$beat = Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$RoboPath\saas'; & '$VenvActivate'; `$env:PYTHONPATH='$RoboPath'; celery -A saas beat --loglevel=info"
) -PassThru -WindowStyle Normal

Start-Sleep -Seconds 5
Write-Host "✅ Celery Beat iniciado (PID: $($beat.Id))" -ForegroundColor Green
Write-Host ""

# 4. Dashboard
Write-Host "4/4 Iniciando Dashboard..." -ForegroundColor Cyan
$dashboard = Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$RoboPath'; & '$VenvActivate'; streamlit run dashboard_master.py --server.port 8501 --server.address 0.0.0.0"
) -PassThru -WindowStyle Normal

Start-Sleep -Seconds 5
Write-Host "✅ Dashboard iniciado (PID: $($dashboard.Id))" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "  SISTEMA INICIADO COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "4 janelas abertas:" -ForegroundColor Yellow
Write-Host "  1. Django (Waitress) - PID: $($django.Id)" -ForegroundColor White
Write-Host "  2. Celery Worker - PID: $($worker.Id)" -ForegroundColor White
Write-Host "  3. Celery Beat - PID: $($beat.Id)" -ForegroundColor White
Write-Host "  4. Dashboard - PID: $($dashboard.Id)" -ForegroundColor White
Write-Host ""

Write-Host "Aguardando 20 segundos para tudo inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 20

Write-Host ""
Write-Host "Verificando componentes..." -ForegroundColor Cyan
Write-Host ""

# Verificar Django
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8001" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ Django funcionando (porta 8001)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Django ainda inicializando..." -ForegroundColor Yellow
}

# Verificar Dashboard
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8501" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ Dashboard funcionando (porta 8501)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Dashboard ainda inicializando..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ACESSOS:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Dashboard: http://localhost:8501" -ForegroundColor White
Write-Host "Django Admin: http://localhost:8001/admin" -ForegroundColor White
Write-Host "API Keys: http://localhost:8001/api-keys/" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "  SISTEMA RODANDO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Bot configurado com:" -ForegroundColor Yellow
Write-Host "  ✅ 10 símbolos" -ForegroundColor White
Write-Host "  ✅ Filtro ULTRA agressivo (0.1%)" -ForegroundColor White
Write-Host "  ✅ Piloto Automático" -ForegroundColor White
Write-Host ""
Write-Host "Primeiro trade estimado: 5-15 minutos" -ForegroundColor Yellow
Write-Host ""
Write-Host "Aguarde e observe os logs do Celery Worker!" -ForegroundColor Cyan
Write-Host ""

pause


