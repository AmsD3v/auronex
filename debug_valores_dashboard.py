"""Debug: Por que mostra R$ 1.227,60?"""

capital_usd = 46.40
lucro_usd = 49.31
cotacao_real = 5.29

print("="*70)
print("  DEBUG VALORES DASHBOARD")
print("="*70)
print()

print(f"Capital USD: ${capital_usd}")
print(f"Lucro USD: ${lucro_usd}")
print(f"Cotação REAL: R$ {cotacao_real}")
print()

print("CONVERSÕES CORRETAS:")
print(f"  Capital BRL: ${capital_usd} × {cotacao_real} = R$ {capital_usd * cotacao_real:.2f}")
print(f"  Lucro BRL: ${lucro_usd} × {cotacao_real} = R$ {lucro_usd * cotacao_real:.2f}")
print()

print("VALORES ERRADOS POSSIVEIS:")
print(f"  Lucro × 5 × 5: ${lucro_usd} × 5 × 5 = R$ {lucro_usd * 5 * 5:.2f}")
print(f"  Capital × 5: ${capital_usd} × 5 = R$ {capital_usd * 5:.2f}")
print(f"  Lucro × Capital: ${lucro_usd} × ${capital_usd} = R$ {lucro_usd * capital_usd:.2f}")
print()

print("="*70)
print("VALORES CORRETOS:")
print(f"  Capital: R$ {capital_usd * cotacao_real:.2f}")
print(f"  Lucro: R$ {lucro_usd * cotacao_real:.2f}")
print(f"  Total: R$ {(capital_usd + lucro_usd) * cotacao_real:.2f}")
print("="*70)

