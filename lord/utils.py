
from typing import List
import re
import json

from lord.database import Slot, Deck, Game, Scenario, Card
from lord.scrap import pegar_carta_jogador
import lord
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



def carta_para_dicionario(card: Card) -> dict:
    return {
        'pack_code': card.pack_code,
        'pack_name': card.pack_name,
        'type_code': card.type_code,
        'type_name': card.type_name,
        'sphere_code': card.sphere_code,
        'number': card.position,
        'name': card.name,
        'traits': card.traits,
        'text': card.text,
        'is_unique': card.is_unique,
        'threat': card.threat,
        'willpower': card.willpower,
        'attack': card.attack,
        'defense': card.defense,
        'health': card.health,
        'quantity': card.quantity,
        'deck_limit': card.deck_limit,
        'has_errata': card.has_errata,
        'url': card.url,
        'imagesrc': card.imagesrc,
        'cost': card.cost
    }


def pegar_classe_da_carta_jogador(carta: Card):
    if carta.type_code == 'hero':
        return lord.Hero
    elif carta.type_code == 'ally':
        return lord.Aliado
    elif carta.type_code == 'event':
        return lord.Evento
    elif carta.type_code == 'attachment':
        return lord.Acessorio
    else:
        raise Exception("Esse carta não é de jogador ou não configurada ");

def carta_cenario_para_dicionario(card: Scenario) -> dict:
    return {
        'number': card.number, # ok
        'pack_code': card.pack_code, # ok
        'pack_name': card.pack_name, # ok
        'type_code': card.type_code, # ok
        'type_name': card.type_name, # ok
        'name': card.name, # ok
        'shadow': card.shadow, # ok
        'traits': card.traits, # ok
        'text': card.text, # ok
        'is_unique': card.is_unique, # ok
        'threat': card.threat, # ok
        'willpower': card.willpower, # ok
        'attack': card.attack, # ok
        'defense': card.defense, # ok
        'health': card.health, # ok
        'keywords': card.keywords, # ok
        'cycle': card.cycle, # ok
        'encounter_set': card.encounter_set,# ok
        'quest_points': card.quest_points, # ok
        'sequence': card.sequence, #ok
        'quantity': card.count, # ok
        'victory': card.victory, # ok
        'notes': card.notes,
        'engage': card.engage
    }    

def pegar_classe_da_carta_cenario(carta: dict):
    if carta['type_code'] == 'enemy':
        return lord.Inimigo
    elif carta['type_code'] == 'quest':
        return lord.Mission
    elif carta['type_code'] == 'location':
        return lord.Localidade
    elif carta['type_code'] == 'treachery':
        return lord.Infortunio
    elif carta['type_code'] == 'objective':
        return lord.Objetivo
    elif carta['type_code'] == 'objective_ally':
        return lord.ObjetivoAliado
    else:
        raise Exception(f"Essa carta não é do deck de cenário. [{carta['name']}]")


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
                print(
                    f'{index}) {carta.name} [{carta.type_name},{carta.sphere_code}] ')
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
                print(remover_tags(carta.text))
                print('------------')
        if args.decks:
            deck = rep.encontra_deck_por_nome(args.search)
            mostrar_deck(deck)


def opcao_play(args):
    if args.new:
        # criar um game
        g = Game()
        if args.active:
            g.active = True
            ativo = rep.encontra_game_ativo()
            if ativo:
                ativo.active = False
                rep.salva_game(ativo)
        rep.salva_game(g)
        print('Jogo criado.')
    elif args.list:
        games = rep.encontra_games()
        for game in games:
            print('ID: {} {}'.format(game.id, '(ativo)' if game.active else ''))
    elif args.search:
        game= rep.encontra_game_por_id(args.search)
        if game is None:
            print('Jogo não encontrado.')
        else:
            if args.active:
                game.active = True
                ativo = rep.encontra_game_ativo()
                if ativo:
                    ativo.active = False
                    rep.salva_game(ativo)
                rep.salva_game(game)
                
    else:
        ativo = rep.encontra_game_ativo()
        if not ativo:
            print('Nenhum jogo ativo encontrado.')
        else:
            print('ID: {}'.format(ativo.id))
            print('Número de Jogadores: {}'.format(ativo.nplayers))
            print('Rodada corrente: {}'.format(ativo.rounds))
