import lord
from . import repository as rep
from . import database
from . import utils
from . import collections
from . import jsonqueries

def carrega_deck_jogador(codigo):
    deck = rep.encontra_deck(codigo)
    if not deck: return
    deck_jogo = lord.Baralho()
    cards_player = rep.encontra_slots(database.Slot.SLOT_SLOTS, deck.id)
    for slot in cards_player:
        ClasseCarta = utils.pegar_classe_da_carta_jogador(slot.card)
        if ClasseCarta is not lord.Hero:
            campos = utils.carta_para_dicionario(slot.card)
            for i in range(slot.quantity):
                deck_jogo.nova_carta(ClasseCarta(slot.card.name, **campos))
    return deck_jogo

def carregar_deck_herois(codigo):
    deck = rep.encontra_deck(codigo)
    if not deck: return
    deck_jogo = lord.Baralho()
    cards_hero = rep.encontra_slots(database.Slot.SLOT_HEROES, deck.id)
    for slot in cards_hero:
        campos = utils.carta_para_dicionario(slot.card)
        for i in range(slot.quantity):
            deck_jogo.nova_carta(lord.Hero(slot.card.name, **campos))
    return deck_jogo

def carregar_deck(codigo):
    deck_herois = carregar_deck_herois(codigo)
    deck_jogador = carrega_deck_jogador(codigo)
    return (deck_herois, deck_jogador)

def carregar_deck_cenario(nome):
    deck_missao = lord.DeckDeMissao()
    deck_encontro = lord.DeckEncontro()
    cartas = []
    for conjunto in collections.CENARIOS_CONJUNTOS[nome]['conjuntos']:
        cartas.extend(jsonqueries.encontra_cartas_conjunto_por_nome(conjunto))
    for carta in cartas:
        if carta['type_code'] == 'quest':
            deck_missao.nova_carta(lord.Mission(carta['name'], **carta))
        else:
            ClasseCarta = utils.pegar_classe_da_carta_cenario(carta)
            for i in range(int(float(carta['count']))):
                deck_encontro.nova_carta(ClasseCarta(carta['name'], **carta))
    return (deck_missao, deck_encontro)
