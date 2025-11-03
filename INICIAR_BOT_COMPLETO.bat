@echo off
echo ========================================
echo   INICIANDO SISTEMA COMPLETO DO BOT
echo ========================================
echo.
echo Este script vai iniciar TODOS os componentes:
echo   1. Django (porta 8001)
echo   2. Celery Worker (executa trades)
echo   3. Celery Beat (dispara analises)
echo   4. Dashboard Streamlit (porta 8501)
echo.
echo IMPORTANTE: Vao abrir 4 janelas!
echo NAO FECHE NENHUMA DELAS!
echo.
pause

echo.
echo 1/4 Iniciando Django...
start "Django Server" cmd /k "cd /d I:\Robo && call venv\Scripts\activate.bat && set PYTHONPATH=I:\Robo && cd saas && python manage.py runserver 8001"
timeout /t 5

echo 2/4 Iniciando Celery Worker...
start "Celery Worker" cmd /k "cd /d I:\Robo && call venv\Scripts\activate.bat && set PYTHONPATH=I:\Robo && cd saas && celery -A saas worker --pool=solo --loglevel=info"
timeout /t 5

echo 3/4 Iniciando Celery Beat...
start "Celery Beat" cmd /k "cd /d I:\Robo && call venv\Scripts\activate.bat && set PYTHONPATH=I:\Robo && cd saas && celery -A saas beat --loglevel=info"
timeout /t 5

echo 4/4 Iniciando Dashboard...
start "Dashboard Streamlit" cmd /k "cd /d I:\Robo && call venv\Scripts\activate.bat && streamlit run dashboard_master.py --server.port 8501"

echo.
echo ========================================
echo   SISTEMA INICIADO COM SUCESSO!
echo ========================================
echo.
echo 4 janelas abertas:
echo   1. Django (porta 8001)
echo   2. Celery Worker
echo   3. Celery Beat
echo   4. Dashboard (porta 8501)
echo.
echo AGUARDE 30 segundos...
timeout /t 30

echo.
echo ========================================
echo   ACESSOS:
echo ========================================
echo.
echo Dashboard: http://localhost:8501
echo Django Admin: http://localhost:8001/admin
echo API Keys: http://localhost:8001/api-keys/
echo.
echo ========================================
echo   IMPORTANTE:
echo ========================================
echo.
echo 1. Mantenha as 4 janelas abertas!
echo 2. Configure Bot no Django Admin
echo 3. Adicione API Keys
echo 4. Ative o bot (is_active = True)
echo 5. Aguarde 5-30 min para primeiro trade
echo.
echo Bot vai executar trades automaticamente!
echo.
pause

