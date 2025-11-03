"""
Instalar RoboTrader como Serviço do Windows
Executar como Administrador!
"""
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import subprocess
import time
import os


class RoboTraderService(win32serviceutil.ServiceFramework):
    _svc_name_ = "RoboTrader"
    _svc_display_name_ = "RoboTrader SaaS"
    _svc_description_ = "Sistema de Trading Bot Automatizado"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.django_process = None
        self.streamlit_process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        
        # Parar processos
        if self.django_process:
            self.django_process.terminate()
        if self.streamlit_process:
            self.streamlit_process.terminate()

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        # Paths
        robo_dir = r"I:\Robo"
        venv_python = r"I:\Robo\venv\Scripts\python.exe"
        
        # Iniciar Django
        self.django_process = subprocess.Popen(
            [venv_python, "manage.py", "runserver", "8001"],
            cwd=os.path.join(robo_dir, "saas")
        )
        
        time.sleep(5)  # Aguardar Django iniciar
        
        # Iniciar Streamlit
        streamlit_exe = r"I:\Robo\venv\Scripts\streamlit.exe"
        self.streamlit_process = subprocess.Popen(
            [streamlit_exe, "run", "dashboard_master.py", "--server.port", "8501"],
            cwd=robo_dir
        )
        
        # Manter rodando
        while True:
            if win32event.WaitForSingleObject(self.stop_event, 5000) == win32event.WAIT_OBJECT_0:
                break


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(RoboTraderService)


