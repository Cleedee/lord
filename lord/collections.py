
def passage_through_mirkwood(jogo):
    jogo.mover_carta('Forest Spider', jogo.DECK_DE_ENCONTRO, jogo.AREA_DE_AMEACA)
    jogo.mover_carta('Old Forest Road', jogo.DECK_DE_ENCONTRO, jogo.AREA_DE_AMEACA)
    print('setup concluído.')

def journey_down_the_anduin(jogo):
    for jogador in jogo.jogadores:
        carta = jogo.deck_de_encontro.comprar()
        print(f'{carta.nome} colocada na área de ameaça.')
        jogo.area_de_ameaca.cartas.append(carta)
    print('setup concluido.')

def escape_from_dol_guldur(jogo):
    gandalf = jogo.mover_carta("Gandalf's Map", jogo.DECK_DE_ENCONTRO, jogo.AREA_DE_AMEACA)
    dungeon = jogo.mover_carta('Dungeon Torch', jogo.DECK_DE_ENCONTRO, jogo.AREA_DE_AMEACA)
    shadow = jogo.mover_carta('Shadow Key', jogo.DECK_DE_ENCONTRO, jogo.AREA_DE_AMEACA)
    jogo.mover_carta('Nazgûl of Dol Guldur', jogo.DECK_DE_ENCONTRO, jogo.FORA_DO_JOGO)
    carta1 = jogo.deck_de_encontro.comprar()
    gandalf.anexos.append(carta1)
    carta2 = jogo.deck_de_encontro.comprar()
    dungeon.anexos.append(carta2)
    carta3 = jogo.deck_de_encontro.comprar()
    shadow.anexos.append(carta3)

def the_hunt_for_gollum(jogo):
    for jogador in jogo.jogadores:
        carta = jogo.deck_de_encontro.comprar()
        print(f'{carta.nome} colocada na área de ameaça.')
        jogo.area_de_ameaca.cartas.append(carta)
    print('setup concluido.')

def conflict_at_the_carrock(jogo):
    jogo.mover_carta('The Carrock', jogo.DECK_DE_ENCONTRO, jogo.AREA_DE_AMEACA)
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
    print('setup concluido.')

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
            'The Hunt For Gollum',
            'Journey Down the Anduin',
            "Sauron's Reach",
        ],
        'setup': the_hunt_for_gollum
    }    
}