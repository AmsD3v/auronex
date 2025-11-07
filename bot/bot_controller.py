"""
Controlador de Bots - Gerencia múltiplos bots simultaneamente
Integração com dashboard web
"""
import threading
import time
import logging
from typing import Dict
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration
from bot.main import TradingBot
from bot.bot_locks import acquire_bot_lock, renew_bot_lock, release_bot_lock, force_clear_expired_locks

logger = logging.getLogger(__name__)


class BotController:
    """Controla múltiplos bots simultaneamente"""
    
    def __init__(self):
        self.active_bots: Dict[int, dict] = {}  # {bot_id: {'bot': obj, 'thread': thread}}
        self.running = False
        
    def start_bot(self, bot_id: int) -> bool:
        """
        Inicia um bot específico
        ✅ COM LOCK - Garante apenas 1 instância!
        
        Args:
            bot_id: ID do bot no banco
            
        Returns:
            True se iniciou com sucesso
        """
        # ✅ VERIFICAR LOCK PRIMEIRO
        if not acquire_bot_lock(bot_id):
            logger.error(f"[BLOQUEADO] Bot {bot_id} JÁ ESTÁ RODANDO em outro processo!")
            logger.error(f"[BLOQUEADO] IMPOSSÍVEL iniciar múltiplas instâncias!")
            return False
        
        if bot_id in self.active_bots:
            logger.warning(f"Bot {bot_id} ja esta rodando neste processo")
            release_bot_lock(bot_id)
            return False
        
        try:
            # Criar instância do bot
            bot = TradingBot(bot_id)
            
            # Carregar config
            if not bot.load_config():
                logger.error(f"Falha ao carregar config do bot {bot_id}")
                return False
            
            # Inicializar componentes
            if not bot.initialize_components():
                logger.error(f"Falha ao inicializar bot {bot_id}")
                return False
            
            # Criar thread
            thread = threading.Thread(target=bot.run, daemon=True)
            
            # Registrar
            self.active_bots[bot_id] = {
                'bot': bot,
                'thread': thread,
                'config': bot.config
            }
            
            # Iniciar
            thread.start()
            
            logger.info(f"[OK] Bot {bot_id} ({bot.config['name']}) iniciado!")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao iniciar bot {bot_id}: {e}")
            return False
    
    def stop_bot(self, bot_id: int) -> bool:
        """
        Para um bot específico
        ✅ Libera lock
        """
        if bot_id not in self.active_bots:
            logger.warning(f"Bot {bot_id} nao esta rodando")
            release_bot_lock(bot_id)  # ✅ Liberar lock mesmo assim
            return False
        
        try:
            bot_data = self.active_bots[bot_id]
            bot_data['bot'].stop()
            
            # Aguardar thread terminar
            bot_data['thread'].join(timeout=5)
            
            # Remover
            del self.active_bots[bot_id]
            
            # ✅ LIBERAR LOCK
            release_bot_lock(bot_id)
            
            logger.info(f"[OK] Bot {bot_id} parado e lock liberado")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao parar bot {bot_id}: {e}")
            return False
    
    def get_bot_status(self, bot_id: int) -> dict:
        """Retorna status de um bot"""
        if bot_id in self.active_bots:
            bot_data = self.active_bots[bot_id]
            return {
                'running': True,
                'name': bot_data['config']['name'],
                'symbols': bot_data['config']['symbols']
            }
        else:
            return {'running': False}
    
    def sync_with_database(self):
        """Sincroniza bots ativos com banco de dados - SÓ INICIA SE USUÁRIO ATIVOU!"""
        try:
            db = SessionLocal()
            
            # Buscar APENAS bots marcados como ATIVOS no banco
            # is_active = True significa que USUÁRIO clicou em START!
            active_in_db = db.query(BotConfiguration).filter(
                BotConfiguration.is_active == True
            ).all()
            
            print(f"[BOT CONTROLLER] Bots marcados como ativos no banco: {len(active_in_db)}")
            for bot in active_in_db:
                print(f"  - Bot {bot.id}: {bot.name} ({bot.exchange})")
            
            active_ids = {b.id for b in active_in_db}
            
            # Parar bots que foram desativados
            for bot_id in list(self.active_bots.keys()):
                if bot_id not in active_ids:
                    logger.info(f"Bot {bot_id} foi DESATIVADO pelo usuario - parando...")
                    self.stop_bot(bot_id)
            
            # Iniciar APENAS bots que usuário ATIVOU explicitamente
            for bot in active_in_db:
                if bot.id not in self.active_bots:
                    logger.info(f"Bot {bot.id} foi ATIVADO pelo usuario - iniciando...")
                    self.start_bot(bot.id)
            
            db.close()
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar: {e}")
    
    def run_controller(self):
        """
        Loop principal do controlador
        ✅ Com limpeza de locks expirados
        """
        logger.info("[OK] Controlador de bots iniciado COM PROTEÇÃO DE LOCKS")
        self.running = True
        
        iteration = 0
        
        try:
            while self.running:
                iteration += 1
                
                # ✅ Limpar locks expirados a cada 30s
                if iteration % 3 == 0:
                    expired = force_clear_expired_locks()
                    if expired > 0:
                        logger.info(f"[LOCK] Limpou {expired} locks expirados")
                
                # Sincronizar com banco a cada 10 segundos
                self.sync_with_database()
                
                # Mostrar status
                logger.info(f"Bots ativos: {len(self.active_bots)}")
                
                # ✅ Renovar locks a cada iteração
                for bot_id in self.active_bots.keys():
                    renew_bot_lock(bot_id)
                
                time.sleep(10)
                
        except KeyboardInterrupt:
            logger.info("Parando controlador...")
        finally:
            # Parar todos os bots
            for bot_id in list(self.active_bots.keys()):
                self.stop_bot(bot_id)


if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    controller = BotController()
    controller.run_controller()


