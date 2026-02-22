# Exemplo de efeito 1: Ir para a mão do jogador
def efeito_adicionar_aa_mao(carta, estado_jogo):
    print(f"Efeito: {carta.nome} adicionado à mão de {estado_jogo.jogador_atual.nome}")
    estado_jogo.jogador_atual.mao.append(carta)


# Exemplo de efeito 2: Aumentar a ameaça
def efeito_aumentar_ameacao(carta, estado_jogo):
    print(f"Efeito: {carta.nome} aumenta a ameaça em 2!")
    estado_jogo.jogador_atual.ameaca += 2
