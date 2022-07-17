
def passage_through_mirkwood(jogo):
    jogo.deck_de_encontro.mover_para_area_de_ameaça('Forest Spider')
    jogo.deck_de_encontro.mover_para_area_de_ameaça('Old Forest Road')
    print('Forest Spider foi colocado na área de ameaça.')
    print('Old Forest Road foi colocado na área de ameaça.')
    print('Setup concluído.')

def journey_down_the_anduin(jogo):
    for jogador in jogo.jogadores:
        carta = jogo.deck_de_encontro.comprar()
        print(f'{carta.nome} colocada na área de ameaça.')
        jogo.area_de_ameaca.cartas.append(carta)
    print('setup concluido.')

def escape_from_dol_guldur(jogo):
    gandalf = jogo.deck_de_encontro.mover_para_area_de_ameaça("Gandalf's Map")
    dungeon = jogo.deck_de_encontro.mover_para_area_de_ameaça('Dungeon Torch')
    shadow = jogo.deck_de_encontro.mover_para_area_de_ameaça('Shadow Key')
    nazgul = shadow = jogo.deck_de_encontro.mover_para_fora_do_jogo('Nazgûl of Dol Guldur')
    carta1 = jogo.deck_de_encontro.comprar()
    gandalf.anexos.append(carta1)
    print(f"{carta1.nome} foi anexada a Gandalf's Map.")
    carta2 = jogo.deck_de_encontro.comprar()
    dungeon.anexos.append(carta2)
    print(f"{carta2.nome} foi anexada a Dungeon Torch.")
    carta3 = jogo.deck_de_encontro.comprar()
    shadow.anexos.append(carta3)
    print(f"{carta3.nome} foi anexada a Shadow Key.")
    print('setup concluido.')

def the_hunt_for_gollum(jogo):
    for jogador in jogo.jogadores:
        carta = jogo.deck_de_encontro.comprar()
        print(f'{carta.nome} colocada na área de ameaça.')
        jogo.area_de_ameaca.cartas.append(carta)
    print('Setup concluido.')

def conflict_at_the_carrock(jogo):
    jogo.deck_de_encontro.mover_para_area_de_ameaça('The Carrock')
    jogo.deck_de_encontro.mover_para_fora_do_jogo('Sacked!')
    jogo.deck_de_encontro.mover_para_fora_do_jogo('Sacked!')
    jogo.deck_de_encontro.mover_para_fora_do_jogo('Sacked!')
    jogo.deck_de_encontro.mover_para_fora_do_jogo('Sacked!')
    jogo.deck_de_encontro.mover_para_fora_do_jogo('Morris')
    jogo.deck_de_encontro.mover_para_fora_do_jogo('Louis')
    jogo.deck_de_encontro.mover_para_fora_do_jogo('Rupert')
    jogo.deck_de_encontro.mover_para_fora_do_jogo('Stuart')
    for jogador in jogo.jogadores:
        jogo.fora_do_jogo.mover_para_deck_de_encontro('Sacked!')
    jogo.deck_de_encontro.embaralhar()
    print('Setup concluido.')

CENARIOS_CONJUNTOS = {
    'Passage Through Mirkwood' : {
        'conjuntos':
            [
            'Dol Guldur Orcs',
            'Passage Through Mirkwood',
            'Spiders of Mirkwood'
             ],
        'setup': passage_through_mirkwood
    },
    'Journey Down the Anduin': {
        'conjuntos': [
            'Journey Down the Anduin',
            "Sauron's Reach",
            "Dol Guldur Orcs",
            "Wilderlands"
        ],
        'setup': journey_down_the_anduin
    },
    'Escape from Dol Guldur': {
        'conjuntos': [
            'Escape from Dol Guldur',
            'Spiders of Mirkwood',
            'Dol Guldur Orcs',
        ],
        'setup': escape_from_dol_guldur
    },
    'The Hunt for Gollum': {
        'conjuntos': [
            'The Hunt for Gollum',
            'Journey Down the Anduin',
            "Sauron's Reach",
        ],
        'setup': the_hunt_for_gollum
    },
    'Conflict at the Carrock': {
        'conjuntos': [
            'Conflict at the Carrock',
            'Journey Down the Anduin',
            "Wilderlands",
        ],
        'setup': conflict_at_the_carrock
    }
}