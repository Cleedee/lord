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
    deck.nova_carta(lord.Card('Snowbourn Scout'))
    deck.nova_carta(lord.Card('Windfola'))
    deck.nova_carta(lord.Card('Rohan Warhorse'))
    deck.nova_carta(lord.Card('Rohan Warhorse'))
    deck.nova_carta(lord.Card('Firefoot'))
    deck.nova_carta(lord.Card('Westfold Outrider'))
    deck.nova_carta(lord.Card('Armored Destrier'))
    return deck

@pytest.fixture
def herois():
    deck = lord.Deck()
    deck.nova_carta(lord.Hero('Elfhelm', 10))
    deck.nova_carta(lord.Hero('Éomer', 10))
    deck.nova_carta(lord.Hero('Éowyn', 9))
    return deck

@pytest.fixture
def deck_de_missao():
    # http://hallofbeorn.com/LotR/Scenarios/A-Shadow-of-the-Past
    texto = """
    Setup: Set Buckleberry Ferry aside, out of play. Add 1 Black Rider to the
    staging area and make Bag End the active location. Shuffle the encounter
    deck.
    """
    deck = lord.Deck()
    deck.nova_carta(lord.Mission('Three is Company',texto))
    deck.nova_carta(lord.Mission('A Shortcut to Mushrooms'))
    deck.nova_carta(lord.Mission('Escape to Buckland'))
    return deck

@pytest.fixture
def deck_de_encontro():
    deck = lord.Deck()
    deck.nova_carta(lord.Card('A Shadow of the Past'))
    deck.nova_carta(lord.Card('Bag End'))
    deck.nova_carta(lord.Card('Woody End'))
    deck.nova_carta(lord.Card('Stock-Brook'))
    deck.nova_carta(lord.Card('Pathless Country'))
    deck.nova_carta(lord.Card('Buckleberry Ferry'))
    deck.nova_carta(lord.Card('Black Rider'))
    deck.nova_carta(lord.Location('Bag End',0,3,vitoria = 1))
    return deck


def test_sem_jogadores():
    jogo = lord.Jogo()
    assert False if jogo.jogadores else True

def test_um_jogador(jogo_com_um_jogador):
    jogo = jogo_com_um_jogador
    assert jogo.jogadores != None and len(jogo.jogadores) == 1
    assert jogo.jogador1.nome == 'Paulo'

def test_deck_de_2_cartas(jogo_com_um_jogador, deck_duas_cartas, herois):
    jogo = jogo_com_um_jogador
    deck = deck_duas_cartas
    jogo.jogador1.usar_decks(herois, deck)
    assert jogo.jogador1.deck_de_jogador.total == 2

def test_sem_cartas_na_mao(jogo_com_um_jogador, deck_duas_cartas, herois):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_decks(herois, deck_duas_cartas)
    assert len(jogo.jogador1.mão) == 0

def test_carta_virada(jogo_com_um_jogador, deck_duas_cartas, herois):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_decks(herois, deck_duas_cartas)
    jogo.jogador1.herois_em_jogo.cartas[0].virar()
    assert jogo.jogador1.herois_em_jogo.cartas[0].virado == True

def test_mão_inicial(jogo_com_um_jogador, deck_para_abertura, herois):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_decks(herois, deck_para_abertura)
    jogo.jogador1.embaralhar_deck()
    jogo.jogador1.comprar_mão_inicial()
    assert jogo.jogador1.herois_em_jogo.total == 3
    assert len(jogo.jogador1.mão) == 6

def test_ameaça_inicial_é_29(jogo_com_um_jogador, deck_para_abertura, herois):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_decks(herois, deck_para_abertura)
    assert jogo.jogador1.ameaça == 29

def test_total_recursos_pos_fase_recursos(jogo_com_um_jogador, deck_para_abertura,
    herois):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_decks(herois, deck_para_abertura)
    jogo.jogador1.embaralhar_deck()
    jogo.jogador1.comprar_mão_inicial()
    jogo.jogador1.adicionar_recursos()
    assert jogo.jogador1.herois_em_jogo.cartas[0].recursos == 1
    assert jogo.jogador1.herois_em_jogo.cartas[1].recursos == 1
    assert jogo.jogador1.herois_em_jogo.cartas[2].recursos == 1

def test_comprar_carta(jogo_com_um_jogador, deck_para_abertura, herois):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_decks(herois, deck_para_abertura)
    jogo.jogador1.embaralhar_deck()
    jogo.jogador1.comprar_mão_inicial()
    jogo.jogador1.comprar()
    assert len(jogo.jogador1.mão) == 7

def test_jogar_carta_custo_1(jogo_com_um_jogador, deck_para_abertura, herois):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_decks(herois, deck_para_abertura)
    jogo.jogador1.comprar_mão_inicial()
    jogo.jogador1.adicionar_recursos()
    jogo.jogador1.comprar()
    jogo.jogador1.jogar('Snowbourn Scout')
    jogo.jogador1.pagar_de('Elfhelm', 1)
    assert len(jogo.jogador1.mão) == 6
    assert jogo.jogador1.mesa.total == 1
    assert jogo.jogador1.mesa.cartas[0].virado == False
    assert jogo.jogador1.herois_em_jogo.cartas[0].recursos == 0

def test_existe_cenario(jogo_com_um_jogador, deck_para_abertura,
    deck_de_missao, deck_de_encontro, herois):
    jogo = jogo_com_um_jogador
    jogo.escolher_cenario('A Shadow of the Past', deck_de_missao, deck_de_encontro)
    jogo.jogador1.usar_decks(herois, deck_para_abertura)
    jogo.jogador1.comprar_mão_inicial()
    assert jogo.deck_de_missao.total > 0
    assert jogo.deck_de_encontro.total > 0

def test_carta_fora_do_jogo(jogo_com_um_jogador, deck_para_abertura,
    deck_de_missao, deck_de_encontro, herois):
    jogo = jogo_com_um_jogador
    jogo.escolher_cenario('A Shadow of the Past', deck_de_missao, deck_de_encontro)
    jogo.jogador1.usar_decks(herois, deck_para_abertura)
    jogo.jogador1.comprar_mão_inicial()
    jogo.mover_carta('Buckleberry Ferry',jogo.DECK_DE_ENCONTRO,jogo.FORA_DO_JOGO)
    jogo.mover_carta('Black Rider',jogo.DECK_DE_ENCONTRO,jogo.AREA_DE_AMEACA)
    jogo.mover_carta('Bag End',jogo.DECK_DE_ENCONTRO,jogo.LOCALIZACAO_ATIVA)
    assert 'Set Buckleberry Ferry aside' in jogo.deck_de_missao.cartas[0].texto_frente
    assert jogo.fora_do_jogo.total > 0
    assert jogo.fora_do_jogo.cartas[0].nome == 'Buckleberry Ferry'
    assert jogo.area_de_ameaca.total > 0
    assert jogo.area_de_ameaca.cartas[0].nome == 'Black Rider'
