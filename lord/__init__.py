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
        self.herois = []
        self.cartas = []

    @property
    def total(self):
        return len(self.cartas)

    def nova_carta(self, carta):
        self.cartas.append(carta)

    def separar(self):
        h = []
        c = []
        for carta in self.cartas:
            if isinstance(carta, Hero):
                h.append(carta)
            else:
                c.append(carta)
        self.herois = h
        self.cartas = c

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
        self.hand = Mão()
        self.espaço_herois = []
        self.deck = None
        self.mesa = []

    def usar_deck(self, deck):
        self.deck = deck
    
    @property
    def mão(self):
        return self.hand

    @property
    def ameaça(self):
        return sum(h.custo_ameaça for h in self.espaço_herois)
        #return reduce((lambda x, y: x.custo_ameaça + y.custo_ameaça), self.espaço_herois)

    def separar(self):
        self.deck.separar()
        self.espaço_herois.extend(self.deck.herois)

    def embaralhar_deck(self):
        random.shuffle(self.deck.cartas)

    def comprar_mão_inicial(self):
        self.hand = Mão(self.deck.cartas[0:6])
        self.deck.cartas = self.deck.cartas[6:]

    def comprar(self):
        self.hand.extend(self.deck.cartas[0:1])
        self.deck.cartas = self.deck.cartas[1:]

    def adicionar_recursos(self):
        for heroi in self.espaço_herois:
            heroi.adicionar_recurso()

    def jogar(self, nome_carta):
        pos = self.hand.index(nome_carta)
        print(pos)
        carta = self.hand.pop(pos)
        if not carta:
            raise Exception
        self.mesa.append( carta )

    def pagar_de(self, heroi, quantidade):
        for count, value in enumerate( self.espaço_herois):
            if value.nome == heroi:
                self.espaço_herois[count].recursos -= quantidade
                break


class Jogo():
    def __init__(self):
        self.jogadores = []

    def novo_jogador(self, nome):
        self.jogadores.append(Jogador(nome))

    @property
    def jogador1(self):
        return self.jogadores[0] if self.jogadores else None 