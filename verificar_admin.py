from fastapi_app.database import get_db
from fastapi_app.models import User

db = next(get_db())

# Buscar admin
admin = db.query(User).filter(User.email == 'admin@robotrader.com').first()

if admin:
    print(f"Admin encontrado: ID {admin.id}")
    print(f"is_staff: {admin.is_staff}")
    print(f"is_superuser: {admin.is_superuser}")
    
    if not admin.is_staff or not admin.is_superuser:
        print("\nCORRIGINDO permissoes...")
        admin.is_staff = True
        admin.is_superuser = True
        db.commit()
        print("[OK] Admin corrigido!")
    else:
        print("[OK] Admin ja tem permissoes corretas")
else:
    print("Admin nao encontrado!")
    print("Criando admin...")
    
    from fastapi_app.auth import get_password_hash
    from datetime import datetime
    
    new_admin = User(
        username='admin',
        email='admin@robotrader.com',
        password=get_password_hash('admin123'),
        first_name='Admin',
        last_name='Auronex',
        is_staff=True,
        is_superuser=True,
        is_active=True,
        date_joined=datetime.utcnow()
    )
    
    db.add(new_admin)
    db.commit()
    print("[OK] Admin criado!")




