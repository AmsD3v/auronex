"""
Executar bot diretamente: python -m bot ID_DO_BOT
"""
import sys
import asyncio

if len(sys.argv) < 2:
    print("Uso: python -m bot BOT_ID")
    print("Exemplo: python -m bot 38")
    sys.exit(1)

bot_id = int(sys.argv[1])

from bot.main_enterprise_async import TradingBotEnterpriseAsync

async def main():
    bot = TradingBotEnterpriseAsync(bot_id)
    
    if not bot.load_config():
        print("Erro ao carregar config")
        return
    
    if not await bot.initialize_components_async():
        print("Erro ao inicializar")
        return
    
    await bot.run_async()

if __name__ == "__main__":
    asyncio.run(main())

