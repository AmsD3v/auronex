#!/bin/bash

# ========================================
# ROBOTRADER - DEPLOY BOT
# Execute como usuário bottrader
# ========================================

set -e

echo "🚀 ROBOTRADER - Deploy Bot"
echo "============================"
echo ""

# Verificar se NÃO é root
if [ "$EUID" -eq 0 ]; then 
   echo "❌ NÃO execute como root! Use: ./deploy-bot.sh"
   exit 1
fi

# Variáveis
PROJECT_DIR="$HOME/robotrader"
VENV_DIR="$PROJECT_DIR/venv"

# 1. VENV
echo "[1/8] Criando ambiente virtual..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
fi
source $VENV_DIR/bin/activate

# 2. DEPENDÊNCIAS
echo "[2/8] Instalando dependências..."
pip install --upgrade pip
pip install -r $PROJECT_DIR/requirements.txt
pip install gunicorn psycopg2-binary

# 3. .ENV
echo "[3/8] Verificando .env..."
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo "❌ Crie o arquivo .env primeiro!"
    echo "Copie .env.example e preencha os valores"
    exit 1
fi

# 4. MIGRATIONS
echo "[4/8] Executando migrations..."
cd $PROJECT_DIR/saas
python manage.py migrate

# 5. STATIC
echo "[5/8] Coletando static files..."
python manage.py collectstatic --noinput

# 6. SUPERUSER (se não existir)
echo "[6/8] Verificando superuser..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@robotrader.com', 'TROCAR_SENHA_ADMIN')
    print("Superuser 'admin' criado!")
EOF

# 7. SYSTEMD SERVICES
echo "[7/8] Criando systemd services..."

# Django
sudo tee /etc/systemd/system/django-bot.service > /dev/null << EOF
[Unit]
Description=RoboTrader Django
After=network.target postgresql.service

[Service]
Type=notify
User=bottrader
Group=bottrader
WorkingDirectory=$PROJECT_DIR/saas
Environment="PATH=$VENV_DIR/bin"
Environment="DJANGO_SETTINGS_MODULE=saas.settings"
ExecStart=$VENV_DIR/bin/gunicorn \
    --workers 3 \
    --bind unix:$PROJECT_DIR/gunicorn.sock \
    --access-logfile /var/log/django-bot/access.log \
    --error-logfile /var/log/django-bot/error.log \
    --log-level info \
    saas.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Streamlit
sudo tee /etc/systemd/system/streamlit-bot.service > /dev/null << EOF
[Unit]
Description=RoboTrader Streamlit Dashboard
After=network.target django-bot.service

[Service]
Type=simple
User=bottrader
Group=bottrader
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/streamlit run dashboard_master.py \
    --server.port 8501 \
    --server.address 127.0.0.1 \
    --server.headless true

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Celery Worker
sudo tee /etc/systemd/system/celery-bot.service > /dev/null << EOF
[Unit]
Description=Celery Worker for Trading Bot
After=network.target redis.service

[Service]
Type=forking
User=bottrader
Group=bottrader
WorkingDirectory=$PROJECT_DIR/saas
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/celery -A saas worker \
    --loglevel=info \
    --logfile=/var/log/celery-bot/worker.log \
    --pidfile=/var/run/celery-bot/worker.pid

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Celery Beat
sudo tee /etc/systemd/system/celerybeat-bot.service > /dev/null << EOF
[Unit]
Description=Celery Beat Scheduler
After=network.target redis.service

[Service]
Type=simple
User=bottrader
Group=bottrader
WorkingDirectory=$PROJECT_DIR/saas
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/celery -A saas beat \
    --loglevel=info \
    --logfile=/var/log/celery-bot/beat.log \
    --pidfile=/var/run/celery-bot/beat.pid

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 8. ATIVAR SERVIÇOS
echo "[8/8] Ativando serviços..."
sudo systemctl daemon-reload
sudo systemctl enable django-bot streamlit-bot celery-bot celerybeat-bot
sudo systemctl start django-bot streamlit-bot celery-bot celerybeat-bot

echo ""
echo "=========================================="
echo "✅ DEPLOY CONCLUÍDO!"
echo "=========================================="
echo ""
echo "📊 STATUS DOS SERVIÇOS:"
sudo systemctl status django-bot --no-pager | grep Active
sudo systemctl status streamlit-bot --no-pager | grep Active
sudo systemctl status celery-bot --no-pager | grep Active
sudo systemctl status celerybeat-bot --no-pager | grep Active
echo ""
echo "⚠️  PRÓXIMOS PASSOS:"
echo "1. Configurar Nginx: sudo vim /etc/nginx/sites-available/robotrader"
echo "2. Ativar site: sudo ln -s /etc/nginx/sites-available/robotrader /etc/nginx/sites-enabled/"
echo "3. Testar Nginx: sudo nginx -t"
echo "4. Reiniciar Nginx: sudo systemctl restart nginx"
echo "5. Obter SSL: sudo certbot --nginx -d seudominio.com"
echo ""
echo "📝 LOGS:"
echo "Django: sudo journalctl -u django-bot -f"
echo "Streamlit: sudo journalctl -u streamlit-bot -f"
echo "Celery: tail -f /var/log/celery-bot/worker.log"



