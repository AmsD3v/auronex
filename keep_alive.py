"""
Monitor que mantém Django e Streamlit SEMPRE rodando
Reinicia automaticamente se cair
"""
import subprocess
import time
import requests
import os
import signal

def is_django_running():
    try:
        response = requests.get('http://localhost:8001', timeout=2)
        return True
    except:
        return False

def is_streamlit_running():
    try:
        response = requests.get('http://localhost:8501', timeout=2)
        return True
    except:
        return False

def start_django():
    print("🔷 Iniciando Django...")
    subprocess.Popen(
        ['python', 'manage.py', 'runserver', '8001'],
        cwd=r'I:\Robo\saas',
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    time.sleep(5)

def start_streamlit():
    print("📊 Iniciando Streamlit...")
    subprocess.Popen(
        ['streamlit', 'run', 'dashboard_master.py', '--server.port', '8501'],
        cwd=r'I:\Robo',
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    time.sleep(5)

print("="*50)
print("  🤖 ROBOTRADER - Monitor Keep-Alive")
print("="*50)
print()
print("Monitorando servidores a cada 10 segundos...")
print("Pressione Ctrl+C para parar")
print()

# Iniciar tudo
if not is_django_running():
    start_django()
else:
    print("✅ Django já rodando")

time.sleep(3)

if not is_streamlit_running():
    start_streamlit()
else:
    print("✅ Streamlit já rodando")

print()
print("Monitor ativo! Servidores serão reiniciados se caírem.")
print()

# Loop de monitoramento
while True:
    try:
        # Verificar Django
        if not is_django_running():
            print("❌ Django caiu! Reiniciando...")
            start_django()
        
        # Verificar Streamlit
        if not is_streamlit_running():
            print("❌ Streamlit caiu! Reiniciando...")
            start_streamlit()
        
        time.sleep(10)  # Verifica a cada 10 segundos
        
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor parado pelo usuário.")
        break
    except Exception as e:
        print(f"⚠️ Erro no monitor: {e}")
        time.sleep(10)

