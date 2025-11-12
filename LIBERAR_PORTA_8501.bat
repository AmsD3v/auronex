@echo off
REM Liberar porta 8501

echo Procurando processo na porta 8501...
FOR /F "tokens=5" %%P IN ('netstat -ano ^| findstr :8501') DO (
    echo Matando PID %%P...
    taskkill /PID %%P /F
)

echo.
echo Porta 8501 liberada!
echo.
pause

