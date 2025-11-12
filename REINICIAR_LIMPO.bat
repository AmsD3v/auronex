@echo off
REM ====================================
REM REINICIAR SISTEMA LIMPO
REM Mata tudo e inicia de novo
REM ====================================

echo Matando TODOS processos...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul

timeout /t 3

echo.
echo Iniciando sistema limpo...
echo.

cd /d I:\Robo
call TESTAR_LOCAL.bat










