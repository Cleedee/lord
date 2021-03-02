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
    deck.nova_carta(lord.Hero('Balin', 9))
    deck.nova_carta(lord.Card('The One Ring'))
    return deck

@pytest.fixture
def deck_para_abertura():
    deck = lord.Deck()
    deck.nova_carta(lord.Hero('Elfhelm', 10))
    deck.nova_carta(lord.Hero('Éomer', 10))
    deck.nova_carta(lord.Hero('Éowyn', 9))
    deck.nova_carta(lord.Card('Snowbourn Scout'))
    deck.nova_carta(lord.Card('Windfola'))
    deck.nova_carta(lord.Card('Rohan Warhorse'))
    deck.nova_carta(lord.Card('Rohan Warhorse'))
    deck.nova_carta(lord.Card('Firefoot'))
    deck.nova_carta(lord.Card('Westfold Outrider'))
    deck.nova_carta(lord.Card('Armored Destrier'))
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

def test_mão_inicial(jogo_com_um_jogador, deck_para_abertura):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_deck(deck_para_abertura)
    jogo.jogador1.separar()
    jogo.jogador1.embaralhar_deck()
    jogo.jogador1.comprar_mão_inicial()
    assert len(jogo.jogador1.espaço_herois) == 3
    assert len(jogo.jogador1.mão) == 6

def test_ameaça_inicial_é_29(jogo_com_um_jogador, deck_para_abertura):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_deck(deck_para_abertura)
    jogo.jogador1.separar()
    assert jogo.jogador1.ameaça == 29

def test_total_recursos_pos_fase_recursos(jogo_com_um_jogador, deck_para_abertura):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_deck(deck_para_abertura)
    jogo.jogador1.separar()
    jogo.jogador1.embaralhar_deck()
    jogo.jogador1.comprar_mão_inicial()
    jogo.jogador1.adicionar_recursos()
    assert jogo.jogador1.espaço_herois[0].recursos == 1
    assert jogo.jogador1.espaço_herois[1].recursos == 1
    assert jogo.jogador1.espaço_herois[2].recursos == 1

def test_comprar_carta(jogo_com_um_jogador, deck_para_abertura):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_deck(deck_para_abertura)
    jogo.jogador1.separar()
    jogo.jogador1.embaralhar_deck()
    jogo.jogador1.comprar_mão_inicial()
    jogo.jogador1.comprar()
    assert len(jogo.jogador1.mão) == 7

def test_jogar_carta_custo_1(jogo_com_um_jogador, deck_para_abertura):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_deck(deck_para_abertura)
    jogo.jogador1.separar()
    jogo.jogador1.comprar_mão_inicial()
    jogo.jogador1.adicionar_recursos()
    jogo.jogador1.comprar()
    jogo.jogador1.jogar('Snowbourn Scout')
    jogo.jogador1.pagar_de('Elfhelm', 1)
    assert len(jogo.jogador1.mão) == 6
    assert len(jogo.jogador1.mesa) == 1
    assert jogo.jogador1.mesa[0].virado == False
    assert jogo.jogador1.espaço_herois[0].recursos == 0