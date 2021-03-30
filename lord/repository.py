from .scrap import pegar_deck_jogador, pegar_carta_jogador
from .database import Card, Deck, Slot, db

def encontra_carta(codigo):
    return Card.get_or_none(code = codigo)

def encontra_deck(codigo_deck):
    return Deck.get_or_none(id = codigo_deck)

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
        print('SLOTS')
        for slot in deck['slots']:
            print(slot)
            c = encontra_carta(slot)
            if not c:
                carta = pegar_carta_jogador(slot)
                c = Card.create(**carta)
            slot = Slot.create(
                slot_type=Slot.SLOT_SLOTS,
                deck = d,
                card = c,
                quantity = deck['slots'][slot]
            )
        print('SIDESLOTS')
        for slot in deck['sideslots']:
            print(slot)
            c = encontra_carta(slot)
            if not c:
                carta = pegar_carta_jogador(slot)
                c = Card.create(**carta)
            slot = Slot.create(
                slot_type=Slot.SLOT_SIDESLOTS,
                deck = d,
                card = c,
                quantity = deck['sideslots'][slot]
            )
        print('HEROES')
        for slot in deck['heroes']:
            print(slot)
            c = encontra_carta(slot)
            if not c:
                carta = pegar_carta_jogador(slot)
                c = Card.create(**carta)
            slot = Slot.create(
                slot_type=Slot.SLOT_HEROES,
                deck = d,
                card = c,
                quantity = deck['heroes'][slot]
            )
    return True

def salva_card(carta):
    if not encontra_carta(carta['code']):
        c = Card(**carta)
        c.save()
        return True
    return False
