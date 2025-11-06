@echo off
REM ========================================
REM PREPARAR DEPLOY PARA PRODUÇÃO
REM Build otimizado + Instruções
REM ========================================

echo.
echo ============================================================
echo   PREPARANDO DASHBOARD REACT PARA DEPLOY
echo   Destino: https://app.auronex.com.br
echo ============================================================
echo.

cd auronex-dashboard

echo [1/4] Limpando builds anteriores...
if exist .next rmdir /s /q .next
timeout /t 1 /nobreak >nul

echo [2/4] Instalando dependencias (producao)...
call npm ci --production=false

echo [3/4] Executando build de producao...
call npm run build

echo [4/4] Criando arquivos .env...
copy env.production.example .env.production >nul 2>&1
copy env.local.example .env.local >nul 2>&1

echo.
echo ============================================================
echo   BUILD CONCLU�DO COM SUCESSO!
echo ============================================================
echo.
echo ARQUIVOS PRONTOS EM: auronex-dashboard\
echo.
echo PR�XIMOS PASSOS:
echo   1. Compactar pasta auronex-dashboard
echo   2. Enviar ao servidor
echo   3. Seguir guia: DEPLOY_PRODUCAO_REACT.md
echo.
echo LEIA: DEPLOY_PRODUCAO_REACT.md
echo.
pause

