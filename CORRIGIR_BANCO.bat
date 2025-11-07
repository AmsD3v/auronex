@echo off
REM ====================================
REM CORRIGIR BANCO - Adicionar colunas
REM ====================================

cd /d I:\Robo

echo.
echo Atualizando banco de dados...
echo.

REM Adicionar colunas (ignora se já existir)
sqlite3 db.sqlite3 "ALTER TABLE bot_configurations ADD COLUMN is_testnet BOOLEAN DEFAULT 1;" 2>nul
sqlite3 db.sqlite3 "ALTER TABLE bot_configurations ADD COLUMN analysis_interval INTEGER DEFAULT 5;" 2>nul
sqlite3 db.sqlite3 "ALTER TABLE bot_configurations ADD COLUMN hunter_mode BOOLEAN DEFAULT 0;" 2>nul

echo.
echo ✅ Banco atualizado!
echo.
echo Colunas adicionadas:
echo   - is_testnet (Testnet/Producao)
echo   - analysis_interval (Velocidade: 1-5s)
echo   - hunter_mode (Modo cacador)
echo.

REM Verificar estrutura
echo Estrutura atual da tabela:
sqlite3 db.sqlite3 ".schema bot_configurations"

echo.
pause


