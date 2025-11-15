@echo off
REM ========================================
REM Configurar .env automaticamente
REM ========================================

echo ======================================================================
echo   CONFIGURANDO .ENV PARA AURONEX
echo ======================================================================
echo.

REM Verificar se .env já existe
if exist .env (
    echo [AVISO] Arquivo .env ja existe!
    echo.
    choice /C SN /M "Deseja fazer backup e sobrescrever"
    if errorlevel 2 goto :EOF
    
    REM Fazer backup
    copy .env .env.backup.%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2% >nul
    echo [OK] Backup criado: .env.backup.*
    echo.
)

REM Copiar .env.local para .env
copy .env.local .env >nul

echo [OK] Arquivo .env criado com sucesso!
echo.
echo ======================================================================
echo   CHAVES GERADAS:
echo ======================================================================
echo.
echo ENCRYPTION_KEY = 3zHzFSUpbptbx2sOSG1E9eAVpT0egw9aWFsczVtcq44=
echo SECRET_KEY = 9f05ab3f6c9eea75e00ada9ebac1a8293107273420c167a332c385e11e6b9105
echo.
echo ======================================================================
echo   [ATENCAO] NUNCA commite o .env no Git!
echo ======================================================================
echo.
echo Proximos passos:
echo 1. Configure suas API Keys das exchanges (se tiver)
echo 2. Execute: python scripts/migrate_encryption.py (se tem API Keys antigas)
echo 3. Reinicie os servicos
echo.
pause






