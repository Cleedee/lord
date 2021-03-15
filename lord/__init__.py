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

class Deck():
    def __init__(self):
        self.cartas = []

    @property
    def total(self):
        return len(self.cartas)

    def nova_carta(self, carta):
        self.cartas.append(carta)

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
        self.herois_em_jogo = None
        self.mesa = []

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
        self.mesa.append( carta )

    def pagar_de(self, heroi, quantidade):
        for count, value in enumerate( self.herois_em_jogo.cartas):
            if value.nome == heroi:
                self.herois_em_jogo.cartas[count].recursos -= quantidade
                break


class Jogo():
    def __init__(self):
        self.jogadores = []
        self.nome_cenario = ''
        self.deck_de_missao = None
        self.deck_de_encontro = None

    def novo_jogador(self, nome):
        self.jogadores.append(Jogador(nome))

    @property
    def jogador1(self):
        return self.jogadores[0] if self.jogadores else None

    def escolher_cenario(self,nome, deck_de_missao, deck_de_encontro):
        self.nome_cenario = nome
        self.deck_de_missao = deck_de_missao
        self.deck_de_encontro = deck_de_encontro
