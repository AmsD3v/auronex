# Script para adicionar rota de logout se não existir

print("Verificando se precisa adicionar rota de logout...")
print("Se não tiver, adicione no final de fastapi_app/routers/pages.py:")
print("""
@router.get("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    '''Logout do usuário'''
    
    # Verificar se era admin
    user = get_current_user_from_cookie(request, db)
    
    # Se era admin, volta para login do admin
    if user and (user.is_staff or user.is_superuser):
        response = RedirectResponse(url="/login?next=/admin/", status_code=303)
    else:
        # Usuário comum vai para landing page
        response = RedirectResponse(url="/", status_code=303)
    
    response.delete_cookie("access_token")
    return response
""")



