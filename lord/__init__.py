import random
from functools import reduce
from collections import UserList

class Card():
    def __init__(self, nome):
        self.nome = nome
        self.virado = False

    def virar(self):
        self.virado = True

    def __repr__(self):
        return self.nome

class Hero(Card):
    def __init__(self, nome, custo_ameaça):
        super().__init__(nome)
        self.custo_ameaça = custo_ameaça
        self.recursos = 0

    def adicionar_recurso(self):
        self.recursos += 1

class Mission(Card):
    def __init__(self, nome, texto_frente = '', texto_verso = ''):
        super().__init__(nome)
        self.texto_frente = texto_frente
        self.texto_verso = texto_verso

class Location(Card):
    def __init__(self, nome, força_ameaça, pontos_missao, vitoria = 0):
        super().__init__(nome)
        self.força_ameaça = força_ameaça
        self.pontos_missao = pontos_missao
        self.vitoria = vitoria

class Deck():
    def __init__(self):
        self.cartas = []

    @property
    def total(self):
        return len(self.cartas)

    def nova_carta(self, carta: Card):
        self.cartas.append(carta)

    def retirar(self, nome_carta):
        return next((self.cartas.pop(i) for i, l in enumerate(self.cartas) if l.nome == nome_carta), None)

    def procurar_cartas_por_nome(self, nome):
        return [carta for carta in self.cartas if carta.nome == nome]

class Area(Deck):
    def __init__(self):
        super().__init__()

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

    def usar_decks(self, deck_de_herois, deck_de_jogador):
        self.deck_de_herois = deck_de_herois
        self.deck_de_jogador = deck_de_jogador
        self.herois_em_jogo = Deck()
        self.herois_em_jogo.cartas = self.deck_de_herois.cartas[:]
        self.deck_de_compra = Deck()
        self.deck_de_compra.cartas = self.deck_de_jogador.cartas[:]

    @property
    def mão(self):
        return self.hand

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
        print(pos)
        carta = self.hand.pop(pos)
        if not carta:
            raise Exception
        self.mesa.nova_carta( carta )

    def pagar_de(self, heroi, quantidade):
        for count, value in enumerate( self.herois_em_jogo.cartas):
            if value.nome == heroi:
                self.herois_em_jogo.cartas[count].recursos -= quantidade
                break


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
            Jogo.DECK_DE_ENCONTRO : Deck(),
            Jogo.DECK_DE_MISSAO : Deck(),
            Jogo.FORA_DO_JOGO : Area(),
            Jogo.AREA_DE_AMEACA : Area(),
            Jogo.LOCALIZACAO_ATIVA : Area()
        }

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
        self.jogadores.append(Jogador(nome))

    @property
    def jogador1(self):
        return self.jogadores[0] if self.jogadores else None

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
