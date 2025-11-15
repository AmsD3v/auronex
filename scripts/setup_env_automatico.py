#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Automático do .env
Configura tudo automaticamente!
"""

import os
import sys
import io
from pathlib import Path

# Fix encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*70)
print("  SETUP AUTOMATICO - AURONEX")
print("="*70)
print()

# Diretório raiz do projeto
projeto_root = Path(__file__).parent.parent
env_path = projeto_root / '.env'

print(f"Diretorio do projeto: {projeto_root}")
print(f"Arquivo .env sera criado em: {env_path}")
print()

# Verificar se .env já existe
if env_path.exists():
    print("[AVISO] Arquivo .env ja existe!")
    print()
    resposta = input("Deseja fazer backup e sobrescrever? (s/n): ").lower()
    
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("Operacao cancelada.")
        sys.exit(0)
    
    # Fazer backup
    from datetime import datetime
    backup_name = f".env.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_path = projeto_root / backup_name
    
    with open(env_path, 'r') as f:
        backup_content = f.read()
    
    with open(backup_path, 'w') as f:
        f.write(backup_content)
    
    print(f"[OK] Backup criado: {backup_name}")
    print()

# Conteúdo do .env (já com as chaves geradas!)
env_content = """# ========================================
# AURONEX TRADING BOT - Configuração LOCAL
# ========================================
# Gerado automaticamente em: 14/11/2025

# ========================================
# SEGURANÇA - CRÍTICO
# ========================================

# Chave de criptografia para API Keys
ENCRYPTION_KEY=3zHzFSUpbptbx2sOSG1E9eAVpT0egw9aWFsczVtcq44=

# Chave secreta para JWT tokens
SECRET_KEY=9f05ab3f6c9eea75e00ada9ebac1a8293107273420c167a332c385e11e6b9105

# Algoritmo JWT
ALGORITHM=HS256

# Expiração dos tokens
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# ========================================
# CORS - Origens Permitidas
# ========================================

ALLOWED_ORIGINS=http://localhost:8501,http://127.0.0.1:8501

# ========================================
# AMBIENTE
# ========================================

ENVIRONMENT=development
DEBUG_MODE=True
LOG_LEVEL=INFO

# ========================================
# BANCO DE DADOS
# ========================================

DATABASE_URL=sqlite:///./db.sqlite3

# ========================================
# BOT TRADING
# ========================================

# Paper Trading (True = simulação, False = ordens reais)
PAPER_TRADING=True
USE_TESTNET=True

# Configurações padrão
TRADING_SYMBOL=BTC/USDT
TIMEFRAME=15m
STRATEGY=trend_following

# Gerenciamento de Risco
POSITION_SIZE_PERCENT=0.10
STOP_LOSS_PERCENT=0.02
TAKE_PROFIT_PERCENT=0.04
MAX_DRAWDOWN_PERCENT=0.10
MAX_TRADES_PER_DAY=10

# ========================================
# EXCHANGES (Configure as que for usar)
# ========================================

# Binance Testnet
BINANCE_TESTNET_API_KEY=
BINANCE_TESTNET_SECRET_KEY=

# ========================================
# NOTIFICAÇÕES (Opcional)
# ========================================

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
ENABLE_TELEGRAM=False

SLACK_WEBHOOK_URL=
DISCORD_WEBHOOK_URL=

# ========================================
# CACHE (Redis) - Opcional
# ========================================

REDIS_URL=redis://localhost:6379/0

# ========================================
# MONITORAMENTO (Opcional)
# ========================================

SENTRY_DSN=

# ========================================
# SISTEMA
# ========================================

UPDATE_INTERVAL=60
SAVE_HISTORICAL_DATA=True
"""

# Escrever .env
print("[1/3] Criando arquivo .env...")
try:
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("[OK] Arquivo .env criado com sucesso!")
    print()
except Exception as e:
    print(f"[ERRO] Nao foi possivel criar .env: {e}")
    sys.exit(1)

# Verificar se foi criado
print("[2/3] Verificando arquivo...")
if env_path.exists():
    size = env_path.stat().st_size
    print(f"[OK] Arquivo .env existe ({size} bytes)")
    print()
else:
    print("[ERRO] Arquivo .env nao foi criado!")
    sys.exit(1)

# Mostrar resumo
print("[3/3] Configuracao completa!")
print()
print("="*70)
print("  CONFIGURACAO CONCLUIDA!")
print("="*70)
print()
print("Arquivo criado: .env")
print("Localizacao:", env_path)
print()
print("Chaves configuradas:")
print("  - ENCRYPTION_KEY: 3zHzFSUpbptbx2sOSG1E9eAV...")
print("  - SECRET_KEY: 9f05ab3f6c9eea75e00ada9e...")
print("  - CORS: http://localhost:8501")
print("  - Ambiente: development")
print()
print("="*70)
print("  PROXIMOS PASSOS:")
print("="*70)
print()
print("1. Se voce tem API Keys antigas, execute:")
print("   python scripts/migrate_encryption.py")
print()
print("2. Reinicie os servicos:")
print("   MATAR_TUDO.bat")
print("   TESTAR_SERVER_LOCAL_09_11_25.bat")
print()
print("3. Teste o sistema:")
print("   http://localhost:8501")
print()
print("="*70)
print("[ATENCAO] NUNCA commite o .env no Git!")
print("="*70)
print()






