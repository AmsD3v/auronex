@echo off
echo ===================================
echo   TESTAR ENDPOINT BALANCE
echo ===================================
echo.

echo [INFO] Testando endpoints da API...
echo.

REM Ativar venv
call venv\Scripts\activate.bat

REM Testar com Python
python -c "import requests; r = requests.get('http://localhost:8001/health'); print(f'Health: {r.status_code} - {r.json()}')"

echo.
echo Aguarde o proximo teste...
timeout /t 2 /nobreak >nul

python -c "import requests; print('Testando /api/exchange/balance...'); r = requests.get('http://localhost:8001/api/exchange/balance', headers={'Authorization': 'Bearer SEU_TOKEN_AQUI'}); print(f'Status: {r.status_code}'); print(f'Response: {r.text[:200]}')" 2>nul

echo.
echo ===================================
echo.
echo Se deu erro 401: Normal (precisa token)
echo Se deu erro 404: Backend nao carregou router
echo Se deu 200 OK: FUNCIONANDO!
echo.

pause

