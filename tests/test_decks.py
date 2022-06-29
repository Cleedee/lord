import pytest

from lord import scrap, loader
from lord import Hero, Jogo, Baralho
import lord

@pytest.fixture
def jogo_com_um_jogador():
    jogo = Jogo()
    jogo.novo_jogador('Paulo')
    return jogo

@pytest.fixture
def deck_de_missao():
    # http://hallofbeorn.com/LotR/Scenarios/A-Shadow-of-the-Past
    texto = """
    Setup: Set Buckleberry Ferry aside, out of play. Add 1 Black Rider to the
    staging area and make Bag End the active location. Shuffle the encounter
    deck.
    """
    deck = Baralho()
    deck.nova_carta(lord.Mission('Three is Company',texto))
    deck.nova_carta(lord.Mission('A Shortcut to Mushrooms'))
    deck.nova_carta(lord.Mission('Escape to Buckland'))
    return deck

@pytest.fixture
def deck_de_encontro():
    deck = Baralho()
    deck.nova_carta(lord.Card('A Shadow of the Past'))
    deck.nova_carta(lord.Card('Bag End'))
    deck.nova_carta(lord.Card('Woody End'))
    deck.nova_carta(lord.Card('Stock-Brook'))
    deck.nova_carta(lord.Card('Pathless Country'))
    deck.nova_carta(lord.Card('Buckleberry Ferry'))
    deck.nova_carta(lord.Card('Black Rider'))
    deck.nova_carta(lord.Location('Bag End',0,3,vitoria = 1))
    return deck

@pytest.fixture
def deck_dict():
    d = {
        'id': 20040,
        'name': 'Four Hobbitsesss',
        'date_creation': '2021-03-22T14:47:32-03:00',
        'date_update': '2021-03-22T14:47:32-03:00',
        'description_md': '',
        'user_id': 9451,
        'heroes': {'10001': 1, '17109': 1, '19112': 1, '21002': 1},
        'slots': {
            '01023': 2,
            '01036': 2,
            '01045': 1,
            '01049': 1,
            '01050': 2,
            '01057': 2,
            '01073': 2,
            '02103': 2,
            '06010': 2,
            '06065': 1,
            '08087': 2,
            '09014': 1,
            '10001': 1,
            '10007': 2,
            '10034': 1,
            '12035': 1,
            '17002': 2,
            '17109': 1,
            '19112': 1,
            '19115': 1,
            '19116': 2,
            '19117': 2,
            '19121': 2,
            '21002': 1,
            '22005': 2,
            '22006': 2,
            '22110': 2,
            '22142': 1,
            '22147': 1,
            '141006': 1,
            '141008': 1,
            '142003': 1,
            '142005': 1,
            '144005': 2,
            '146005': 2,
            '146012': 2
        },
        'sideslots': {
            '01034': 2,
            '19149': 2,
            '21001': 1,
            '21009': 2,
            '21010': 2,
            '22033': 1
        },
        'version': '1.0',
        'freeze_comments': None,
        'is_published': True,
        'nb_votes': 0,
        'nb_favorites': 0,
        'nb_comments': 0,
        'starting_threat': 25
    }
    return d
