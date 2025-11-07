@echo off
REM ====================================
REM FAZER DEPLOY - Manual
REM Você controla quando enviar
REM ====================================

cd /d I:\Robo

echo.
echo ============================================================
echo   DEPLOY PARA GITHUB
echo ============================================================
echo.

REM Mostrar mudanças
git status

echo.
echo Arquivos acima serao enviados.
echo.
pause

REM Adicionar tudo
git add .

REM Commit com timestamp
set HORA=%time:~0,2%:%time:~3,2%
git commit -m "Deploy %date% %HORA%"

REM Push
git push origin main

echo.
echo ============================================================
echo   ENVIADO PARA GITHUB!
echo ============================================================
echo.
echo Proximo: Execute no servidor
echo   ./DEPLOY_PRODUCAO_4_TERMINAIS.sh
echo.

pause

