"""
Configurar Banco de Dados FastAPI
Cria tabelas e primeiro usuário
"""
import sys
from pathlib import Path

print("=" * 70)
print("  CONFIGURACAO DO BANCO DE DADOS FASTAPI")
print("=" * 70)
print()

# 1. Criar todas as tabelas
print("1. Criando tabelas do FastAPI...")
try:
    from fastapi_app.database import engine, Base
    from fastapi_app.models import User, ExchangeAPIKey, BotConfiguration, Trade
    
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    print("   [OK] Tabelas criadas com sucesso!")
    
    # Verificar tabelas
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"   [INFO] Tabelas criadas: {tables}")
    
except Exception as e:
    print(f"   [ERRO] Falha ao criar tabelas: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# 2. Criar primeiro usuário
print("2. Criando primeiro usuario...")
try:
    from fastapi_app.database import get_db
    from fastapi_app.models import User
    from fastapi_app.auth import get_password_hash
    
    db = next(get_db())
    
    # Verificar se já existe
    existing = db.query(User).filter(User.email == "admin@robotrader.com").first()
    
    if existing:
        print("   [INFO] Usuario 'admin@robotrader.com' ja existe")
        print("   [INFO] Atualizando senha...")
        
        # Atualizar senha
        existing.password = get_password_hash("admin123")
        db.commit()
        print("   [OK] Senha atualizada!")
    else:
        # Criar novo
        print("   [INFO] Criando novo usuario...")
        
        user = User(
            username="admin",
            email="admin@robotrader.com",
            password=get_password_hash("admin123"),
            first_name="Admin",
            last_name="RoboTrader",
            is_active=True
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print(f"   [OK] Usuario criado: {user.email} (ID: {user.id})")
    
    print()
    print("CREDENCIAIS DE ACESSO:")
    print("  Email: admin@robotrader.com")
    print("  Senha: admin123")
    
except Exception as e:
    print(f"   [ERRO] Falha ao criar usuario: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# 3. Verificar funcionamento
print("3. Testando autenticacao...")
try:
    from fastapi_app.auth import verify_password, get_password_hash
    
    test_password = "teste123"
    test_hash = get_password_hash(test_password)
    
    is_valid = verify_password(test_password, test_hash)
    
    if is_valid:
        print("   [OK] Sistema de autenticacao funcionando!")
    else:
        print("   [ERRO] Falha na verificacao de senha!")
        sys.exit(1)
        
except Exception as e:
    print(f"   [ERRO] Falha no teste: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 70)
print("  CONFIGURACAO CONCLUIDA COM SUCESSO!")
print("=" * 70)
print()
print("PROXIMOS PASSOS:")
print("1. Execute: INICIAR_FASTAPI.bat")
print("2. Acesse: http://localhost:8501")
print("3. Faca login:")
print("   - Email: admin@robotrader.com")
print("   - Senha: admin123")
print()
print("=" * 70)

