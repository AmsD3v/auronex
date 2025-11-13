"""
Sincronizar versão entre backend e frontend
"""

# Ler VERSION.txt
with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

print(f"Versão atual: {version}")

# Atualizar .env do React
with open('auronex-dashboard/.env', 'r') as f:
    env_lines = f.readlines()

new_lines = []
found = False
for line in env_lines:
    if line.startswith('NEXT_PUBLIC_VERSION'):
        new_lines.append(f'NEXT_PUBLIC_VERSION={version}\n')
        found = True
    else:
        new_lines.append(line)

if not found:
    new_lines.append(f'NEXT_PUBLIC_VERSION={version}\n')

with open('auronex-dashboard/.env', 'w') as f:
    f.writelines(new_lines)

print(f"✅ Versão sincronizada: {version}")
print("Frontend e Backend agora na mesma versão!")

