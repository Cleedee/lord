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
    deck = lord.DeckDeMissao()
    deck.nova_carta(lord.Mission("Grimbeorn's Quest"))
    return deck

@pytest.fixture
def deck_de_conflict_at_the_carrock():
    deck = lord.DeckEncontro()
    deck.nova_carta(lord.Infortunio('Sacked!'))
    deck.nova_carta(lord.Infortunio('Sacked!'))
    deck.nova_carta(lord.Infortunio('Sacked!'))
    deck.nova_carta(lord.Infortunio('Sacked!'))
    deck.nova_carta(lord.Inimigo('Morris'))
    deck.nova_carta(lord.Inimigo('Louis'))
    deck.nova_carta(lord.Inimigo('Rupert')) 
    deck.nova_carta(lord.Inimigo('Stuart'))
    deck.nova_carta(lord.Localidade('The Carrock'))
    return deck

def test_setup_conflict_at_the_carrock(jogo_com_um_jogador, deck_de_missao_conflict_at_the_carrock,
        deck_de_conflict_at_the_carrock):
    jogo = jogo_com_um_jogador
    jogo.escolher_cenario('Conflict at the Carrock', deck_de_missao_conflict_at_the_carrock,
        deck_de_conflict_at_the_carrock)
    jogo.area_de_ameaca.jogo = jogo
    jogo.deck_de_encontro.jogo = jogo
    jogo.fora_do_jogo.jogo = jogo
    lord.packs.conflict_at_the_carrock(jogo)
    assert jogo.area_de_ameaca.cartas[0].nome == 'The Carrock'
    assert len(jogo.fora_do_jogo.cartas) == 7