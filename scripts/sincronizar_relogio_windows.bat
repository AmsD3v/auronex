@echo off
REM ========================================
REM Sincronizar Relógio do Windows
REM ========================================

echo ======================================================================
echo   SINCRONIZANDO RELOGIO DO WINDOWS
echo ======================================================================
echo.

echo [1/3] Parando servico de tempo...
net stop w32time

echo.
echo [2/3] Sincronizando com servidor NTP...
w32tm /config /manualpeerlist:"time.windows.com,0x1" /syncfromflags:manual /reliable:YES /update
w32tm /resync /force

echo.
echo [3/3] Iniciando servico de tempo...
net start w32time

echo.
echo ======================================================================
echo   SINCRONIZACAO CONCLUIDA!
echo ======================================================================
echo.
echo Hora atual: %date% %time%
echo.
echo Agora tente novamente:
echo   python scripts/importar_api_keys_do_env.py
echo.
pause





