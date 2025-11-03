#!/bin/bash

# ========================================
# ROBOTRADER - MONITOR DE SAÚDE
# ========================================

echo "🔍 ROBOTRADER - Monitor de Saúde"
echo "=================================="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Função para verificar serviço
check_service() {
    if systemctl is-active --quiet $1; then
        echo -e "${GREEN}✅ $1 RODANDO${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 PARADO${NC}"
        return 1
    fi
}

# 1. SERVIÇOS
echo "📊 STATUS DOS SERVIÇOS"
echo "======================"
check_service django-bot
check_service streamlit-bot
check_service celery-bot
check_service celerybeat-bot
check_service postgresql
check_service redis-server
check_service nginx
echo ""

# 2. RECURSOS
echo "💾 USO DE RECURSOS"
echo "=================="
echo "Memória:"
free -h | grep -E "Mem|Swap" | awk '{print "  "$1" "$2" / "$3" ("$5")"}'
echo ""
echo "Disco:"
df -h / | tail -1 | awk '{print "  Root: "$3" / "$2" ("$5" usado)"}'
echo ""
echo "CPU Load:"
uptime | awk -F'load average:' '{print "  "$2}'
echo ""

# 3. PROCESSOS PYTHON
echo "🐍 PROCESSOS PYTHON"
echo "==================="
PYTHON_COUNT=$(ps aux | grep python | grep -v grep | wc -l)
echo "  Total: $PYTHON_COUNT processos"
echo ""

# 4. CONEXÕES DE REDE
echo "🌐 CONEXÕES DE REDE"
echo "==================="
CONNECTIONS=$(ss -s | grep "estab" | awk '{print $2}')
echo "  Estabelecidas: $CONNECTIONS"
echo ""

# 5. ÚLTIMOS ERROS
echo "⚠️  ÚLTIMOS ERROS (5 minutos)"
echo "=============================="
echo "Django:"
sudo journalctl -u django-bot --since "5 minutes ago" | grep -i error | tail -3 || echo "  Nenhum erro"
echo ""
echo "Celery:"
sudo tail -20 /var/log/celery-bot/worker.log | grep -i error | tail -3 || echo "  Nenhum erro"
echo ""

# 6. BANCO DE DADOS
echo "🗄️  BANCO DE DADOS"
echo "==================="
DB_SIZE=$(sudo -u postgres psql -d robotrader -tAc "SELECT pg_size_pretty(pg_database_size('robotrader'));")
echo "  Tamanho: $DB_SIZE"
DB_CONNECTIONS=$(sudo -u postgres psql -d robotrader -tAc "SELECT count(*) FROM pg_stat_activity WHERE datname='robotrader';")
echo "  Conexões ativas: $DB_CONNECTIONS"
echo ""

# 7. UPTIME
echo "⏱️  UPTIME"
echo "=========="
uptime -p
echo ""

# 8. CERTIFICADO SSL (se existir)
if [ -f /etc/letsencrypt/live/*/fullchain.pem ]; then
    echo "🔒 CERTIFICADO SSL"
    echo "=================="
    CERT_FILE=$(find /etc/letsencrypt/live -name "fullchain.pem" | head -1)
    EXPIRY=$(openssl x509 -enddate -noout -in "$CERT_FILE" | cut -d= -f2)
    echo "  Expira em: $EXPIRY"
    echo ""
fi

echo "=================================="
echo "✅ Health Check Concluído!"
echo "=================================="
echo ""
echo "📝 Ver logs completos:"
echo "  Django: sudo journalctl -u django-bot -f"
echo "  Streamlit: sudo journalctl -u streamlit-bot -f"
echo "  Celery: tail -f /var/log/celery-bot/worker.log"
echo ""
echo "🔄 Reiniciar serviço:"
echo "  sudo systemctl restart NOME_SERVICO"



