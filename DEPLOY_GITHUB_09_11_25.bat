@echo off
REM ====================================
REM DEPLOY GITHUB COM VERSIONAMENTO
REM Data: 09/11/2025
REM Versao: 1.0.XXb (auto incrementa)
REM ====================================

cd /d I:\Robo

echo.
echo ============================================================
echo   DEPLOY GITHUB - VERSIONAMENTO AUTOMATICO
echo ============================================================
echo.

REM Ler versao atual do arquivo
if not exist VERSION.txt (
    echo 1.0.01b > VERSION.txt
)

set /p VERSAO_ATUAL=<VERSION.txt
echo Versao atual: %VERSAO_ATUAL%

REM Extrair numero da versao (1.0.XXb)
for /f "tokens=3 delims=." %%a in ("%VERSAO_ATUAL%") do set PATCH=%%a
REM Remover 'b' do final
set PATCH_NUM=%PATCH:~0,-1%

REM Incrementar
set /a PATCH_NUM+=1

REM Adicionar zeros se necessario
if %PATCH_NUM% LSS 10 set PATCH_NUM=0%PATCH_NUM%

REM Nova versao
set NOVA_VERSAO=1.0.%PATCH_NUM%b

echo Nova versao: %NOVA_VERSAO%
echo.

REM Pedir descricao
set /p DESCRICAO="Descricao das mudancas: "
echo.

REM Salvar nova versao
echo %NOVA_VERSAO% > VERSION.txt

echo ============================================================
echo   FAZENDO DEPLOY
echo ============================================================
echo.

REM Mostrar mudancas
git status --short
echo.
pause

REM Git add
git add -A

REM Commit
git commit -m "v%NOVA_VERSAO%: %DESCRICAO%"

REM Tag
git tag -a v%NOVA_VERSAO% -m "%DESCRICAO%"

REM Push
git push origin main
git push origin v%NOVA_VERSAO%

echo.
echo ============================================================
echo   DEPLOY CONCLUIDO!
echo ============================================================
echo.
echo Versao: %VERSAO_ATUAL% -^> %NOVA_VERSAO%
echo Tag: v%NOVA_VERSAO%
echo GitHub: https://github.com/AmsD3v/auronex/releases/tag/v%NOVA_VERSAO%
echo.
echo PROXIMO PASSO:
echo   No servidor, execute:
echo   ./ATUALIZAR_SERVER_PRODUCAO_09_11_25.sh
echo.
echo ============================================================
echo.

pause

