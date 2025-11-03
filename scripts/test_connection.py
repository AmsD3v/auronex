"""
Script para testar conexão com a Binance
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.exchange import BinanceExchange
from config.settings import Settings
from rich.console import Console
from rich.table import Table

console = Console()


def test_connection():
    """Testa conexão com Binance"""
    console.print("\n[bold cyan]Testando Conexao com Binance...[/bold cyan]\n")
    
    settings = Settings()
    
    # Mostrar modo
    mode = "TESTNET" if settings.USE_TESTNET else "PRODUCAO"
    console.print(f"Modo: [bold]{mode}[/bold]\n")
    
    try:
        # Criar exchange
        exchange = BinanceExchange()
        
        # Testar conexão
        success, message = exchange.test_connection()
        
        if success:
            console.print(f"[bold green]{message}[/bold green]")
            
            # Mostrar informações detalhadas
            balance = exchange.get_balance()
            ticker = exchange.get_ticker(settings.TRADING_SYMBOL)
            
            # Tabela de saldos
            table = Table(title="Saldos Disponiveis")
            table.add_column("Moeda", style="cyan")
            table.add_column("Livre", style="green")
            table.add_column("Bloqueado", style="yellow")
            table.add_column("Total", style="blue")
            
            for coin in ['USDT', 'BTC', 'ETH', 'BNB']:
                if coin in balance:
                    free = balance[coin]['free']
                    used = balance[coin]['used']
                    total = balance[coin]['total']
                    
                    if total > 0:
                        table.add_row(
                            coin,
                            f"{free:.8f}",
                            f"{used:.8f}",
                            f"{total:.8f}"
                        )
            
            console.print("\n")
            console.print(table)
            
            # Informações de mercado
            if ticker:
                console.print(f"\n[bold]{settings.TRADING_SYMBOL}[/bold]")
                console.print(f"Último Preço: [green]${ticker['last']:,.2f}[/green]")
                console.print(f"24h High: [green]${ticker['high']:,.2f}[/green]")
                console.print(f"24h Low: [red]${ticker['low']:,.2f}[/red]")
                console.print(f"24h Volume: [blue]{ticker['baseVolume']:,.2f}[/blue]")
            
            console.print("\n[bold green]Conexao estabelecida com sucesso![/bold green]\n")
            return True
            
        else:
            console.print(f"[bold red]{message}[/bold red]\n")
            return False
            
    except Exception as e:
        console.print(f"[bold red]❌ Erro: {str(e)}[/bold red]\n")
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

