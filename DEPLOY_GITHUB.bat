@echo off
chcp 65001 >nul
title Auronex - Deploy para GitHub
color 0A

echo ========================================
echo   AURONEX - DEPLOY PARA GITHUB
echo ========================================
echo.

cd /d I:\Robo

REM Ler versão atual
if not exist VERSION.txt (
    echo 1.0-A1 > VERSION.txt
    echo [INFO] Arquivo VERSION.txt criado - v1.0-A1
)

set /p VERSAO_ATUAL=<VERSION.txt
echo Versao atual: %VERSAO_ATUAL%
echo.

REM Menu de tipo de versão
echo Tipo de atualizacao:
echo   1. Alpha (desenvolvimento/testes internos)
echo   2. Beta (testes publicos)
echo   3. Release (producao estavel)
echo   4. Patch (correcao bug)
echo   5. Minor (melhoria pequena)
echo   6. Major (mudanca grande)
echo.

set /p TIPO="Digite 1-6: "

REM Calcular nova versão
if "%TIPO%"=="1" (
    REM Alpha - incrementar número alpha
    for /f "tokens=1,2 delims=-A" %%a in ("%VERSAO_ATUAL%") do (
        set BASE=%%a
        set ALPHA_NUM=%%b
    )
    if not defined ALPHA_NUM set ALPHA_NUM=0
    set /a ALPHA_NUM+=1
    set NOVA_VERSAO=!BASE!-A!ALPHA_NUM!
    set MENSAGEM_TIPO=alpha
)

if "%TIPO%"=="2" (
    REM Beta
    for /f "tokens=1,2 delims=-" %%a in ("%VERSAO_ATUAL%") do (
        set BASE=%%a
        set /a BETA_NUM=1
    )
    set NOVA_VERSAO=!BASE!-B!BETA_NUM!
    set MENSAGEM_TIPO=beta
)

if "%TIPO%"=="3" (
    REM Release
    for /f "tokens=1 delims=-" %%a in ("%VERSAO_ATUAL%") do (
        set NOVA_VERSAO=%%a
    )
    set MENSAGEM_TIPO=release
)

if "%TIPO%"=="4" (
    REM Patch (1.0.1, 1.0.2...)
    for /f "tokens=1,2,3 delims=." %%a in ("%VERSAO_ATUAL%") do (
        set MAJOR=%%a
        set MINOR=%%b
        set /a PATCH=%%c+1
    )
    if not defined PATCH set PATCH=1
    set NOVA_VERSAO=!MAJOR!.!MINOR!.!PATCH!
    set MENSAGEM_TIPO=patch
)

if "%TIPO%"=="5" (
    REM Minor (1.1, 1.2...)
    for /f "tokens=1,2 delims=." %%a in ("%VERSAO_ATUAL%") do (
        set MAJOR=%%a
        set /a MINOR=%%b+1
    )
    set NOVA_VERSAO=!MAJOR!.!MINOR!
    set MENSAGEM_TIPO=minor
)

if "%TIPO%"=="6" (
    REM Major (2.0, 3.0...)
    for /f "tokens=1 delims=." %%a in ("%VERSAO_ATUAL%") do (
        set /a MAJOR=%%a+1
    )
    set NOVA_VERSAO=!MAJOR!.0
    set MENSAGEM_TIPO=major
)

echo.
echo ========================================
echo Nova versao: %NOVA_VERSAO%
echo ========================================
echo.

REM Pedir descrição da mudança
set /p DESCRICAO="Descricao da mudanca: "

echo.
echo ========================================
echo   PROCESSANDO DEPLOY
echo ========================================
echo.

REM Salvar nova versão
echo %NOVA_VERSAO% > VERSION.txt

REM Git add
echo [1/4] Adicionando arquivos...
git add .

REM Git commit
echo [2/4] Criando commit...
git commit -m "v%NOVA_VERSAO%: %MENSAGEM_TIPO% - %DESCRICAO%"

REM Criar tag
echo [3/4] Criando tag de versao...
git tag -a v%NOVA_VERSAO% -m "Versao %NOVA_VERSAO%: %DESCRICAO%"

REM Git push
echo [4/4] Enviando para GitHub...
git push origin main
git push origin v%NOVA_VERSAO%

echo.
echo ========================================
echo   DEPLOY COMPLETO!
echo ========================================
echo.
echo Versao: v%NOVA_VERSAO%
echo Commit: %MENSAGEM_TIPO%
echo Descricao: %DESCRICAO%
echo.
echo GitHub: https://github.com/AmsD3v/auronex
echo Tag: https://github.com/AmsD3v/auronex/releases/tag/v%NOVA_VERSAO%
echo.
echo ========================================
echo   PROXIMO PASSO
echo ========================================
echo.
echo No servidor Xubuntu, execute:
echo   ./ATUALIZAR_SERVIDOR.sh
echo.
echo Isso vai:
echo   - Baixar versao v%NOVA_VERSAO%
echo   - Reiniciar servicos
echo   - Sistema atualizado!
echo.

pause

