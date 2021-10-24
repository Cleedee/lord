
from typing import List
import re

from lord.database import Slot, Deck, Game
from lord.scrap import pegar_carta_jogador
import lord.repository as rep

TAG_RE = re.compile(r'<[^>]+>')

def somente_aliados(slots: List[Slot]) -> List[Slot]:
    return [s for s in slots if s.card.is_ally]

def somente_acessorios(slots: List[Slot]) -> List[Slot]:
    return [s for s in slots if s.card.is_attachment]

def somente_eventos(slots: List[Slot]) -> List[Slot]:
    return [s for s in slots if s.card.is_event]

def somente_contratos(slots: List[Slot]) -> List[Slot]:
    return [s for s in slots if s.card.is_contract]

def somente_tesouros(slots: List[Slot]) -> List[Slot]:
    return [s for s in slots if s.card.is_treasure]

def remover_tags(texto):
    return TAG_RE.sub('', texto)

def mostrar_deck(deck: Deck):
    if deck:
        heroes = rep.encontra_slots(Slot.SLOT_HEROES, deck.id)
        cards = rep.encontra_slots(Slot.SLOT_SLOTS, deck.id)
        allies = somente_aliados(cards)
        attachments = somente_acessorios(cards)
        events = somente_eventos(cards)
        contracts = somente_contratos(cards)
        treasures = somente_tesouros(cards)
        total_allies = sum([s.quantity for s in allies])
        total_attachments = sum([s.quantity for s in attachments])
        total_events = sum([c.quantity for c in events])
        total_contracts = sum([c.quantity for c in contracts])
        total_treasures = sum([c.quantity for c in treasures])                    
        total_cards = sum([c.quantity for c in cards])
        print(deck.name)
        print('------')
        print(f'Starting Threat: {deck.starting_threat}')
        print(f'{len(heroes)} Heroes, {total_cards} Cards')
        print()
        print('Heroes')
        for slot in heroes:
            print(f'{slot.card.name}')
        print(f'Contract ({total_contracts})')
        for slot in contracts:
            print(f'{slot.quantity}x {slot.card.name}')
        print(f'Ally ({total_allies})')
        for slot in allies:
            print(f'{slot.quantity}x {slot.card.name}')
        print(f'Attachments ({total_attachments})')
        for slot in attachments:
            print(f'{slot.quantity}x {slot.card.name}')
        print(f'Events ({total_events})')
        for slot in events:
            print(f'{slot.quantity}x {slot.card.name}')
        print(f'Treasure ({total_treasures})')
        for slot in treasures:
            print(f'{slot.quantity}x {slot.card.name}')                        


def opcao_ringsdb(args):
    if args.search:
        codigo = args.search
        salvou = rep.salva_deck(codigo)
        if salvou:
            print('Deck encontrado e salvo.')


def opcao_base(args):
    if args.list:
        if args.decks:
            lista = rep.encontra_decks()
            if lista:
                for index, deck in enumerate(lista):
                    print(f'{index}) {deck.name} ({deck.starting_threat})')
                if args.view is not None:
                    deck = lista[args.view]
                    mostrar_deck(deck)

    if args.search:
        if args.card:
            lista = rep.encontra_carta_por_nome(args.search)
            print(f'Cartas encontradas: {len(lista)}')
            for index, carta in enumerate(lista):
                print(f'{index}) {carta.name} [{carta.type_name},{carta.sphere_code}] ')
            print('------------')
            if args.view is not None:
                carta = lista[args.view]
                if carta.cost is None:
                    c = pegar_carta_jogador(str(carta.code).zfill(5))
                    rep.salva_card(c)
                    carta = rep.encontra_carta(carta.code)
                print(carta.name)
                print(f"{carta.type_name}. Cost: {carta.cost}")
                print(carta.traits)
                print()
                print(remover_tags( carta.text))
                print('------------')
        if args.decks:
            deck = rep.encontra_deck_por_nome(args.search)
            mostrar_deck(deck)

def opcao_play(args):
    if args.new:
        # criar um game
        rep.salva_game(Game())
        print('Jogo criado.')