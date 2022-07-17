import pytest

import lord

@pytest.fixture
def jogo_com_um_jogador():
    jogo = lord.Jogo()
    jogo.novo_jogador('Paulo')
    return jogo

@pytest.fixture
def jogo_com_dois_jogadores():
    jogo = lord.Jogo()
    jogo.novo_jogador('Paulo')
    jogo.novo_jogador('Maria')
    return jogo

@pytest.fixture
def deck_duas_cartas():
    base = {'text':'', 'traits':'','number': 0, 'type_code': 'hero'}
    balin = {
        'threat': 9,
        'willpower': 2,
        'attack': 1,
        'defense': 2,
        'health': 4,
        'sphere_code': 'leadership',
    }
    balin.update(base)
    deck = lord.Baralho()
    deck.nova_carta(lord.Hero('Balin', **balin))
    deck.nova_carta(lord.Carta('The One Ring', **base))
    return deck

@pytest.fixture
def deck_para_abertura():
    deck = lord.Baralho()
    base = {'number': 0,'type_code':'hero'}
    snowbourn = {
        'text': """Response: After Snowbourn Scout enters play, choose a location. 
            Place 1 progress token on that location.""",
        'sphere_code': 'leadership',
        'willpower': 0,
        'attack': 0,
        'defense': 1,
        'health': 1,
        'cost': 1,
        'traits': 'Rohan. Scout.'
    }
    snowbourn.update(base)
    windfola = {
        'text': """
            Attach to a spirit hero, or to Éowyn. Restricted.

            Attached character gets +1 willpower.

            Response: After attached character is removed from the quest, exhaust Windfola to 
            commit attached hero to the quest.
            """,
        'sphere_code': 'spirit',
        'traits': 'Mount.',
        'cost': 1,
    }
    windfola.update(base)
    rohan_warhorse = {
        'text': """
            Attach to a  or Rohan hero. Restricted.

            Response: After attached hero participates in an attack that destroys an enemy, 
            exhaust Rohan Warhorse to ready attached hero.
            """,
        'sphere_code':  'tactics',
        'traits': 'Mount.',
        'cost': 1
    }
    rohan_warhorse.update(base)
    firefoot = {
        'sphere_code': 'tactics',
        'cost': 2,
        'traits': 'Mount.',
        'text': ''
    }
    firefoot.update(base)
    westfold = {
        'cost': 2,
        'willpower': 0,
        'attack': 2,
        'defense': 1,
        'health': 2,
        'sphere_code': 'tactics',
        'traits': 'Rohan. Scout.',
        'text': ''
    }
    westfold.update(base)
    armored = {
        'sphere_code': 'leadership',
        'cost': 2,
        'traits': 'Mount.',
        'text': ''
    }
    armored.update(base)
    deck.nova_carta(lord.Aliado('Snowbourn Scout', **snowbourn))
    deck.nova_carta(lord.Acessorio('Windfola', **windfola))
    deck.nova_carta(lord.Acessorio('Rohan Warhorse', **rohan_warhorse))
    deck.nova_carta(lord.Acessorio('Rohan Warhorse', **rohan_warhorse))
    deck.nova_carta(lord.Acessorio('Firefoot', **firefoot))
    deck.nova_carta(lord.Aliado('Westfold Outrider', **westfold))
    deck.nova_carta(lord.Acessorio('Armored Destrier', **armored))
    return deck

@pytest.fixture
def herois():
    base = {'number': 0, 'text': '', 'type_code': 'hero'}
    elfhelm = {
        'threat': 10,
        'willpower': 2,
        'attack': 2,
        'defense': 2,
        'health': 4,
        'sphere_code': 'leadership',
        'traits': 'Rohan. Scout. Warrior.'
    }
    elfhelm.update(base)
    eomer = {
        'threat': 10,
        'willpower': 1,
        'attack': 3,
        'defense': 2,
        'health': 4,
        'sphere_code': 'leadership',
        'traits': 'Rohan. Noble. Warrior.'
    }
    eomer.update(base)
    eowyn = {
        'threat': 9,
        'willpower': 4,
        'attack': 1,
        'defense': 1,
        'health': 3,
        'sphere_code': 'spirit',
        'traits': 'Noble. Rohan.'
    }
    eowyn.update(base)    
    deck = lord.Baralho()
    deck.nova_carta(lord.Hero('Elfhelm', **elfhelm))
    deck.nova_carta(lord.Hero('Éomer', **eomer))
    deck.nova_carta(lord.Hero('Éowyn', **eowyn))
    return deck

@pytest.fixture
def deck_de_missao():
    # http://hallofbeorn.com/LotR/Scenarios/A-Shadow-of-the-Past
    texto = """
    Setup: Set Buckleberry Ferry aside, out of play. Add 1 Black Rider to the
    staging area and make Bag End the active location. Shuffle the encounter
    deck.
    """
    deck = lord.DeckDeMissao()
    base = {'text':'', 'traits':'','number': 0, 'type_code': 'quest', 
        'sequence': '1.0', 'quest_points': 0
    }
    missao = base.copy()
    missao['text'] = texto
    deck.nova_carta(lord.Mission('Three is Company', **missao))
    deck.nova_carta(lord.Mission('A Shortcut to Mushrooms', **base))
    deck.nova_carta(lord.Mission('Escape to Buckland', **base))
    return deck

@pytest.fixture
def deck_de_encontro():
    base = {'text':'', 'traits':'','number': 0, 'type_code': 'hero'}
    bagend = {
        'threat': 0,
        'quest_points': 3,
        'victory': '1',
        'encounter_set': '',
        'shadow': ''
    }
    bagend.update(base)
    deck = lord.Baralho()
    deck.nova_carta(lord.Carta('A Shadow of the Past', **base))
    deck.nova_carta(lord.Carta('Bag End', **base))
    deck.nova_carta(lord.Carta('Woody End', **base))
    deck.nova_carta(lord.Carta('Stock-Brook', **base))
    deck.nova_carta(lord.Carta('Pathless Country', **base))
    deck.nova_carta(lord.Carta('Buckleberry Ferry', **base))
    deck.nova_carta(lord.Carta('Black Rider', **base))
    deck.nova_carta(lord.Localidade('Bag End', **bagend))
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
    assert jogo.jogador1.ameaça_inicial == 29

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
    #jogo.jogador1.usar_decks(herois, deck_para_abertura)
    #jogo.jogador1.comprar_mão_inicial()
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
    assert 'Set Buckleberry Ferry aside' in jogo.deck_de_missao.cartas[0].texto
    assert jogo.fora_do_jogo.total > 0
    assert jogo.fora_do_jogo.cartas[0].nome == 'Buckleberry Ferry'
    assert jogo.area_de_ameaca.total > 0
    assert jogo.area_de_ameaca.cartas[0].nome == 'Black Rider'

def test_total_recursos(jogo_com_um_jogador, deck_para_abertura, herois):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_decks(herois, deck_para_abertura)
    jogo.jogador1.comprar_mão_inicial()
    jogo.jogador1.adicionar_recursos()
    assert jogo.jogador1.leadership == 2
    assert jogo.jogador1.spirit == 1

def test_ver_primeira_carta_da_mão(jogo_com_um_jogador, deck_para_abertura, herois):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_decks(herois, deck_para_abertura)
    jogo.jogador1.comprar_mão_inicial()
    texto = 'Snowbourn Scout'
    assert jogo.jogador1.mão[0].nome == texto

def test_ver_segunda_carta_da_mão(jogo_com_um_jogador, deck_para_abertura, herois):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_decks(herois, deck_para_abertura)
    jogo.jogador1.comprar_mão_inicial()
    texto = 'Windfola'
    assert jogo.jogador1.mão[1].nome == texto

def test_custo_da_carta(jogo_com_um_jogador, deck_para_abertura, herois):
    jogo = jogo_com_um_jogador
    jogo.jogador1.usar_decks(herois, deck_para_abertura)
    jogo.jogador1.comprar_mão_inicial()
    assert jogo.jogador1.hand[0].custo == 1 # Snowbourn Scout
    assert jogo.jogador1.hand[4].custo == 2 # Firefoot

def test_primeiro_jogador(jogo_com_dois_jogadores):
    jogo = jogo_com_dois_jogadores
    assert jogo.jogador_inicial == None

def test_definir_jogador_inicial_antes_de_comprar_mão_preparação(
        jogo_com_dois_jogadores,
        herois, deck_para_abertura):
    jogo = jogo_com_dois_jogadores
    jogo.jogador1.usar_decks(herois, deck_para_abertura)
    jogo.jogador1.comprar_mão_inicial()
    assert jogo.jogador_inicial == None
    assert len(jogo.jogador1.mão) == 0
