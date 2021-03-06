from . import Deck, Card, Hero
from . import repository as rep
from . import database

def carrega_deck_jogador(codigo):
    deck = rep.encontra_deck(codigo)
    if not deck: return
    deck_jogo = Deck()
    cards_player = rep.encontra_slots(database.Slot.SLOT_SLOTS, deck.id)
    for slot in cards_player:
        for i in range(slot.quantity):
            deck_jogo.nova_carta(Card(slot.card.name))
    return deck_jogo

def carregar_deck_herois(codigo):
    deck = rep.encontra_deck(codigo)
    if not deck: return
    deck_jogo = Deck()
    cards_hero = rep.encontra_slots(database.Slot.SLOT_HEROES, deck.id)
    for slot in cards_hero:
        for i in range(slot.quantity):
            deck_jogo.nova_carta(Hero(slot.card.name, slot.card.threat))
    return deck_jogo
