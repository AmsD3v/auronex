# 🔧 Como Usar o Ambiente Virtual (venv)

## ✅ O Que É e Por Que Usar?

O **ambiente virtual (venv)** isola as dependências do RoboTrader de outros projetos Python no seu computador.

**Benefícios:**
- ✅ Sem conflitos com outros projetos
- ✅ Versões específicas de cada biblioteca
- ✅ Fácil de recriar em outro computador
- ✅ Boa prática profissional

---

## 🚀 Como Usar no Dia a Dia

### **1. Ativar o Ambiente Virtual**

**SEMPRE que for usar o RoboTrader**, ative o venv primeiro:

#### Windows (PowerShell)
```powershell
cd I:\Robo
.\venv\Scripts\activate
```

#### Windows (CMD)
```cmd
cd I:\Robo
venv\Scripts\activate.bat
```

#### Linux/macOS
```bash
cd /caminho/para/Robo
source venv/bin/activate
```

**Você verá** `(venv)` no início da linha do terminal:
```
(venv) PS I:\Robo>
```

---

### **2. Usar o Bot Normalmente**

Com o venv ativado, use todos os comandos normalmente:

```powershell
# Testar conexão
python scripts/test_connection.py

# Baixar dados
python scripts/download_data.py --days 7

# Executar backtest
python scripts/run_backtest.py

# Executar bot
python main.py
```

---

### **3. Desativar o Ambiente Virtual**

Quando terminar de usar o RoboTrader:

```powershell
deactivate
```

O `(venv)` desaparecerá do prompt.

---

## 📝 Comandos Úteis

### Verificar Se Está no Venv
```powershell
# Se aparecer (venv) no início, está ativado
# Ou verifique:
where python
# Deve mostrar: I:\Robo\venv\Scripts\python.exe
```

### Ver Bibliotecas Instaladas (no venv)
```powershell
# Ativar venv primeiro!
.\venv\Scripts\activate

# Listar todas
pip list

# Verificar uma específica
pip show ccxt
```

### Atualizar Uma Biblioteca
```powershell
# Ativar venv primeiro!
.\venv\Scripts\activate

# Atualizar
pip install --upgrade nome_da_biblioteca
```

### Reinstalar Tudo do Zero
```powershell
# Deletar venv atual
Remove-Item -Recurse -Force venv

# Criar novo
python -m venv venv

# Ativar
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

---

## 🎯 Workflow Típico

### Toda vez que for usar o bot:

```powershell
# 1. Abrir PowerShell/Terminal
# 2. Ir para a pasta do projeto
cd I:\Robo

# 3. Ativar venv
.\venv\Scripts\activate

# 4. Usar o bot
python main.py

# 5. Quando terminar, desativar
deactivate
```

---

## 🔄 Atalhos (Opcional)

### Criar Script de Ativação Rápida

**Windows - arquivo `start.bat`:**
```batch
@echo off
cd /d I:\Robo
call venv\Scripts\activate.bat
cls
echo.
echo ========================================
echo   RoboTrader - Ambiente Ativado
echo ========================================
echo.
echo Comandos disponiveis:
echo   python scripts/test_connection.py
echo   python scripts/run_backtest.py
echo   python main.py
echo.
cmd /k
```

**Uso:**
1. Salve como `start.bat` em `I:\Robo\`
2. Duplo clique para abrir terminal já com venv ativado

---

## ⚠️ Problemas Comuns

### "Scripts\activate: cannot be loaded..."
**Solução:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Venv não ativa / comando não encontrado
**Solução:**
```powershell
# Recriar venv
Remove-Item -Recurse venv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### "pip: command not found" (após ativar)
**Solução:**
```powershell
# Use python -m pip em vez de pip
python -m pip install -r requirements.txt
```

### Esqueci de ativar e instalei sem venv
**Solução:**
- Não tem problema! As bibliotecas estão no sistema global
- Da próxima vez, ative o venv antes
- Se quiser limpar, desinstale manualmente ou reinstale Python

---

## 💡 Dicas Pro

### 1. Sempre Ativar Primeiro
Crie o hábito:
```
cd I:\Robo → .\venv\Scripts\activate → usar bot
```

### 2. Verificar Ativação
Se o prompt mostra `(venv)`, está OK!

### 3. Um Venv Por Projeto
Cada projeto Python deve ter seu próprio venv.

### 4. Não Versionar o Venv
O `.gitignore` já está configurado para ignorar a pasta `venv/`.

### 5. Compartilhar Projeto
Para outro computador:
1. Copie todo o projeto EXCETO `venv/`
2. No novo computador: `python -m venv venv`
3. Ative e instale: `pip install -r requirements.txt`

---

## 📦 Conteúdo do Venv

```
venv/
├── Scripts/              # Executáveis (Windows)
│   ├── activate          # Script de ativação
│   ├── python.exe        # Python isolado
│   └── pip.exe          # Pip isolado
├── Lib/                 # Bibliotecas instaladas
│   └── site-packages/   # Onde ficam ccxt, pandas, etc
└── pyvenv.cfg           # Configuração
```

---

## ✅ Checklist de Boas Práticas

Antes de usar o bot:
- [ ] Ativar venv (`.\venv\Scripts\activate`)
- [ ] Confirmar prompt mostra `(venv)`
- [ ] Executar comandos normalmente
- [ ] Desativar quando terminar (`deactivate`)

---

## 🆘 Ainda com Dúvidas?

**Comando universal que sempre funciona:**
```powershell
# Ir para a pasta
cd I:\Robo

# Ativar (escolha um)
.\venv\Scripts\activate           # PowerShell
venv\Scripts\activate.bat         # CMD
source venv/bin/activate          # Linux/Mac

# Usar normalmente
python main.py
```

---

**Ambiente virtual configurado e funcionando! 🎉**

**Lembre-se**: SEMPRE ative o venv antes de usar o RoboTrader!

