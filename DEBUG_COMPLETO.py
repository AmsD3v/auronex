"""Debug completo - Ver EXATAMENTE o que esta no banco"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration, User

db = SessionLocal()

print("="*70)
print("  DEBUG COMPLETO - BANCO DE DADOS")
print("="*70)
print()

# TODOS os bots
bots = db.query(BotConfiguration).all()
print(f"TODOS OS BOTS ({len(bots)}):")
for b in bots:
    print(f"  Bot {b.id}: {b.name} ({b.exchange})")
    print(f"    Ativo: {b.is_active}")
    print(f"    Symbols: {b.symbols}")
    print(f"    Capital: ${b.capital}")
    print()

# Bots ATIVOS
ativos = db.query(BotConfiguration).filter(BotConfiguration.is_active == True).all()
print(f"BOTS ATIVOS ({len(ativos)}):")
for b in ativos:
    print(f"  Bot {b.id}: {b.name}")
    print(f"    Exchange: {b.exchange}")
    print(f"    Symbols: {b.symbols}")
    print(f"    Capital: ${b.capital}")
    print()

# Usuario 74
user = db.query(User).filter(User.id == 74).first()
print(f"USUARIO 74:")
print(f"  Email: {user.email}")
print(f"  first_name: '{user.first_name}'")
print(f"  last_name: '{user.last_name}'")
print(f"  Vazio: {not user.first_name or user.first_name.strip() == ''}")
print()

db.close()

print("="*70)
print("CONCLUSAO:")
print("  Se bot ativo tem symbols errados -> corrigir no banco")
print("  Se user.first_name vazio -> API deve retornar email")
print("="*70)

