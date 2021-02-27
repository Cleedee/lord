import pytest

import lord

@pytest.fixture
def jogo_com_um_jogador():
    jogo = lord.Jogo()
    jogo.novo_jogador('Paulo')
    return jogo

@pytest.fixture
def deck_duas_cartas():
    deck = lord.Deck()
    deck.nova_carta(lord.Hero('Balin'))
    deck.nova_carta(lord.Card('The One Ring'))
    return deck

def test_sem_jogadores():
    jogo = lord.Jogo()
    assert False if jogo.jogadores else True

def test_um_jogador(jogo_com_um_jogador):
    jogo = jogo_com_um_jogador
    assert jogo.jogadores != None and len(jogo.jogadores) == 1
    assert jogo.jogador1.nome == 'Paulo'

def test_deck_de_2_cartas(jogo_com_um_jogador, deck_duas_cartas):
    jogo = jogo_com_um_jogador
    deck = deck_duas_cartas
    jogo.jogador1.usar_deck(deck)
    assert jogo.jogador1.deck.total == 2

def test_sem_cartas_na_mao(jogo_com_um_jogador, deck_duas_cartas):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_deck(deck_duas_cartas)
    assert len(jogo.jogador1.mão) == 0

def test_separar_herois(jogo_com_um_jogador, deck_duas_cartas):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_deck(deck_duas_cartas)
    jogo.jogador1.separar()
    assert len(jogo.jogador1.espaço_herois) == 1

def test_carta_virada(jogo_com_um_jogador, deck_duas_cartas):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_deck(deck_duas_cartas)
    jogo.jogador1.separar()
    jogo.jogador1.espaço_herois[0].virar()
    assert jogo.jogador1.espaço_herois[0].virado == True