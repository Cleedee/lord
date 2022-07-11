import random
from functools import reduce
from collections import UserList

from lord import repository as rep
from lord import loader, utils, collections
from lord.collections import CENARIOS_CONJUNTOS

class Carta():
    def __init__(self, nome, **args):
        self.nome = nome
        self.texto =  utils.remover_tags(args['text'])
        self.atributos= args['traits']
        self.numero = args['number']
        self.tipo = args['type_code']
        self.virado = False
        self.anexos = []

    def virar(self):
        self.virado = True

    def __repr__(self):
        return self.nome

class CartaJogador(Carta):
    def __init__(self, nome, **args):
        super().__init__(nome, **args)
        self.esfera = args['sphere_code']

    @property
    def is_neutral(self):
        return True if self.esfera == 'neutral' else False

    @property
    def is_leadership(self):
        return True if self.esfera == 'leadership' else False
    
    @property
    def is_lore(self):
        return True if self.esfera == 'lore' else False

    @property
    def is_spirit(self):
        return True if self.esfera == 'spirit' else False

    @property
    def is_tactics(self):
        return True if self.esfera == 'tactics' else False

    @property
    def is_baggins(self):
        return True if self.esfera == 'baggins' else False


class Hero(CartaJogador):
    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)
        self.custo_ameaça = kwargs['threat']
        self.força_vontade = kwargs['willpower']
        self.ataque = kwargs['attack']
        self.defesa = kwargs['defense']
        self.pontos_vida = kwargs['health']
        self.recursos = 0
        self.dano = 0

    def adicionar_recurso(self):
        self.recursos += 1

    def __repr__(self):
        texto = ''
        texto += f'Nome: {self.nome} ({self.custo_ameaça})\n'
        texto += f'{self.atributos}\n'
        texto += f'FV: {self.força_vontade} A: {self.ataque} D: {self.defesa} PV: {self.pontos_vida}'
        return texto


class Acessorio(CartaJogador):

    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)
        self.custo = kwargs['cost']

    def __str__(self):
        texto = ''
        texto += f'{self.nome} ({self.tipo})\n'
        texto += f'Esfera/Custo: {self.esfera} / {self.custo}\n'
        texto += '------------\n'
        texto += f'Atributos: {self.atributos}\n'
        texto += '------------\n'
        texto += f'{self.texto}\n'
        return texto

class Aliado(CartaJogador):

    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)
        self.custo = kwargs['cost']
        self.força_vontade = kwargs['willpower']
        self.ataque = kwargs['attack']
        self.defesa = kwargs['defense']
        self.pontos_vida = kwargs['health']
        self.dano = 0

    def __str__(self):
        texto = ''
        texto += f'{self.nome} ({self.tipo})\n'
        texto += f'Esfera/Custo: {self.esfera} / {self.custo}\n'
        texto += f'FV: {self.força_vontade} A: {self.ataque} D: {self.defesa} PV: {self.pontos_vida}\n'
        texto += f'Dano: {self.dano}\n'
        texto += '------------\n'
        texto += f'Atributos: {self.atributos}\n'
        texto += '------------\n'
        texto += f'{self.texto}\n'
        return texto

class Evento(CartaJogador):
    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)
        self.custo = kwargs['cost']

    def __str__(self):
        texto = ''
        texto += f'{self.nome} ({self.tipo})\n'
        texto += f'Esfera/Custo: {self.esfera} / {self.custo}\n'
        texto += '------------\n'
        texto += f'Atributos: {self.atributos}\n'
        texto += '------------\n'
        texto += f'{self.texto}\n'
        return texto

class CartaCenario(Carta):
    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)
        self.força_ameaça = 0

class Mission(CartaCenario):
    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)

class Localidade(CartaCenario):
    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)
        self.força_ameaça = int(kwargs['threat'])
        self.pontos_missao = kwargs['quest_points']
        self.vitoria = kwargs['victory']
        self.conjunto_encontro = kwargs['encounter_set']
        self.efeito_sombrio = kwargs['shadow']

    def __str__(self):
        texto = ''
        texto += f'{self.nome} ({self.tipo})\n'
        texto += '------------\n'
        texto += f'FA: {self.força_ameaça} PM: {self.pontos_missao}\n'
        texto += f'Pontos de Vitória: {self.vitoria}\n'
        texto += f'Atributos: {self.atributos}\n'
        texto += '------------\n'
        texto += f'{self.texto}\n'
        if self.efeito_sombrio:
            texto += '------------\n'
            texto += f'{self.efeito_sombrio}\n'
        return texto            
    

class Infortunio(CartaCenario):
    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)
        self.conjunto_encontro = kwargs['encounter_set']
        self.efeito_sombrio = kwargs['shadow']

class Objetivo(CartaCenario):
    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)
        self.conjunto_encontro = kwargs['encounter_set']
        self.efeito_sombrio = kwargs['shadow']

class ObjetivoAliado(CartaCenario):
    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)
        self.força_vontade = kwargs['willpower']
        self.ataque = kwargs['attack']
        self.defesa = kwargs['defense']
        self.pontos_vida = kwargs['health']
        self.dano = 0


class Inimigo(CartaCenario):
    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)
        self.custo_engajamento = kwargs['engage']
        self.força_ameaça = int(kwargs['threat'])
        self.ataque = kwargs['attack']
        self.defesa = kwargs['defense']
        self.pontos_vida = kwargs['health']
        self.conjunto_encontro = kwargs['encounter_set']
        self.efeito_sombrio = kwargs['shadow']
        self.dano = 0



class Baralho():
    def __init__(self):
        self.cartas = []

    def __repr__(self):
        if len(self.cartas) > 10:
            return super().__repr__()
        repr = ''
        for carta in self.cartas:
            repr += f'{carta.nome}\n'
        return repr        

    @property
    def total(self):
        return len(self.cartas)

    def nova_carta(self, carta: Carta):
        self.cartas.append(carta)

    def retirar(self, nome_carta):
        return next((self.cartas.pop(i) for i, l in enumerate(self.cartas) if l.nome == nome_carta), None)

    def procurar_cartas_por_nome(self, nome):
        return [carta for carta in self.cartas if carta.nome == nome]

    def comprar(self):
        return self.cartas.pop()

class Area(Baralho):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        repr = ''
        for carta in self.cartas:
            repr += f'{carta.nome}\n'
        return repr


class Mão(UserList):
    def index(self, valor):
        for count, value in enumerate(self.data):
            if value.nome == valor:
                return count
        else:
            raise ValueError

class Jogador():
    def __init__(self, nome = 'Jogador 1'):
        self.nome = nome
        self.deck_de_jogador = None
        self.deck_de_herois = None
        # espaço de jogo
        self.hand = Mão()
        self.deck_de_compra = None
        self.deck_de_descarte = None
        self.descarte = Baralho()
        self.herois_em_jogo = Area()
        self.mesa = Area()
        self.jogo: Jogo = None
        self.total_ameaça = 0

    def usar_decks(self, deck_de_herois, deck_de_jogador):
        self.deck_de_herois = deck_de_herois
        self.deck_de_jogador = deck_de_jogador
        self.herois_em_jogo = Baralho()
        self.herois_em_jogo.cartas = self.deck_de_herois.cartas[:]
        self.deck_de_compra = Baralho()
        self.deck_de_compra.cartas = self.deck_de_jogador.cartas[:]
        self.total_ameaça = self.ameaça_inicial

    @property
    def mão(self):
        return self.hand

    def _posicao_na_mao(self, posicao):
        carta = self.hand[posicao - 1]
        print(carta)

    @property
    def h1(self):
        self._posicao_na_mao(1)

    @property
    def h2(self):
        self._posicao_na_mao(2)

    @property
    def h3(self):
        self._posicao_na_mao(3)

    @property
    def h4(self):
        self._posicao_na_mao(4)

    @property
    def h5(self):
        self._posicao_na_mao(5)

    @property
    def h6(self):
        self._posicao_na_mao(6)

    @property
    def h7(self):
        self._posicao_na_mao(7)

    @property
    def hfim(self):
        quantidade = len(self.hand)
        self._posicao_na_mao(quantidade)

    def h(self, posicao):
        self._posicao_na_mao(posicao)

    @property
    def ameaça_inicial(self):
        return sum(h.custo_ameaça for h in self.deck_de_herois.cartas)

    def embaralhar_deck(self):
        random.shuffle(self.deck_de_compra.cartas)

    def comprar_mão_inicial(self):
        self.hand = Mão(self.deck_de_compra.cartas[0:6])
        self.deck_de_compra.cartas = self.deck_de_compra.cartas[6:]

    def comprar(self):
        self.hand.extend(self.deck_de_compra.cartas[0:1])
        self.deck_de_compra.cartas = self.deck_de_compra.cartas[1:]

    def adicionar_recursos(self):
        for heroi in self.herois_em_jogo.cartas:
            heroi.adicionar_recurso()

    def jogar(self, nome_carta):
        pos = self.hand.index(nome_carta)
        carta = self.hand.pop(pos)
        if not carta:
            raise Exception
        self.mesa.nova_carta( carta )

    def pagar_de(self, heroi, quantidade):
        for count, value in enumerate( self.herois_em_jogo.cartas):
            if value.nome == heroi:
                self.herois_em_jogo.cartas[count].recursos -= quantidade
                break

    @property
    def recursos(self):
        leadership = lore = spirit = tactics = 0
        for heroi in self.herois_em_jogo.cartas:
            if heroi.is_leadership:
                leadership += heroi.recursos
            if heroi.is_lore:
                lore += heroi.recursos
            if heroi.is_spirit:
                spirit += heroi.recursos
            if heroi.is_tactics:
                tactics += heroi.recursos
        texto = ''
        texto += f'Leadership: {leadership}\n'
        texto += f'Lore: {lore}\n'
        texto += f'Spirit: {spirit}\n'
        texto += f'Tactics: {tactics}'
        print(texto)
        return texto

    def _herois_em_linha(self):
        texto = ''
        for heroi in self.herois_em_jogo.cartas:
            texto += f'{heroi.nome} ({heroi.recursos}) '
        return texto

    def __repr__(self):
        texto = '-------------------\n'
        texto += f'Jogador: {self.nome}\n'
        texto += f'Ameaça: {self.total_ameaça}\n'
        texto += f'Pontos de Vitória: 0\n'
        texto += f'Primeiro jogador: Sim\n'
        texto += f'Herois: {self._herois_em_linha()}\n'
        texto += '-------------------'
        return texto


class Jogo():
    DECK_DE_ENCONTRO = 'DECK_DE_ENCONTRO'
    DECK_DE_MISSAO = 'DECK_DE_MISSAO'
    FORA_DO_JOGO = 'FORA_DO_JOGO'
    AREA_DE_AMEACA = 'AREA_DE_AMEACA'
    LOCALIZACAO_ATIVA = 'LOCALIZACAO_ATIVA'
    DESCARTE_ENCONTRO = 'DESCARTE_ENCONTRO'

    def __init__(self, colecao = None):
        self.jogadores = []
        self.nome_cenario = ''
        self.locais = {
            Jogo.DECK_DE_ENCONTRO : Baralho(),
            Jogo.DECK_DE_MISSAO : Baralho(),
            Jogo.DESCARTE_ENCONTRO: Baralho(),
            Jogo.FORA_DO_JOGO : Area(),
            Jogo.AREA_DE_AMEACA : Area(),
            Jogo.LOCALIZACAO_ATIVA : Area()
        }
        self.primeiro_jogador = None
        self.colecao = colecao

    def __repr__(self):
        # TODO
        texto = ''
        texto += f'Área de Ameaça ({self.força_ameaça}): \n'
        for carta in self.area_de_ameaca.cartas:
            texto += f'\t{carta.nome} ({carta.tipo})\n'
            for anexo in carta.anexos:
                texto += f'\t\t{anexo.nome} ({anexo.tipo})\n'
        texto += '\n'
        texto += 'Localização Ativa:\n'
        for carta in self.localizacao_ativa.cartas:
            texto += f'\t{carta.nome}\n'
            for anexo in carta.anexos:
                texto += f'\t\t{anexo.nome} ({anexo.tipo})\n'            
        texto += '\n'
        texto += 'Cartas fora do Jogo:\n'
        print(self.fora_do_jogo.cartas)
        for carta in self.fora_do_jogo.cartas:
            texto += f'\t{carta.nome} ({carta.tipo})\n'
        return texto

    @property
    def força_ameaça(self):
        total = 0
        for carta in self.area_de_ameaca.cartas:
            total += carta.força_ameaça
            for anexo in carta.anexos:
                total += anexo.força_ameaça
        return total

    @property
    def deck_de_missao(self):
        return self.locais[Jogo.DECK_DE_MISSAO]

    @deck_de_missao.setter
    def deck_de_missao(self, d):
        self.locais[Jogo.DECK_DE_MISSAO] = d

    @property
    def deck_de_encontro(self):
        return self.locais[Jogo.DECK_DE_ENCONTRO]

    @deck_de_encontro.setter
    def deck_de_encontro(self, d):
        self.locais[Jogo.DECK_DE_ENCONTRO] = d

    @property
    def fora_do_jogo(self):
        return self.locais[Jogo.FORA_DO_JOGO]

    @fora_do_jogo.setter
    def fora_do_jogo(self, a):
        self.locais[Jogo.FORA_DO_JOGO] = a

    @property
    def area_de_ameaca(self):
        return self.locais[Jogo.AREA_DE_AMEACA]

    @area_de_ameaca.setter
    def area_de_ameaca(self, a):
        self.locais[Jogo.AREA_DE_AMEACA] = a

    @property
    def localizacao_ativa(self):
        return self.locais[Jogo.LOCALIZACAO_ATIVA]

    @localizacao_ativa.setter
    def localizacao_ativa(self, a):
        self.locais[Jogo.LOCALIZACAO_ATIVA] = a

    def novo_jogador(self, nome):
        novo = Jogador(nome)
        novo.jogo = self
        self.jogadores.append(novo)
        return novo

    @property
    def jogador1(self):
        return self.jogadores[0] if self.jogadores else None

    @property
    def jogador2(self):
        return self.jogadores[1] if self.jogadores and len(self.jogadores) > 1 else None

    def escolher_cenario(self,nome, deck_de_missao, deck_de_encontro):
        self.nome_cenario = nome
        self.deck_de_missao = deck_de_missao
        self.deck_de_encontro = deck_de_encontro

    def mover_carta(self, nome_carta, origem, destino):
        deck_origem = self.locais[origem]
        deck_destino = self.locais[destino]
        carta = deck_origem.retirar(nome_carta)
        deck_destino.nova_carta(carta)
        return carta

    def embaralhar_deck_encontro(self):
        random.shuffle(self.deck_de_encontro.cartas)

    def setup(self):
        preparacao = CENARIOS_CONJUNTOS[self.nome_cenario]['setup']
        preparacao(self)

    def prepara_jogador(self, nome, codigo_deck):
        jogador = self.novo_jogador(nome)
        jogador.usar_decks(*self.colecao.pegar_deck_jogador(codigo_deck))
        return jogador

    def enfrentar_cenario(self, nome_cenario):
        self.nome_cenario = nome_cenario
        d1, d2 = loader.carregar_deck_cenario(nome_cenario)
        self.deck_de_missao = d1
        self.deck_de_encontro = d2
        self.embaralhar_deck_encontro()

    def ler(self, nome):
        encontradas = []
        for carta in self.area_de_ameaca.cartas:
            if nome in carta.nome:
                encontradas.append(carta)
            for anexo in carta.anexos:
                if nome in anexo.nome:
                    encontradas.append(anexo)                
        for jogador in self.jogadores:
            for heroi in jogador.herois_em_jogo.cartas:
                if nome in heroi.nome:
                    encontradas.append(heroi)
            for carta in jogador.mesa.cartas:
                if nome in carta.nome:
                    encontradas.append(carta)
        for encontrada in encontradas:
            print(encontrada)
            print('------------------------\n')

class Colecao():

    def __init__(self):
        self.decks = rep.encontra_decks()

    def __repr__(self):
        repr = ''
        for deck in self.decks:
            repr += f'{deck.id}) {deck.name}\n'
        return repr

    def cenarios(self):
        return list(CENARIOS_CONJUNTOS.keys())

    def pegar_deck_jogador(self, codigo):
        return loader.carregar_deck(codigo)