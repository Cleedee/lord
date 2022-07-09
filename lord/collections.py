
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
    }
}