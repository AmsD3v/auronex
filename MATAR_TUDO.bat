@echo off
REM ====================================
REM MATAR TODOS PROCESSOS
REM Python + Node.js
REM ====================================

echo.
echo ============================================================
echo   MATANDO TODOS OS PROCESSOS
echo ============================================================
echo.

echo [1/2] Matando Python...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul

echo [2/2] Matando Node.js...
taskkill /F /IM node.exe 2>nul

echo.
echo ✅ Todos processos mortos!
echo.
echo Agora execute:
echo   TESTAR_LOCAL.bat
echo.

pause


