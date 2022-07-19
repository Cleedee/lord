import random
from functools import reduce
from collections import UserList
from urllib.parse import urlparse

from rich.console import Console
from rich.table import Table
from rich.markup import escape

from lord import repository as rep
from lord import loader, utils
from lord.packs import CENARIOS_CONJUNTOS

class Carta():
    def __init__(self, nome, text='', traits='', number=0, type_code='ally', **kwargs):
        self.nome = nome
        self.texto =  utils.remover_tags(text) if text else ''
        self.atributos= traits
        self.numero = number
        self.tipo = type_code
        self.virado = False
        self.anexos = []

    def virar(self):
        self.virado = True

    def __repr__(self):
        return self.nome

class CartaJogador(Carta):
    def __init__(self, nome, sphere_code='', **kwargs):
        super().__init__(nome, **kwargs)
        self.esfera = sphere_code

    @property
    def is_neutral(self):
        return True if self.esfera == 'neutral' else False

    @property
    def is_leadership(self):
        return True if self.esfera == 'leadership' else False
    
    @property
    def is_lore(self):
        return True if self.esfera == 'lore' else False

    @property
    def is_spirit(self):
        return True if self.esfera == 'spirit' else False

    @property
    def is_tactics(self):
        return True if self.esfera == 'tactics' else False

    @property
    def is_baggins(self):
        return True if self.esfera == 'baggins' else False


class Hero(CartaJogador):
    def __init__(self, nome, threat=10, willpower=2, attack=1, 
        defense=1, health=1,
        **kwargs):
        super().__init__(nome, **kwargs)
        self.custo_ameaça = threat
        self.força_vontade = willpower
        self.ataque = attack
        self.defesa = defense
        self.pontos_vida = health
        self.recursos = 0
        self.dano = 0

    def adicionar_recurso(self):
        self.recursos += 1

    def __repr__(self):
        console = Console()
        table = Table(show_header=False, show_lines=True)
        table.add_row(f'[bold]Nome:[/] {self.nome} ({self.custo_ameaça}) {self.esfera}')
        table.add_row(f'[bold]Atributos:[/] {self.atributos}')
        texto = f'FV: {self.força_vontade} A: {self.ataque} D: {self.defesa} PV: {self.pontos_vida}\n'
        texto += f'Dano: {self.dano}'
        table.add_row(texto)
        table.add_row(f'{escape(self.texto)}')
        console.print(table)
        return ''


class Acessorio(CartaJogador):

    def __init__(self, nome, cost=1, **kwargs):
        super().__init__(nome, **kwargs)
        self.custo = cost

    def __str__(self):

        console = Console()
        table = Table(show_header=False, show_lines=True)
        table.add_row(f'[bold]Nome:[/] {self.nome} ({self.custo}) {self.tipo}')
        table.add_row(f'[bold]Esfera:[/] {self.esfera}')
        table.add_row(f'[bold]Atributos:[/] {self.atributos}')
        table.add_row(f'{escape(self.texto)}')
        console.print(table)
        return ''


class Aliado(CartaJogador):

    def __init__(self, nome, cost=1, willpower=1, attack=1, defense=1,
        health=1,
        **kwargs):
        super().__init__(nome, **kwargs)
        self.custo = cost
        self.força_vontade = willpower
        self.ataque = attack
        self.defesa = defense
        self.pontos_vida = health
        self.dano = 0

    def __str__(self):
        console = Console()
        table = Table(show_header=False, show_lines=True)
        table.add_row(f'[bold]Nome:[/] {self.nome} ({self.custo}) {self.tipo}')
        table.add_row(f'[bold]Esfera:[/] {self.esfera}')
        texto = f'FV: {self.força_vontade} A: {self.ataque} D: {self.defesa} PV: {self.pontos_vida}'
        table.add_row(texto)
        table.add_row(f'Dano: {self.dano}')
        table.add_row(f'[bold]Atributos:[/] {self.atributos}')
        table.add_row(f'{escape(self.texto)}')
        console.print(table)
        return ''


class Evento(CartaJogador):
    def __init__(self, nome, cost=1, **kwargs):
        super().__init__(nome, **kwargs)
        self.custo = cost

    def __str__(self):
        console = Console()
        table = Table(show_header=False, show_lines=True)
        table.add_row(f'[bold]Nome:[/] {self.nome} ({self.custo}) {self.tipo}')
        table.add_row(f'[bold]Esfera:[/] {self.esfera}')
        table.add_row(f'[bold]Atributos:[/] {self.atributos}')
        table.add_row(f'{escape(self.texto)}')
        console.print(table)
        return ''

# Player Side Quest
class MissaoParalela(CartaJogador):

    def __init__(self, nome, cost=1, victory=0, quest=1, **kwargs):
        super().__init__(nome, **kwargs)
        self.custo = cost
        self.vitoria = victory
        self.pontos_missao = quest

    def __repr__(self):
        console = Console()
        table = Table(show_header=False, show_lines=True)
        table.add_row(f'[bold]Nome:[/] {self.nome} ({self.custo}) {self.tipo}')
        table.add_row(f'[bold]Atributos:[/] {self.atributos}')

        table.add_row(f'[bold]Pontos de Missão:[/] {self.pontos_missao}')
        table.add_row(f'{escape(self.texto)}')
        table.add_row(f'[bold]Vitória:[/] {self.vitoria}')
        console.print(table)
        return ''


class CartaCenario(Carta):
    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)
        self.força_ameaça = 0

    @property
    def is_location(self):
        return True if self.tipo == 'location' else False

    @property
    def is_enemy(self):
        return True if self.tipo == 'enemy' else False

    @property
    def is_treachery(self):
        return True if self.tipo == 'treachery' else False

    @property
    def is_objective(self):
        return True if self.tipo == 'objective' else False

    @property
    def is_objective_ally(self):
        return True if self.tipo == 'objective_ally' else False

class Mission(CartaCenario):
    def __init__(self, nome, sequence='1', quest_points=1, **kwargs):
        super().__init__(nome, **kwargs)
        self.sequencia = int(float(sequence))
        self.pontos_missao = quest_points

    def __str__(self):
        console = Console()
        table = Table(show_header=False, show_lines=True)
        table.add_row(f'[bold]{self.nome}[/] ({self.tipo})')
        table.add_row(f'[bold]Pontos de Missão:[/] {self.pontos_missao}')
        table.add_row(f'{escape(self.texto)}')

        console.print(table)
        return ''            

class Localidade(CartaCenario):
    def __init__(self, nome, threat='', quest_points='', victory='', encounter_set='',
        shadow='', **kwargs):
        super().__init__(nome, **kwargs)
        self.força_ameaça = threat
        self.pontos_missao = quest_points
        self.vitoria = victory
        self.conjunto_encontro = encounter_set
        self.efeito_sombrio = shadow

    def __str__(self):
        console = Console()
        table = Table(show_header=False, show_lines=True)
        table.add_row(f'[bold]{self.nome}[/] ({self.tipo})')

        texto = ''
        texto += f'[bold]Força de Ameaça:[/] {self.força_ameaça} [bold]Pontos de Missão:[/] {self.pontos_missao}\n'
        texto += f'[bold]Pontos de Vitória:[/] {self.vitoria}\n'
        texto += f'[bold]Atributos:[/] {self.atributos}\n'

        table.add_row(texto)
        table.add_row(f'{escape(self.texto)}')

        if self.efeito_sombrio:
            table.add_row(f'[bold]Efeito Sombrio:[/] {self.efeito_sombrio}')
        console.print(table)
        return ''            
    

class Infortunio(CartaCenario):
    def __init__(self, nome, encounter_set='', shadow='', **kwargs):
        super().__init__(nome, **kwargs)
        self.conjunto_encontro = encounter_set
        self.efeito_sombrio = shadow

    def __str__(self):
        console = Console()
        table = Table(show_header=False, show_lines=True)
        table.add_row(f'[bold]{self.nome}[/] ({self.tipo})')
        table.add_row(f'[bold]Atributos:[/] {self.atributos}')
        table.add_row(f'{escape(self.texto)}')


        if self.efeito_sombrio:
            table.add_row(f'[bold]Efeito Sombrio:[/] {self.efeito_sombrio}')
        console.print(table)
        return ''                    

class Objetivo(CartaCenario):
    def __init__(self, nome, encounter_set='', shadow='', **kwargs):
        super().__init__(nome, **kwargs)
        self.conjunto_encontro = encounter_set
        self.efeito_sombrio = shadow

    def __str__(self):
        console = Console()
        table = Table(show_header=False, show_lines=True)
        table.add_row(f'[bold]{self.nome}[/] ({self.tipo})')
        table.add_row(f'[bold]Atributos:[/] {self.atributos}')
        table.add_row(f'{escape(self.texto)}')

        console.print(table)
        return ''

class ObjetivoAliado(CartaCenario):
    def __init__(self, nome, willpower=0, attack=0, defense=0, health=1, **kwargs):
        super().__init__(nome, **kwargs)
        self.força_vontade = willpower
        self.ataque = attack
        self.defesa = defense
        self.pontos_vida = health
        self.dano = 0


class Inimigo(CartaCenario):
    def __init__(self, nome, engage=20, threat=1, attack=1, defense=1,
        health=1, encounter_set='', shadow='', **kwargs):
        super().__init__(nome, **kwargs)
        self.custo_engajamento = engage
        self.força_ameaça = int(threat)
        self.ataque = attack
        self.defesa = defense
        self.pontos_vida = health
        self.conjunto_encontro = encounter_set
        self.efeito_sombrio = shadow
        self.dano = 0

    def __str__(self):
        console = Console()
        table = Table(show_header=False, show_lines=True)
        table.add_row(f'[bold]{self.nome}[/] ({self.tipo})')

        texto = ''
        texto += f'[bold]Custo de Engajamento:[/] {self.custo_engajamento}\n'
        texto += f'FA: {self.força_ameaça} A: {self.ataque} D: {self.defesa} PV: {self.pontos_vida}\n'
        texto += f'[bold]Dano:[/] {self.dano}\n'
        texto += f'[bold]Atributos:[/] {self.atributos}'

        table.add_row(texto)

        table.add_row(f'{escape(self.texto)}')
        if self.efeito_sombrio:
            table.add_row(f'[bold]Efeito Sombrio:[/] {self.efeito_sombrio}')
        console.print(table)
        return ''

class Baralho():
    def __init__(self):
        self.cartas = []

    def __repr__(self):
        if len(self.cartas) > 10:
            return super().__repr__()
        repr = ''
        for carta in self.cartas:
            repr += f'{carta.nome}\n'
        return repr        

    @property
    def total(self):
        return len(self.cartas)

    def nova_carta(self, carta: Carta):
        self.cartas.append(carta)

    def retirar(self, nome_carta):
        return next((self.cartas.pop(i) for i, l in enumerate(self.cartas) if l.nome == nome_carta), None)

    def procurar_cartas_por_nome(self, nome):
        return [carta for carta in self.cartas if carta.nome == nome]

    def comprar(self):
        return self.cartas.pop()

class Area(Baralho):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        repr = ''
        for carta in self.cartas:
            repr += f'{carta.nome}\n'
        return repr

class AreaAmeaça(Area):
    def __init__(self, jogo=None):
        super().__init__()
        self.jogo = jogo

    def mover_para_localizacao_ativa(self, nome):
        print(f'{nome} agora é a localização ativa.')
        return self.jogo.mover_carta(nome, Jogo.AREA_DE_AMEACA,Jogo.LOCALIZACAO_ATIVA)

    def mover_para_descarte(self, nome):
        print(f'{nome} foi descartada.')
        return self.jogo.mover_carta(nome, Jogo.AREA_DE_AMEACA,Jogo.DESCARTE_ENCONTRO)

class DeckEncontro(Baralho):
    def __init__(self, jogo=None):
        super().__init__()
        self.jogo = jogo

    def mover_para_area_de_ameaça(self, nome):
        print(f'{nome} foi adicionada à área de ameaça.')
        return self.jogo.mover_carta(nome, Jogo.DECK_DE_ENCONTRO,Jogo.AREA_DE_AMEACA)

    def mover_para_descarte(self, nome):
        print(f'{nome} foi descartada.')
        return self.jogo.mover_carta(nome, Jogo.DECK_DE_ENCONTRO,Jogo.DESCARTE_ENCONTRO)

    def mover_para_fora_do_jogo(self, nome):
        print(f'{nome} foi posta fora do jogo.')
        return self.jogo.mover_carta(nome, Jogo.DECK_DE_ENCONTRO,Jogo.FORA_DO_JOGO)

    def embaralhar(self):
        print('Deck embaralhado.')
        random.shuffle(self.cartas)

class DeckDeMissao(Baralho):
    def __init__(self, jogo=None):
        super().__init__()
        self.jogo = jogo

    def cartas_da_sequencia(self, sequencia):
        encontradas = []
        for carta in self.cartas:
            if carta.sequencia == sequencia:
                encontradas.append(carta)
        return encontradas

class ForaDoJogo(Area):
    def __init__(self, jogo=None):
        super().__init__()
        self.jogo = jogo

    def mover_para_deck_de_encontro(self, nome):
        print(f'{nome} foi colocada na área de ameaça.')
        return self.jogo.mover_carta(nome, Jogo.FORA_DO_JOGO, Jogo.DECK_DE_ENCONTRO)

class Mão(UserList):
    def index(self, valor):
        for count, value in enumerate(self.data):
            if value.nome == valor:
                return count
        else:
            raise ValueError

class Jogador():
    def __init__(self, nome = 'Jogador 1'):
        self.nome = nome
        self.deck_de_jogador = None
        self.deck_de_herois = None
        # espaço de jogo
        self.hand = Mão()
        self.deck_de_compra = None
        self.deck_de_descarte = None
        self.descarte = Baralho()
        self.herois_em_jogo = Area()
        self.mesa = Area()
        self.jogo: Jogo = None
        self.total_ameaça = 0

    def usar_decks(self, deck_de_herois, deck_de_jogador):
        self.deck_de_herois = deck_de_herois
        self.deck_de_jogador = deck_de_jogador
        self.herois_em_jogo = Baralho()
        self.herois_em_jogo.cartas = self.deck_de_herois.cartas[:]
        self.deck_de_compra = Baralho()
        self.deck_de_compra.cartas = self.deck_de_jogador.cartas[:]
        self.total_ameaça = self.ameaça_inicial


    @property
    def leadership(self):
        total = 0
        for heroi in self.herois_em_jogo.cartas:
            if heroi.is_leadership:
                total += heroi.recursos
        return total

    @property
    def lore(self):
        total = 0
        for heroi in self.herois_em_jogo.cartas:
            if heroi.is_lore:
                total += heroi.recursos
        return total

    @property
    def spirit(self):
        total = 0
        for heroi in self.herois_em_jogo.cartas:
            if heroi.is_spirit:
                total += heroi.recursos
        return total

    @property
    def tactics(self):
        total = 0
        for heroi in self.herois_em_jogo.cartas:
            if heroi.is_tactics:
                total += heroi.recursos
        return total

    @property
    def mão(self):
        return self.hand

    def _posicao_na_mao(self, posicao):
        carta = self.hand[posicao - 1]
        print(carta)

    @property
    def h1(self):
        self._posicao_na_mao(1)

    @property
    def h2(self):
        self._posicao_na_mao(2)

    @property
    def h3(self):
        self._posicao_na_mao(3)

    @property
    def h4(self):
        self._posicao_na_mao(4)

    @property
    def h5(self):
        self._posicao_na_mao(5)

    @property
    def h6(self):
        self._posicao_na_mao(6)

    @property
    def h7(self):
        self._posicao_na_mao(7)

    @property
    def hfim(self):
        quantidade = len(self.hand)
        self._posicao_na_mao(quantidade)

    def h(self, posicao):
        self._posicao_na_mao(posicao)

    @property
    def ameaça_inicial(self):
        return sum(h.custo_ameaça for h in self.deck_de_herois.cartas)

    def embaralhar_deck(self):
        random.shuffle(self.deck_de_compra.cartas)

    def comprar_mão_inicial(self):
        if self.jogo.jogador_inicial:
            self.hand = Mão(self.deck_de_compra.cartas[0:6])
            self.deck_de_compra.cartas = self.deck_de_compra.cartas[6:]
        elif len(self.jogo.jogadores) == 1:
            self.jogo.jogador_inicial = self
            self.hand = Mão(self.deck_de_compra.cartas[0:6])
            self.deck_de_compra.cartas = self.deck_de_compra.cartas[6:]
        else:
            print('Antes, determine o jogador inicial.')

    def comprar(self):
        self.hand.extend(self.deck_de_compra.cartas[0:1])
        self.deck_de_compra.cartas = self.deck_de_compra.cartas[1:]

    def adicionar_recursos(self):
        for heroi in self.herois_em_jogo.cartas:
            heroi.adicionar_recurso()

    def jogar(self, nome_carta):
        pos = self.hand.index(nome_carta)
        carta = self.hand.pop(pos)
        if not carta:
            raise Exception
        self.mesa.nova_carta( carta )

    def pagar_de(self, heroi, quantidade):
        for count, value in enumerate( self.herois_em_jogo.cartas):
            if value.nome == heroi:
                self.herois_em_jogo.cartas[count].recursos -= quantidade
                break

    @property
    def recursos(self):
        console = Console()
        table = Table(show_header=False)
        table.add_column('Esfera')
        table.add_column('Valor')
        table.add_row('Leadership', str(self.leadership))
        table.add_row('Lore', str(self.lore))
        table.add_row('Spirit', str(self.spirit))
        table.add_row('Tactics', str(self.tactics))
        console.print(table)
        return ''

    def _herois_em_linha(self):
        texto = ''
        for heroi in self.herois_em_jogo.cartas:
            texto += f'{heroi.nome} ({heroi.recursos}) '
        return texto

    def __repr__(self):
        console = Console()
        table = Table(show_header=False, header_style="bold magenta")
        table.add_column("Campo")
        table.add_column("Valor")
        table.add_row('Jogador', str(self.nome))
        table.add_row('Ameaça', str(self.total_ameaça))
        table.add_row('Pontos de Vitória', '0')
        table.add_row('Jogador Inicial', 'Sim' if self.jogo.jogador_inicial == self else 'Não')
        table.add_row('Herois', self._herois_em_linha())
        console.print(table)
        return ''


class Jogo():
    DECK_DE_ENCONTRO = 'DECK_DE_ENCONTRO'
    DECK_DE_MISSAO = 'DECK_DE_MISSAO'
    FORA_DO_JOGO = 'FORA_DO_JOGO'
    AREA_DE_AMEACA = 'AREA_DE_AMEACA'
    LOCALIZACAO_ATIVA = 'LOCALIZACAO_ATIVA'
    DESCARTE_ENCONTRO = 'DESCARTE_ENCONTRO'

    def __init__(self, colecao = None):
        self.jogadores = []
        self.nome_cenario = ''
        self.locais = {
            Jogo.DECK_DE_ENCONTRO : DeckEncontro(self),
            Jogo.DECK_DE_MISSAO : DeckDeMissao(self),
            Jogo.DESCARTE_ENCONTRO: Baralho(),
            Jogo.FORA_DO_JOGO : ForaDoJogo(self),
            Jogo.AREA_DE_AMEACA : AreaAmeaça(self),
            Jogo.LOCALIZACAO_ATIVA : Area()
        }
        self.jogador_inicial = None
        self.missao_atual = None
        self.colecao = colecao
        

    def __repr__(self):
        console = Console()
        table = Table('Áreas', show_header=False, show_lines=True, min_width=100)
        if self.missao_atual:
            table.add_row(f'MISSÃO: {self.missao_atual.nome} [{self.missao_atual.sequencia}]')
        else:
            table.add_row(f'MISSÃO: ')
        table.add_row(f'ÁREA DE AMEAÇA ({self.força_ameaça})')
        texto_area_ameaca = ''
        for carta in self.area_de_ameaca.cartas:
            texto_area_ameaca += f'\t{carta.nome} ({carta.tipo})\n'
            for anexo in carta.anexos:
                texto_area_ameaca += f'\t\t{anexo.nome} ({anexo.tipo})\n'
        table.add_row(texto_area_ameaca)
        table.add_row('LOCALIZAÇÃO ATIVA')
        texto_localizacao_ativa = ''
        for carta in self.localizacao_ativa.cartas:
            texto_localizacao_ativa += f'\t{carta.nome}\n'
            for anexo in carta.anexos:
                texto_localizacao_ativa += f'\t\t{anexo.nome} ({anexo.tipo})\n'
        table.add_row(texto_localizacao_ativa)
        table.add_row('CARTAS FORA DE JOGO')
        texto_fora_jogo = ''
        for carta in self.fora_do_jogo.cartas:
            texto_fora_jogo += f'\t{carta.nome} ({carta.tipo})\n'
        table.add_row(texto_fora_jogo)
        console.print(table)
        return ''

    @property
    def força_ameaça(self):
        total = 0
        for carta in self.area_de_ameaca.cartas:
            total += int(carta.força_ameaça) if carta.força_ameaça.isdigit() else 0
            for anexo in carta.anexos:
                total += anexo.força_ameaça
        return total

    @property
    def deck_de_missao(self):
        return self.locais[Jogo.DECK_DE_MISSAO]

    @deck_de_missao.setter
    def deck_de_missao(self, d):
        self.locais[Jogo.DECK_DE_MISSAO] = d

    @property
    def deck_de_encontro(self):
        return self.locais[Jogo.DECK_DE_ENCONTRO]

    @deck_de_encontro.setter
    def deck_de_encontro(self, d):
        self.locais[Jogo.DECK_DE_ENCONTRO] = d

    @property
    def fora_do_jogo(self):
        return self.locais[Jogo.FORA_DO_JOGO]

    @fora_do_jogo.setter
    def fora_do_jogo(self, a):
        self.locais[Jogo.FORA_DO_JOGO] = a

    @property
    def area_de_ameaca(self):
        return self.locais[Jogo.AREA_DE_AMEACA]

    @area_de_ameaca.setter
    def area_de_ameaca(self, a):
        self.locais[Jogo.AREA_DE_AMEACA] = a

    @property
    def localizacao_ativa(self):
        return self.locais[Jogo.LOCALIZACAO_ATIVA]

    @localizacao_ativa.setter
    def localizacao_ativa(self, a):
        self.locais[Jogo.LOCALIZACAO_ATIVA] = a

    def novo_jogador(self, nome):
        novo = Jogador(nome)
        novo.jogo = self
        self.jogadores.append(novo)
        return novo

    @property
    def jogador1(self):
        return self.jogadores[0] if self.jogadores else None

    @property
    def jogador2(self):
        return self.jogadores[1] if self.jogadores and len(self.jogadores) > 1 else None

    def escolher_cenario(self,nome, deck_de_missao, deck_de_encontro):
        self.nome_cenario = nome
        self.deck_de_missao = deck_de_missao
        self.deck_de_encontro = deck_de_encontro

    def mover_carta(self, nome_carta, origem, destino):
        deck_origem = self.locais[origem]
        deck_destino = self.locais[destino]
        carta = deck_origem.retirar(nome_carta)
        deck_destino.nova_carta(carta)
        return carta

    def comprar(self):
        carta = self.deck_de_encontro.comprar()
        self.area_de_ameaca.cartas.append(carta)
        print(f'{carta.nome} foi adicionada à Área de Ameaça.')
        if carta.is_treachery:
            print(f'{carta.nome} é um infortúnio. Resolva.')
        return carta

    def embaralhar_deck_encontro(self):
        random.shuffle(self.deck_de_encontro.cartas)

    def setup(self):
        preparacao = CENARIOS_CONJUNTOS[self.nome_cenario]['setup']
        preparacao(self)
        q1 = self.deck_de_missao.cartas_da_sequencia(1)[0]
        self.missao_atual = q1

    def prepara_jogador(self, nome, codigo_deck):
        jogador = self.novo_jogador(nome)
        jogador.usar_decks(*self.colecao.pegar_deck_jogador(codigo_deck))
        return jogador

    def enfrentar_cenario(self, nome_cenario):
        self.nome_cenario = nome_cenario
        d1, d2 = loader.carregar_deck_cenario(nome_cenario)
        self.deck_de_missao = d1
        self.deck_de_encontro = d2
        self.deck_de_encontro.jogo = self
        self.embaralhar_deck_encontro()

    def ler(self, nome):
        encontradas = []
        for carta in self.area_de_ameaca.cartas:
            if nome in carta.nome:
                encontradas.append(carta)
            for anexo in carta.anexos:
                if nome in anexo.nome:
                    encontradas.append(anexo)
        for carta in self.fora_do_jogo.cartas:
            if nome in carta.nome:
                encontradas.append(carta)
        for carta in self.localizacao_ativa.cartas:
            if nome in carta.nome:
                encontradas.append(carta)                
        for jogador in self.jogadores:
            for heroi in jogador.herois_em_jogo.cartas:
                if nome in heroi.nome:
                    encontradas.append(heroi)
            for carta in jogador.mesa.cartas:
                if nome in carta.nome:
                    encontradas.append(carta)
            for carta in jogador.mão:
                if nome in carta.nome:
                    encontradas.append(carta)
        if self.missao_atual and nome in self.missao_atual.nome:
            encontradas.append(self.missao_atual)
        for encontrada in encontradas:
            print(encontrada)

class Colecao():

    def __init__(self):
        self.decks = rep.encontra_decks()

    def __repr__(self):
        console = Console()
        table = Table('Código', 'Nome', show_header=False, show_lines=True)
        for deck in self.decks:
            table.add_row(str(deck.id), deck.name)
        console.print(table)
        return ''

    def cenarios(self):
        return list(CENARIOS_CONJUNTOS.keys())

    def pegar_deck_jogador(self, codigo):
        return loader.carregar_deck(codigo)

    def baixar_deck_jogador(self, url):
        partes = urlparse(url)
        codigo = partes.path.strip('/').split('/')[2]
        rep.salva_deck(codigo)

    def atualizar_lista_decks(self):
        self.decks = rep.encontra_decks()