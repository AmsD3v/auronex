"""
Views para controle do sistema (servidores, processos)
"""
import subprocess
import os
import signal
import psutil
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt


def system_control_page(request):
    """Página de controle do sistema"""
    return render(request, 'system_control.html')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_servers_status(request):
    """Verificar status dos servidores"""
    
    django_running = False
    streamlit_running = False
    
    # Verificar Django (porta 8001)
    for conn in psutil.net_connections():
        if conn.laddr.port == 8001 and conn.status == 'LISTEN':
            django_running = True
            break
    
    # Verificar Streamlit (porta 8501)
    for conn in psutil.net_connections():
        if conn.laddr.port == 8501 and conn.status == 'LISTEN':
            streamlit_running = True
            break
    
    return JsonResponse({
        'django': {
            'running': django_running,
            'url': 'http://localhost:8001',
            'port': 8001
        },
        'streamlit': {
            'running': streamlit_running,
            'url': 'http://localhost:8501',
            'port': 8501
        }
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
@csrf_exempt
def start_streamlit(request):
    """Iniciar servidor Streamlit"""
    try:
        # Verificar se já está rodando
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if 'streamlit' in str(proc.info.get('cmdline', [])).lower():
                return JsonResponse({
                    'success': False,
                    'message': 'Streamlit já está rodando!'
                })
        
        # Iniciar Streamlit em background
        import sys
        python_exe = sys.executable
        streamlit_path = os.path.join(os.path.dirname(python_exe), 'Scripts', 'streamlit.exe')
        dashboard_path = os.path.join(os.path.dirname(__file__), '..', '..', 'dashboard_master.py')
        
        subprocess.Popen(
            [streamlit_path, 'run', dashboard_path, '--server.port', '8501', '--server.headless', 'true'],
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Streamlit iniciado com sucesso!',
            'url': 'http://localhost:8501'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao iniciar Streamlit: {str(e)}'
        })


@api_view(['POST'])
@permission_classes([IsAdminUser])
@csrf_exempt
def stop_streamlit(request):
    """Parar servidor Streamlit"""
    try:
        killed = False
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if 'streamlit' in str(proc.info.get('cmdline', [])).lower():
                proc.kill()
                killed = True
        
        if killed:
            return JsonResponse({
                'success': True,
                'message': 'Streamlit parado com sucesso!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Streamlit não estava rodando'
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao parar Streamlit: {str(e)}'
        })


@api_view(['POST'])
@permission_classes([IsAdminUser])
@csrf_exempt
def restart_streamlit(request):
    """Reiniciar servidor Streamlit"""
    try:
        # Parar
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if 'streamlit' in str(proc.info.get('cmdline', [])).lower():
                proc.kill()
        
        import time
        time.sleep(2)  # Aguardar processo terminar
        
        # Iniciar
        import sys
        python_exe = sys.executable
        streamlit_path = os.path.join(os.path.dirname(python_exe), 'Scripts', 'streamlit.exe')
        dashboard_path = os.path.join(os.path.dirname(__file__), '..', '..', 'dashboard_master.py')
        
        subprocess.Popen(
            [streamlit_path, 'run', dashboard_path, '--server.port', '8501', '--server.headless', 'true'],
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Streamlit reiniciado com sucesso!',
            'url': 'http://localhost:8501'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao reiniciar Streamlit: {str(e)}'
        })




