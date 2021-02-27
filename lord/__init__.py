
class Card():
    def __init__(self, nome):
        self.nome = nome
        self.virado = False

    def virar(self):
        self.virado = True

class Hero(Card):
    ...

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

class Jogador():
    def __init__(self, nome = 'Jogador 1'):
        self.nome = nome
        self.hand = []
        self.espaço_herois = []
        self.deck = None

    def usar_deck(self, deck):
        self.deck = deck
    
    @property
    def mão(self):
        return self.hand

    def separar(self):
        self.deck.separar()
        self.espaço_herois.extend(self.deck.herois)

class Jogo():
    def __init__(self):
        self.jogadores = []

    def novo_jogador(self, nome):
        self.jogadores.append(Jogador(nome))

    @property
    def jogador1(self):
        return self.jogadores[0] if self.jogadores else None 