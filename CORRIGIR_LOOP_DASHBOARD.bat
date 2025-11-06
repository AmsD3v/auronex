@echo off
echo ===================================
echo   CORRIGIR LOOP DO DASHBOARD
echo ===================================
echo.

echo [INFO] Parando servidores...
echo.

REM Matar processos Node.js (Next.js)
taskkill /F /IM node.exe 2>nul

REM Aguardar
timeout /t 2 /nobreak >nul

echo [OK] Servidores parados!
echo.

echo [INFO] Limpando cache do Next.js...
echo.

REM Limpar cache do Next.js
if exist "auronex-dashboard\.next" (
    rmdir /s /q "auronex-dashboard\.next"
    echo [OK] Cache do Next.js limpo!
) else (
    echo [INFO] Cache ja estava limpo.
)

echo.
echo [INFO] Limpando node_modules cache...
if exist "auronex-dashboard\.next" (
    rmdir /s /q "auronex-dashboard\.next"
)

echo.
echo ===================================
echo   INICIANDO SISTEMA LIMPO
echo ===================================
echo.

REM Iniciar sistema novamente
call INICIAR_SISTEMA_COMPLETO_REACT.bat

pause

