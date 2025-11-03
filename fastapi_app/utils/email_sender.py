"""
Sistema de envio de emails
Em produção, usar SMTP real (Gmail, SendGrid, etc)
"""
import secrets

def send_password_reset_email(email: str, reset_link: str):
    """
    Enviar email de recuperação de senha
    
    Em PRODUÇÃO, configure:
    - SMTP_HOST = 'smtp.gmail.com'
    - SMTP_PORT = 587
    - SMTP_USER = 'seu-email@gmail.com'
    - SMTP_PASSWORD = 'sua-senha-app'
    
    E use:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    msg = MIMEMultipart()
    msg['From'] = 'noreply@auronex.com.br'
    msg['To'] = email
    msg['Subject'] = 'Recuperação de Senha - Auronex'
    
    body = f'''
    Olá!
    
    Recebemos uma solicitação para redefinir sua senha.
    
    Clique no link abaixo para criar uma nova senha:
    {reset_link}
    
    Este link expira em 1 hora.
    
    Se você não solicitou, ignore este email.
    
    Atenciosamente,
    Equipe Auronex
    '''
    
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()
    """
    
    # SIMULAÇÃO (localhost)
    print("=" * 60)
    print("📧 EMAIL DE RECUPERAÇÃO DE SENHA")
    print("=" * 60)
    print(f"Para: {email}")
    print(f"Assunto: Recuperação de Senha - Auronex")
    print()
    print("Corpo:")
    print("-" * 60)
    print(f"""
Olá!

Recebemos uma solicitação para redefinir sua senha no Auronex Robô Trader.

Clique no link abaixo para criar uma nova senha:

{reset_link}

⏰ Este link expira em 1 hora.

Se você não solicitou esta redefinição, ignore este email.
Sua senha permanecerá inalterada.

Atenciosamente,
Equipe Auronex Robô Trader
    """)
    print("-" * 60)
    print()
    print("✅ Em PRODUÇÃO, este email seria enviado via SMTP!")
    print("=" * 60)
    
    return True

def generate_reset_token():
    """Gerar token seguro para reset"""
    return secrets.token_urlsafe(32)



