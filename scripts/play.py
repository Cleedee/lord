from rich.console import Console
from rich.table import Table


from lord import Colecao, Jogo, Jogador

colecao = Colecao()
jogo = Jogo(colecao)

console = Console()

table = Table(show_header=True, header_style="bold magenta")

table.add_column("Mensagem")
table.add_row("Objetos para usar: colecao, jogo")

console.print(table)