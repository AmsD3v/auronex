@echo off
REM Matar tudo e reiniciar limpo
cd /d I:\Robo

echo Matando processos...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul

timeout /t 2

echo Iniciando sistema...
call TESTAR_LOCAL.bat

