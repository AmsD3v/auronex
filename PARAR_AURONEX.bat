@echo off
title Parar Auronex
color 0C

echo ========================================
echo   PARANDO AURONEX ROBO TRADER
echo ========================================
echo.

echo Parando processos Python (FastAPI, Streamlit, Celery)...
taskkill /F /IM python.exe /T 2>nul
if errorlevel 1 (
    echo Nenhum processo Python encontrado
) else (
    echo OK - Processos Python encerrados
)

echo.
echo Parando processos uvicorn...
taskkill /F /IM uvicorn.exe /T 2>nul

echo.
echo Parando processos streamlit...
taskkill /F /IM streamlit.exe /T 2>nul

echo.
echo ========================================
echo   SISTEMA AURONEX PARADO!
echo ========================================
echo.
pause




