import pytest

import lord

@pytest.fixture
def jogo_com_um_jogador():
    jogo = lord.Jogo()
    jogo.novo_jogador('Paulo')
    return jogo

@pytest.fixture
def deck_de_missao_conflict_at_the_carrock():
    # http://hallofbeorn.com/LotR/Scenarios/A-Shadow-of-the-Past
    texto = """
    Setup: Add The Carrock to the staging area. Remove 4 unique Troll cards 
    and 4 copies of the "Sacked!" card from the encounter deck and set 
    them aside, out of play. Then shuffle 1 "Sacked!" card per player 
    back into the encounter deck.
    """
    deck = lord.Baralho()
    base = {'text':'', 'traits':'','number': 0, 'type_code': 'quest', 'sequence': '1.0'}
    missao = base.copy()
    missao['text'] = texto
    deck.nova_carta(lord.Mission("Grimbeorn's Quest", **missao))
    return deck

@pytest.fixture
def deck_de_conflict_at_the_carrock():
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
    deck = lord.DeckEncontro()
    deck.nova_carta(lord.Infortunio('Sacked!', **base))
    deck.nova_carta(lord.Infortunio('Sacked!', **base))
    deck.nova_carta(lord.Infortunio('Sacked!', **base))
    deck.nova_carta(lord.Infortunio('Sacked!', **base))
    deck.nova_carta(lord.Inimigo('Morris', **base))
    deck.nova_carta(lord.Inimigo('Louis', **base))
    deck.nova_carta(lord.Inimigo('Rupert', **base)) 
    deck.nova_carta(lord.Inimigo('Stuart', **base))
    deck.nova_carta(lord.Localidade('The Carrock', **base))
    return deck

def test_setup_conflict_at_the_carrock(jogo_com_um_jogador, deck_de_missao_conflict_at_the_carrock,
        deck_de_conflict_at_the_carrock):
    jogo = jogo_com_um_jogador
    jogo.escolher_cenario('Conflict at the Carrock', deck_de_missao_conflict_at_the_carrock,
        deck_de_conflict_at_the_carrock)
    jogo.area_de_ameaca.jogo = jogo
    jogo.deck_de_encontro.jogo = jogo
    jogo.fora_do_jogo.jogo = jogo
    lord.collections.conflict_at_the_carrock(jogo)
    assert jogo.area_de_ameaca.cartas[0].nome == 'The Carrock'
    assert len(jogo.fora_do_jogo.cartas) == 7