from rich.console import Console
from rich.table import Table


from lord import Colecao, Jogo, Jogador

colecao = Colecao()
jogo = Jogo(colecao)

console = Console()

table = Table(show_header=True, header_style="bold magenta")

table.add_column("Mensagem")
table.add_row("Objetos para usar: colecao, jogo")
table.add_row("Instancie jogadores com nome_jogador = jogo.preparar_jogador('Nome Jogador', codigo_deck)")
table.add_row("Embaralhe o deck: nome_jogador.embaralhar_deck()")
table.add_row("Comprar mão inicial: nome_jogador.comprar_mão_inicial()")
table.add_row("Escolha o cenário: jogo.enfrentar_cenario('nome do cenário')")

console.print(table)