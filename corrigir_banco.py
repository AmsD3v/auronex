"""Adicionar colunas novas ao banco"""
import sqlite3

db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()

print("Adicionando colunas...")

try:
    cursor.execute("ALTER TABLE bot_configurations ADD COLUMN is_testnet BOOLEAN DEFAULT 1")
    print("[OK] is_testnet adicionada")
except:
    print("[OK] is_testnet ja existe")

try:
    cursor.execute("ALTER TABLE bot_configurations ADD COLUMN analysis_interval INTEGER DEFAULT 5")
    print("[OK] analysis_interval adicionada")
except:
    print("[OK] analysis_interval ja existe")

try:
    cursor.execute("ALTER TABLE bot_configurations ADD COLUMN hunter_mode BOOLEAN DEFAULT 0")
    print("[OK] hunter_mode adicionada")
except:
    print("[OK] hunter_mode ja existe")

db.commit()
db.close()

print("\n[OK] Banco atualizado!")
print("\nTestar: http://localhost:8001/bots-page")
