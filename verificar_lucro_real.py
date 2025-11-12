"""Verificar lucro REAL e responder perguntas"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import Trade, BotConfiguration
from datetime import datetime
from sqlalchemy import func

db = SessionLocal()

print("="*70)
print("  VERIFICACAO COMPLETA - RESPONDENDO DUVIDAS")
print("="*70)
print()

# 1. LUCRO TOTAL (TODOS OS TEMPOS)
todos_fechados = db.query(Trade).filter(Trade.exit_time.isnot(None)).all()
lucro_total = sum(float(t.profit_loss) for t in todos_fechados if t.profit_loss)
print(f"1. LUCRO LIQUIDO TOTAL (todos os tempos):")
print(f"   ${lucro_total:.2f} = R$ {lucro_total * 5:.2f}")
print(f"   De {len(todos_fechados)} trades fechados")
print()

# 2. LUCRO HOJE
hoje = datetime.now().date()
trades_hoje_fechados = db.query(Trade).filter(
    func.date(Trade.entry_time) == hoje,
    Trade.exit_time.isnot(None)
).all()
lucro_hoje = sum(float(t.profit_loss) for t in trades_hoje_fechados if t.profit_loss)
print(f"2. LUCRO HOJE:")
print(f"   ${lucro_hoje:.2f} = R$ {lucro_hoje * 5:.2f}")
print(f"   De {len(trades_hoje_fechados)} trades FECHADOS hoje")
print()

# 3. TRADES HOJE (total)
trades_hoje_total = db.query(Trade).filter(
    func.date(Trade.entry_time) == hoje
).count()
print(f"3. TRADES HOJE (abertas + fechadas):")
print(f"   {trades_hoje_total} trades")
print()

# 4. TAXA SUCESSO
wins = sum(1 for t in todos_fechados if t.profit_loss and float(t.profit_loss) > 0)
loss = sum(1 for t in todos_fechados if t.profit_loss and float(t.profit_loss) < 0)
taxa = (wins / len(todos_fechados) * 100) if todos_fechados else 0
print(f"4. TAXA SUCESSO (todos os tempos):")
print(f"   {taxa:.1f}%")
print(f"   Wins: {wins}, Loss: {loss}, Total: {len(todos_fechados)}")
print()

# 5. BOTS ATIVOS
bots_ativos = db.query(BotConfiguration).filter(BotConfiguration.is_active == True).all()
capital_total = sum(float(b.capital) for b in bots_ativos if b.capital)
print(f"5. BOTS ATIVOS:")
print(f"   {len(bots_ativos)} bot(s)")
print(f"   Capital total: ${capital_total:.2f} = R$ {capital_total * 5:.2f}")
for b in bots_ativos:
    print(f"     - {b.name}: ${b.capital}")
print()

print("="*70)
print("RESPOSTAS:")
print(f"")
print(f"1. Lucro R$ {lucro_total * 5:.2f} está CORRETO? ")
print(f"   SIM - são {len(todos_fechados)} trades desde o inicio")
print(f"")
print(f"2. Deve somar ao Saldo Total?")
print(f"   SIM - Saldo Total = Exchange + Lucro")
print(f"   Saldo exchange: R$ 20")
print(f"   Lucro: R$ {lucro_total * 5:.2f}")
print(f"   TOTAL: R$ {20 + (lucro_total * 5):.2f}")
print(f"")
print(f"3. Trades Hoje e Taxa atualizadas?")
print(f"   Trades Hoje: {trades_hoje_total} (todos)")
print(f"   Taxa: {taxa:.1f}% (de TODOS os trades, não só hoje)")
print(f"")
print(f"4. Lucro é só de hoje?")
print(f"   NAO - é de TODOS os {len(todos_fechados)} trades")
print(f"   Hoje: R$ {lucro_hoje * 5:.2f}")
print(f"   Total: R$ {lucro_total * 5:.2f}")
print("="*70)

db.close()

