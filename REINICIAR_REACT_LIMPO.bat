@echo off
echo ===================================
echo   REINICIAR REACT (LIMPO)
echo ===================================
echo.

echo [INFO] Parando processos Node.js...
taskkill /F /IM node.exe 2>nul

timeout /t 2 /nobreak >nul

echo [OK] Processos parados!
echo.

echo [INFO] Limpando cache do Next.js...
cd auronex-dashboard

if exist .next (
    rmdir /s /q .next
    echo [OK] Cache limpo!
) else (
    echo [INFO] Cache ja estava limpo
)

echo.
echo [INFO] Limpando node_modules/.cache...
if exist node_modules\.cache (
    rmdir /s /q node_modules\.cache
    echo [OK] Cache do node_modules limpo!
)

echo.
echo ===================================
echo   INICIANDO REACT LIMPO
echo ===================================
echo.
echo URL: http://localhost:3000
echo.
echo Aguarde ~15 segundos...
echo (Primeira inicializacao apos limpar cache)
echo.

npm run dev

pause

