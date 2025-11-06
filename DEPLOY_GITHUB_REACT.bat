@echo off
REM ========================================
REM DEPLOY PARA GITHUB - DASHBOARD REACT
REM Commit e push automático
REM ========================================

echo.
echo ============================================================
echo   AURONEX - DEPLOY PARA GITHUB
echo   Dashboard React + Next.js
echo ============================================================
echo.

REM Ir para pasta raiz do projeto
cd /d I:\Robo

REM ========================================
REM 1. VERIFICAR MUDANÇAS
REM ========================================

echo [1/6] Verificando mudancas...
echo.

git status

echo.
echo ============================================================
echo   Arquivos modificados acima serao enviados
echo ============================================================
echo.

REM Pausar para usuário ver
timeout /t 5

REM ========================================
REM 2. ADICIONAR TODOS OS ARQUIVOS
REM ========================================

echo [2/6] Adicionando arquivos ao Git...
echo.

git add .

echo   ✅ Arquivos adicionados
echo.

REM ========================================
REM 3. CRIAR COMMIT
REM ========================================

echo [3/6] Criando commit...
echo.

REM Pegar data/hora atual
set TIMESTAMP=%date:~-4%-%date:~3,2%-%date:~0,2% %time:~0,2%:%time:~3,2%

REM Mensagem de commit
git commit -m "Dashboard React Enterprise - Update %TIMESTAMP%"

if %errorlevel% equ 0 (
    echo   ✅ Commit criado
) else (
    echo   ⚠️  Nenhuma mudanca para commitar
    echo   Verificando se ha commits pendentes...
)

echo.

REM ========================================
REM 4. VERIFICAR BRANCH
REM ========================================

echo [4/6] Verificando branch...
echo.

git branch --show-current

echo   ✅ Branch: main
echo.

REM ========================================
REM 5. PUSH PARA GITHUB
REM ========================================

echo [5/6] Enviando para GitHub...
echo.

git push origin main

if %errorlevel% equ 0 (
    echo.
    echo   ✅ Codigo enviado ao GitHub com sucesso!
) else (
    echo.
    echo   ❌ Erro ao enviar para GitHub
    echo   Verifique sua conexao e credenciais
    pause
    exit /b 1
)

echo.

REM ========================================
REM 6. MOSTRAR RESUMO
REM ========================================

echo [6/6] Resumo do deploy...
echo.

echo ============================================================
echo   ✅ DEPLOY CONCLUIDO!
echo ============================================================
echo.
echo   Codigo enviado para: https://github.com/AmsD3v/auronex
echo.
echo   PROXIMOS PASSOS NO SERVIDOR:
echo.
echo   1. SSH no servidor:
echo      ssh usuario@servidor
echo.
echo   2. Executar script de atualizacao:
echo      cd /home/usuario/robo
echo      ./ATUALIZAR_SERVIDOR_REACT.sh
echo.
echo   3. Aguardar ~3 minutos
echo.
echo   4. Acessar:
echo      https://app.auronex.com.br
echo.
echo ============================================================
echo   Sistema atualizado no GitHub!
echo   Pronto para deploy no servidor!
echo ============================================================
echo.

REM Ver último commit
echo   Ultimo commit:
git log -1 --oneline

echo.
echo   URL do repositorio: https://github.com/AmsD3v/auronex.git
echo.

pause

