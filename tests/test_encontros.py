import pytest

import lord

@pytest.fixture
def deck_de_missao():
    # http://lotrlcg.com/Scenario/Scenario/1001

    deck = lord.DeckDeMissao()
    base = {'text':'', 'traits':'','number': 0, 'type_code': 'quest', 'quest_points': 0}
    q1 = base.copy()
    q1['sequence'] = 1
    q2 = base.copy()
    q2['sequence'] = 2
    q3 = base.copy()
    q3['sequence'] = 3
    q4 = base.copy()
    q4['sequence'] = 3    
    deck.nova_carta(lord.Mission('Flies and Spiders', **q1))
    deck.nova_carta(lord.Mission('A Fork in the Road', **q2))
    deck.nova_carta(lord.Mission("""A Chosen Path - "Don't Leave the Path!" """, **q3))
    deck.nova_carta(lord.Mission("A Chosen Path - Beorn's Path", **q4))
    return deck

@pytest.fixture
def deck_de_encontro():
    base = {
        'text':'',
        'traits':'',
        'number': 0,
        'type_code':'hero',
        'encounter_set': 'Conflict at the Carrock',
        'shadow': '',
        'engage': '',
        'threat': '0',
        'attack': '0',
        'defense': '0',
        'health': '0',
        'quest_points': '0',
        'victory': '0'
    }
    location_fake = {
        'threat': 0,
        'quest_points': 3,
        'victory': '1',
        'encounter_set': '',
        'shadow': ''
    }
    location_fake.update(base)    
    deck = lord.DeckEncontro()
    deck.nova_carta(lord.Inimigo('Forest Spider', **base))
    deck.nova_carta(lord.Localidade('Old Forest Road', **location_fake))
    return deck

def test_missao_atual(mocker, deck_de_missao, deck_de_encontro):
    jogo = lord.Jogo()
    mock_carregar_deck_cenario = mocker.patch('lord.loader.carregar_deck_cenario')
    mock_carregar_deck_cenario.return_value = (deck_de_missao, deck_de_encontro) 
    jogo.enfrentar_cenario('Passage Through Mirkwood')
    jogo.setup()
    assert jogo.missao_atual.nome == 'Flies and Spiders'

def test_objetivo_defendido():
    jogo = lord.Jogo()
