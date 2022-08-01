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
    deck = lord.DeckEncontro()
    deck.nova_carta(lord.Inimigo('Forest Spider'))
    deck.nova_carta(lord.Localidade('Old Forest Road'))
    return deck

@pytest.fixture
def cartas_test_objetivo():
    return [
        lord.Objetivo('Signs of Gollum', traits='Guarded.'),
        lord.Localidade('The East Bank')
    ]

def test_missao_atual(mocker, deck_de_missao, deck_de_encontro):
    jogo = lord.Jogo()
    mock_carregar_deck_cenario = mocker.patch('lord.loader.carregar_deck_cenario')
    mock_carregar_deck_cenario.return_value = (deck_de_missao, deck_de_encontro) 
    jogo.enfrentar_cenario('Passage Through Mirkwood')
    jogo.setup()
    assert jogo.missao_atual.nome == 'Flies and Spiders'

def test_objetivo_defendido(mocker, deck_de_missao, deck_de_encontro, cartas_test_objetivo):
    jogo = lord.Jogo()
    mock_carregar_deck_cenario = mocker.patch('lord.loader.carregar_deck_cenario')
    mock_carregar_deck_cenario.return_value = (deck_de_missao, deck_de_encontro)
    jogo.enfrentar_cenario('Passage Through Mirkwood')
    jogo.setup()
    jogo.deck_de_encontro.cartas.extend(cartas_test_objetivo)
    objetivo = jogo.comprar()
    assert objetivo.defendido == False
    assert objetivo.tem_atributo_defendido == True
    jogo.comprar()
    assert jogo.area_de_ameaca.cartas[2].nome == 'Signs of Gollum'
    assert jogo.area_de_ameaca.cartas[3].nome == 'The East Bank'
    assert objetivo.defendido == True
