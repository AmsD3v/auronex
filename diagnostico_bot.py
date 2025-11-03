#!/usr/bin/env python3
"""
Script de Diagnóstico Automático do Bot
Verifica todas as condições necessárias para o bot funcionar
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path

print("=" * 60)
print("🔍 DIAGNÓSTICO AUTOMÁTICO DO BOT")
print("=" * 60)
print()

# Cores para Windows
class Colors:
    OK = '\033[92m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    INFO = '\033[94m'
    END = '\033[0m'

def check_ok(msg):
    print(f"{Colors.OK}✅ {msg}{Colors.END}")

def check_fail(msg):
    print(f"{Colors.FAIL}❌ {msg}{Colors.END}")

def check_warning(msg):
    print(f"{Colors.WARNING}⚠️  {msg}{Colors.END}")

def check_info(msg):
    print(f"{Colors.INFO}ℹ️  {msg}{Colors.END}")

# 1. Verificar se Django está rodando
print("1️⃣ Verificando Django...")
try:
    response = requests.get('http://localhost:8001', timeout=5)
    check_ok("Django está rodando (porta 8001)")
except:
    check_fail("Django NÃO está rodando!")
    check_info("Inicie: python manage.py runserver 8001")
print()

# 2. Verificar se Redis está rodando
print("2️⃣ Verificando Redis...")
try:
    import redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    check_ok("Redis está rodando")
except:
    check_fail("Redis NÃO está rodando!")
    check_info("Instale e inicie: redis-server")
print()

# 3. Verificar se Celery Worker está rodando
print("3️⃣ Verificando Celery Worker...")
try:
    result = subprocess.run(
        ['powershell', '-Command', 'Get-Process | Select-String "celery"'],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.stdout and 'celery' in result.stdout.lower():
        check_ok("Celery Worker está rodando")
    else:
        check_fail("Celery Worker NÃO está rodando!")
        check_info("Inicie: celery -A saas worker --pool=solo --loglevel=info")
except:
    check_warning("Não foi possível verificar Celery Worker")
print()

# 4. Verificar Bot Configuration no Django
print("4️⃣ Verificando Bot Configuration...")
try:
    # Tentar conectar ao banco SQLite diretamente
    import sqlite3
    db_path = Path(__file__).parent / 'saas' / 'db.sqlite3'
    
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Verificar se tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bot_configurations'")
        if cursor.fetchone():
            # Contar bots ativos
            cursor.execute("SELECT COUNT(*) FROM bot_configurations WHERE is_active = 1")
            count = cursor.fetchone()[0]
            
            if count > 0:
                check_ok(f"Bot Configuration existe ({count} ativo)")
                
                # Mostrar detalhes
                cursor.execute("""
                    SELECT id, name, exchange, capital, is_active 
                    FROM bot_configurations 
                    WHERE is_active = 1
                """)
                for row in cursor.fetchall():
                    print(f"   📊 Bot ID {row[0]}: {row[1]} | {row[2]} | Capital: {row[3]}")
            else:
                check_fail("Nenhum bot ativo!")
                check_info("Crie e ative um bot em: http://localhost:8001/admin")
        else:
            check_fail("Tabela bot_configurations não existe!")
            check_info("Execute: python manage.py migrate")
        
        conn.close()
    else:
        check_warning("Banco de dados não encontrado")
        check_info("Execute: python manage.py migrate")
except Exception as e:
    check_warning(f"Não foi possível verificar Bot Configuration: {e}")
print()

# 5. Verificar API Keys
print("5️⃣ Verificando API Keys...")
try:
    db_path = Path(__file__).parent / 'saas' / 'db.sqlite3'
    
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_exchangeapikey'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) FROM users_exchangeapikey WHERE is_active = 1")
            count = cursor.fetchone()[0]
            
            if count > 0:
                check_ok(f"API Keys configuradas ({count} ativa)")
                
                # Mostrar detalhes (sem expor as keys)
                cursor.execute("""
                    SELECT exchange, is_testnet, is_active 
                    FROM users_exchangeapikey 
                    WHERE is_active = 1
                """)
                for row in cursor.fetchall():
                    testnet = "TESTNET" if row[1] else "PRODUÇÃO"
                    print(f"   🔑 {row[0]} | {testnet}")
            else:
                check_fail("Nenhuma API Key ativa!")
                check_info("Adicione em: http://localhost:8001/api-keys/")
        
        conn.close()
except Exception as e:
    check_warning(f"Não foi possível verificar API Keys: {e}")
print()

# 6. Verificar Trades executados
print("6️⃣ Verificando Trades...")
try:
    db_path = Path(__file__).parent / 'saas' / 'db.sqlite3'
    
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trades'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) FROM trades")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM trades WHERE status = 'open'")
            abertos = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM trades WHERE status = 'closed'")
            fechados = cursor.fetchone()[0]
            
            if total > 0:
                check_ok(f"Trades executados: {total} (Abertos: {abertos}, Fechados: {fechados})")
            else:
                check_fail("ZERO trades executados!")
                check_warning("Bot nunca fez nenhum trade")
        
        conn.close()
except Exception as e:
    check_warning(f"Não foi possível verificar Trades: {e}")
print()

# RESUMO E DIAGNÓSTICO
print("=" * 60)
print("📊 RESUMO DO DIAGNÓSTICO")
print("=" * 60)
print()

# Análise inteligente
problemas = []

# Verificar Django
try:
    requests.get('http://localhost:8001', timeout=2)
except:
    problemas.append("Django não está rodando")

# Verificar Redis
try:
    import redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
except:
    problemas.append("Redis não está rodando")

# Verificar Celery
try:
    result = subprocess.run(
        ['powershell', '-Command', 'Get-Process | Select-String "celery"'],
        capture_output=True,
        text=True,
        timeout=5
    )
    if not (result.stdout and 'celery' in result.stdout.lower()):
        problemas.append("Celery Worker não está rodando")
except:
    problemas.append("Celery Worker não verificado")

if problemas:
    print(f"{Colors.FAIL}🚨 PROBLEMAS ENCONTRADOS:{Colors.END}")
    print()
    for i, problema in enumerate(problemas, 1):
        print(f"   {i}. {problema}")
    print()
    print(f"{Colors.WARNING}📋 PRÓXIMOS PASSOS:{Colors.END}")
    print()
    print("   1. Corrija os problemas acima")
    print("   2. Leia: DIAGNOSTICO_BOT_NAO_TRADE.md")
    print("   3. Execute o checklist completo")
    print("   4. Aguarde 5-30 minutos após corrigir")
    print()
else:
    print(f"{Colors.OK}✅ Sistema parece estar funcionando!{Colors.END}")
    print()
    print(f"{Colors.INFO}💡 Se ainda não tem trades:{Colors.END}")
    print()
    print("   1. Aguarde 5-30 minutos (condições de mercado)")
    print("   2. Verifique logs do Celery Worker")
    print("   3. Verifique se Bot Configuration está correto")
    print()

print("=" * 60)
print("🔍 Diagnóstico completo!")
print("=" * 60)

