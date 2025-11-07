@echo off
REM ====================================
REM DEPLOY COM VERSIONAMENTO
REM Atualiza versao automaticamente
REM ====================================

cd /d I:\Robo

echo.
echo ============================================================
echo   AURONEX - DEPLOY COM VERSIONAMENTO
echo ============================================================
echo.

REM Ler versao atual
set /p VERSAO_ATUAL=<VERSION.txt
echo Versao atual: %VERSAO_ATUAL%
echo.

REM Separar versao (1.0.0-beta)
for /f "tokens=1-3 delims=.-" %%a in ("%VERSAO_ATUAL%") do (
    set MAJOR=%%a
    set MINOR=%%b
    set PATCH=%%c
)

REM Remover sufixo beta/alpha
for /f "tokens=1 delims=-" %%a in ("%PATCH%") do set PATCH_NUM=%%a

REM Menu de versao
echo Tipo de atualizacao:
echo   1. Patch (1.0.X - bugfix)
echo   2. Minor (1.X.0 - feature)
echo   3. Major (X.0.0 - breaking change)
echo   4. Beta (mantem beta)
echo   5. Release (remove beta - versao estavel!)
echo.

set /p TIPO="Escolha (1-5): "
echo.

REM Calcular nova versao
if "%TIPO%"=="1" (
    set /a PATCH_NUM+=1
    set NOVA_VERSAO=%MAJOR%.%MINOR%.%PATCH_NUM%-beta
    set TIPO_MSG=Bugfix
)

if "%TIPO%"=="2" (
    set /a MINOR+=1
    set NOVA_VERSAO=%MAJOR%.%MINOR%.0-beta
    set TIPO_MSG=Feature
)

if "%TIPO%"=="3" (
    set /a MAJOR+=1
    set NOVA_VERSAO=%MAJOR%.0.0-beta
    set TIPO_MSG=Breaking Change
)

if "%TIPO%"=="4" (
    set /a PATCH_NUM+=1
    set NOVA_VERSAO=%MAJOR%.%MINOR%.%PATCH_NUM%-beta
    set TIPO_MSG=Beta Update
)

if "%TIPO%"=="5" (
    REM Release - Remove beta
    set NOVA_VERSAO=%MAJOR%.%MINOR%.%PATCH_NUM%
    set TIPO_MSG=Release Estavel
)

echo Nova versao: %NOVA_VERSAO%
echo Tipo: %TIPO_MSG%
echo.

REM Pedir descricao
set /p DESCRICAO="Descricao das mudancas: "
echo.

echo ============================================================
echo   FAZENDO DEPLOY
echo ============================================================
echo.

REM Salvar nova versao
echo %NOVA_VERSAO% > VERSION.txt

REM Mostrar mudancas
echo Arquivos modificados:
git status --short
echo.
pause

REM Git add
git add -A

REM Commit com versao
git commit -m "v%NOVA_VERSAO%: %TIPO_MSG% - %DESCRICAO%"

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
echo GitHub: https://github.com/AmsD3v/auronex
echo Tag: https://github.com/AmsD3v/auronex/releases/tag/v%NOVA_VERSAO%
echo.
echo ============================================================
echo   PROXIMO PASSO
echo ============================================================
echo.
echo No servidor SSH, execute:
echo   chmod +x ATUALIZAR_SERVIDOR_PRODUCAO.sh
echo   ./ATUALIZAR_SERVIDOR_PRODUCAO.sh
echo.
echo Aguarde ~5-8 minutos
echo.
echo Acesse: https://app.auronex.com.br/
echo.
echo ============================================================
echo.

pause
