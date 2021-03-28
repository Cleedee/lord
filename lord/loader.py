from . import Deck, Card
from . import scrap

def iterador_de_slots(slots):
    for slot in slots.items(): yield slot

def criar_deck_jogador(slots):
    deck = Deck()
    for codigo, quant in iterador_de_slots(slots):
        # carta_dict = scrap.pegar_carta(f'https://ringsdb.com/card/{codigo}')
        # esse codigo fica pesado para testar
        # usaremos decks salvos no banco de dados
        for i in range(quant):
            deck.nova_carta(Card(codigo))
            #deck.nova_carta(Card(carta_dict['card-name']))
    return deck
