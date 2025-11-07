@echo off
REM ====================================
REM FAZER DEPLOY PARA GITHUB
REM Envia código e mostra instruções
REM ====================================

cd /d I:\Robo

echo.
echo ============================================================
echo   FAZER DEPLOY PARA GITHUB
echo ============================================================
echo.

REM Mostrar mudanças
echo Arquivos modificados:
git status --short

echo.
pause

REM Adicionar tudo
git add -A

REM Commit com timestamp
for /f "tokens=1-3 delims=/ " %%a in ("%date%") do set data=%%c-%%b-%%a
for /f "tokens=1-2 delims=: " %%a in ("%time%") do set hora=%%a:%%b

git commit -m "Deploy %data% %hora%"

REM Push
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo   DEPLOY CONCLUIDO!
    echo   Codigo enviado para GitHub
    echo ============================================================
    echo.
    echo PROXIMO PASSO:
    echo.
    echo   No servidor SSH, execute:
    echo   chmod +x DEPLOY_SERVIDOR_FINAL.sh
    echo   ./DEPLOY_SERVIDOR_FINAL.sh
    echo.
    echo   Aguarde ~5-8 minutos
    echo.
    echo   Depois acesse:
    echo   https://app.auronex.com.br/
    echo.
    echo ============================================================
) else (
    echo.
    echo [ERRO] Falha ao enviar para GitHub
    echo.
)

pause
