#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar SECRET_KEY para JWT
Execute: python scripts/generate_secret_key.py
"""

import secrets
import sys
import io

# Fix encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*70)
print("  GERADOR DE SECRET_KEY PARA JWT")
print("="*70)
print()
print("Gerando chave aleatoria (32 bytes hex)...")
print()

# Gerar 32 bytes aleatórios em hexadecimal
secret_key = secrets.token_hex(32)

print("[OK] SECRET_KEY gerada com sucesso!")
print()
print("Adicione ao seu .env:")
print()
print(f"SECRET_KEY={secret_key}")
print()
print("="*70)
print("[ATENCAO]")
print("- NUNCA compartilhe esta chave")
print("- NUNCA commite no Git")
print("- Use .env ou variavel de ambiente")
print("="*70)
print()






