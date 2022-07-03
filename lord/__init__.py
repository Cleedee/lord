import random
from functools import reduce
from collections import UserList

from lord import repository as rep
from lord import loader

class Carta():
    def __init__(self, nome, esfera='neutral', custo=1, texto=''):
        self.nome = nome
        self.esfera = esfera
        self.custo = custo
        self.texto = texto
        self.virado = False

    def virar(self):
        self.virado = True

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

    def __repr__(self):
        return self.nome

class Hero(Carta):
    def __init__(self, nome, custo_ameaça, esfera='neutral', custo=1, texto=''):
        super().__init__(nome, esfera, custo, texto)
        self.custo_ameaça = custo_ameaça
        self.recursos = 0

    def adicionar_recurso(self):
        self.recursos += 1

class Mission(Carta):
    def __init__(self, nome, texto_frente = '', texto_verso = ''):
        super().__init__(nome)
        self.texto_frente = texto_frente
        self.texto_verso = texto_verso

class Localidade(Carta):
    def __init__(self, nome, força_ameaça, pontos_missao, vitoria = 0):
        super().__init__(nome)
        self.força_ameaça = força_ameaça
        self.pontos_missao = pontos_missao
        self.vitoria = vitoria

class Baralho():
    def __init__(self):
        self.cartas = []

    def __repr__(self):
        if len(self.cartas) > 10:
            return super().__repr__(self)
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

class Area(Baralho):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        repr = ''
        for carta in self.cartas:
            repr += f'{carta.nome}\n'
        return repr


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
        self.total_ameaça = self.ameaça

    @property
    def mão(self):
        return self.hand

    def _posicao_na_mao(self, posicao):
        carta = self.hand[posicao - 1]
        texto = f'{carta.nome} ({carta.custo})\n'
        texto += f'Esfera: {carta.esfera}\n\n'
        texto += f'{carta.texto}'
        print(texto)
        return texto

    @property
    def h1(self):
        texto = self._posicao_na_mao(1)
        return texto

    @property
    def h2(self):
        texto = self._posicao_na_mao(2)
        return texto

    @property
    def h3(self):
        texto = self._posicao_na_mao(3)
        return texto

    @property
    def h4(self):
        texto = self._posicao_na_mao(4)
        return texto

    @property
    def h5(self):
        texto = self._posicao_na_mao(5)
        return texto

    @property
    def h6(self):
        texto = self._posicao_na_mao(6)
        return texto

    @property
    def h7(self):
        texto = self._posicao_na_mao(7)
        return texto

    @property
    def hfim(self):
        quantidade = len(self.hand)
        texto = self._posicao_na_mao(quantidade)
        return texto

    @property
    def ameaça(self):
        return sum(h.custo_ameaça for h in self.herois_em_jogo.cartas)
        #return reduce((lambda x, y: x.custo_ameaça + y.custo_ameaça), self.espaço_herois)

    def embaralhar_deck(self):
        random.shuffle(self.deck_de_compra.cartas)

    def comprar_mão_inicial(self):
        self.hand = Mão(self.deck_de_compra.cartas[0:6])
        self.deck_de_compra.cartas = self.deck_de_compra.cartas[6:]

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
        leadership = lore = spirit = tactics = 0
        for heroi in self.herois_em_jogo.cartas:
            if heroi.is_leadership:
                leadership += heroi.recursos
            if heroi.is_lore:
                lore += heroi.recursos
            if heroi.is_spirit:
                spirit += heroi.recursos
            if heroi.is_tactics:
                tactics += heroi.recursos
        texto = ''
        texto += f'Leadership: {leadership}\n'
        texto += f'Lore: {lore}\n'
        texto += f'Spirit: {spirit}\n'
        texto += f'Tactics: {tactics}'
        print(texto)
        return texto

    def _herois_em_linha(self):
        texto = ''
        for heroi in self.herois_em_jogo.cartas:
            texto += f'{heroi.nome} ({heroi.recursos}) '
        return texto

    def __repr__(self):
        texto = '-------------------\n'
        texto += f'Jogador: {self.nome}\n'
        texto += f'Ameaça: {self.total_ameaça}\n'
        texto += f'Pontos de Vitória: 0\n'
        texto += f'Primeiro jogador: Sim\n'
        texto += f'Herois: {self._herois_em_linha()}\n'
        texto += '-------------------'
        return texto


class Jogo():
    DECK_DE_ENCONTRO = 'DECK_DE_ENCONTRO'
    DECK_DE_MISSAO = 'DECK_DE_MISSAO'
    FORA_DO_JOGO = 'FORA_DO_JOGO'
    AREA_DE_AMEACA = 'AREA_DE_AMEACA'
    LOCALIZACAO_ATIVA = 'LOCALIZACAO_ATIVA'

    def __init__(self):
        self.jogadores = []
        self.nome_cenario = ''
        self.locais = {
            Jogo.DECK_DE_ENCONTRO : Baralho(),
            Jogo.DECK_DE_MISSAO : Baralho(),
            Jogo.FORA_DO_JOGO : Area(),
            Jogo.AREA_DE_AMEACA : Area(),
            Jogo.LOCALIZACAO_ATIVA : Area()
        }
        self.primeiro_jogador = None

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
        print('Carta:', carta.nome)
        deck_destino.nova_carta(carta)

class Colecao():

    def __init__(self):
        self.decks = rep.encontra_decks()

    def __repr__(self):
        repr = ''
        for deck in self.decks:
            repr += f'{deck.id}) {deck.name}\n'
        return repr

    def pegar_deck_jogador(self, codigo):
        return loader.carregar_deck(codigo)