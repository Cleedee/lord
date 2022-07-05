import lord
from . import repository as rep
from . import database

def carrega_deck_jogador(codigo):
    deck = rep.encontra_deck(codigo)
    if not deck: return
    deck_jogo = lord.Baralho()
    cards_player = rep.encontra_slots(database.Slot.SLOT_SLOTS, deck.id)
    for slot in cards_player:
        for i in range(slot.quantity):
            deck_jogo.nova_carta(lord.CartaJogador(
                slot.card.name, 
                texto=slot.card.text,
                esfera=slot.card.sphere_code,
                custo=slot.card.cost,
                atributos=slot.card.traits
                )
            )
    return deck_jogo

def carregar_deck_herois(codigo):
    deck = rep.encontra_deck(codigo)
    if not deck: return
    deck_jogo = lord.Baralho()
    cards_hero = rep.encontra_slots(database.Slot.SLOT_HEROES, deck.id)
    for slot in cards_hero:
        for i in range(slot.quantity):
            deck_jogo.nova_carta(lord.Hero(
                slot.card.name, 
                slot.card.threat,
                slot.card.willpower,
                slot.card.attack,
                slot.card.defense,
                slot.card.health,
                texto=slot.card.text, 
                esfera=slot.card.sphere_code,
                atributos=slot.card.traits))
    return deck_jogo

def carregar_deck(codigo):
    deck_herois = carregar_deck_herois(codigo)
    deck_jogador = carrega_deck_jogador(codigo)
    return (deck_herois, deck_jogador)

def carregar_deck_cenario(nome):
    deck_missao = lord.Baralho()
    deck_encontro = lord.Baralho()
    cartas = []
    for conjunto in database.CENARIOS_CONJUNTOS[nome]:
        cartas.extend(rep.encontra_cartas_conjunto_por_nome(conjunto))
    for carta in cartas:
        if carta.type_code == 'quest':
            deck_missao.nova_carta(lord.Mission(carta.name, texto_frente = carta.text))
        else:
            for i in range(int(float(carta.count))):
                deck_encontro.nova_carta(lord.Carta(carta.name))
    print(deck_missao.total)
    print(deck_encontro.total)
    return (deck_missao, deck_encontro)
