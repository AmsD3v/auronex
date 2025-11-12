@echo off
REM Reiniciar React LIMPO (deleta cache)

cd /d I:\Robo\auronex-dashboard

echo Deletando cache...
rmdir /s /q .next 2>nul
rmdir /s /q node_modules\.cache 2>nul

echo.
echo Iniciando React DEV MODE...
echo.

npm run dev
