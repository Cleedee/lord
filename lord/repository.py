from typing import List

from .scrap import pegar_deck_jogador, pegar_carta_jogador
from .database import Card, Deck, Slot, Game, db

def encontra_game_ativo() -> Game:
    return Game.get(Game.active == True)

def encontra_carta_por_nome(nome: str) -> List[Card]:
    return Card.select().where(Card.name.contains(nome))

def encontra_decks():
    return Deck.select()

def encontra_carta(codigo):
    return Card.get_or_none(code = codigo)

def encontra_deck(codigo_deck):
    return Deck.get_or_none(id = codigo_deck)

def encontra_deck_por_nome(nome: str) -> Deck:
    return Deck.get(Deck.name == nome)

def encontra_slots(slot_type, deck_id) -> List[Slot]:
    return Slot.select().where(
        (Slot.slot_type == slot_type) &
        (Slot.deck == deck_id)
    )

def _salva_slot(slot_type, slots, deck):
    for code_card in slots:
        c = encontra_carta(code_card)
        if not c:
            carta = pegar_carta_jogador(code_card)
            c = Card.create(**carta)
        slot = Slot.create(
            slot_type=slot_type,
            deck = deck,
            card = c,
            quantity = slots[code_card]
        )

def salva_deck(codigo_deck):
    if encontra_deck(codigo_deck):
        return False
    deck = pegar_deck_jogador(codigo_deck)
    if not deck:
        return False
    with db.atomic():
        d = Deck.create(
            id = deck['id'],
            name = deck['name'],
            date_creation = deck['date_creation'],
            date_update = deck['date_update'],
            description_md = deck['description_md'],
            user_id = deck['user_id'],
            version = deck['version'],
            is_published = deck['is_published'],
            starting_threat = deck['starting_threat']
        )
        _salva_slot(Slot.SLOT_SLOTS, deck['slots'], d)
        _salva_slot(Slot.SLOT_SIDESLOTS, deck['sideslots'], d)
        _salva_slot(Slot.SLOT_HEROES, deck['heroes'], d)
    return True

def salva_card(carta: dict) -> bool:
    c  = encontra_carta(carta['code'])
    if not c:
        c = Card(**carta)
        c.save()
        return True
    else:
        if c.cost is None:
            # algumas cartas estão sem custo
            if 'cost' in carta.keys():
                c.cost = carta['cost']
                c.save()
                return True
    return False

def salva_game(game: Game) -> bool:
    game.save()
    return True
