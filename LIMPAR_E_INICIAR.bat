@echo off
REM Limpar tudo e iniciar do zero
cd /d I:\Robo

echo Matando processos...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul

echo.
echo Limpando cache React...
cd auronex-dashboard
if exist .next rmdir /S /Q .next
if exist node_modules\.cache rmdir /S /Q node_modules\.cache

echo.
echo Iniciando FastAPI...
cd ..
start "FastAPI" cmd /k "venv\Scripts\activate && uvicorn fastapi_app.main:app --port 8001 --reload"

timeout /t 5

echo Iniciando React...
cd auronex-dashboard
start "React" cmd /k "npm run dev"

echo.
echo Sistema iniciando...
echo Aguarde ~30s
echo.
echo Depois acesse: http://localhost:8501
echo.
echo IMPORTANTE: Pressione Ctrl+Shift+Delete no navegador
echo             Limpar cache e cookies
echo             Recarregar pagina
echo.
pause




