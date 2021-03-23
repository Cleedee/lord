import sys
import re

from . import Hero, Card, Deck

def procurar_cabecalho_tipo(linhas, tipo):
    for count, linha in enumerate( linhas):
        if tipo in linha:
            quantidade = int(''.join([l for l in linha if l.isdigit()]))
            return quantidade, count
    return None, None

def procurar_heroi(linhas):
    # Heroes \((?P<numero>.*)\)\n
    for count, linha in enumerate( linhas):
        if 'Heroes' in linha:
            quantidade = int(''.join([l for l in linha if l.isdigit()]))
            return quantidade, count
    return None, None

def procurar_aliados(linhas):
    for count, linha in enumerate( linhas):
        if 'Allies' in linha:
            quantidade = int(''.join([l for l in linha if l.isdigit()]))
            return quantidade, count
    return (0,0)

def lista_de_cartas(inicio, fim, linhas):
    return linhas[inicio + 1: fim]

def criar_cartas_herois(lista):
    for i in lista:
        i = i.replace('1x','')
        yield Hero(i.strip(), 0)

def criar_cartas_aliados(lista):
    for i in lista:
        quantidade = int(i[0])
        i = i.replace(f'{quantidade}x','')
        for j in range(quantidade):
            yield Card(i.strip())

def abrir_arquivo(nome_arquivo):
    with open(nome_arquivo,'r') as f:
        linhas = [linha for linha in [
             linha.replace('\n','') for linha in f.readlines()
             ] if linha]
    return linhas

def montar_deck(linhas):
    deck_herois = Deck()
    deck_jogador = Deck()
    num_herois, pos_herois = procurar_cabecalho_tipo(linhas,'Heroes')
    num_aliados, pos_aliados = procurar_cabecalho_tipo(linhas,'Allies')
    num_acessorios, pos_acessorios = procurar_cabecalho_tipo(linhas,'Attachments')
    herois = lista_de_cartas(pos_herois, pos_aliados, linhas)
    herois = criar_cartas_herois(herois)
    for carta in herois:
        deck_herois.nova_carta(carta)
    aliados = lista_de_cartas(pos_aliados, pos_acessorios, linhas)
    aliados = criar_cartas_aliados(aliados)
    for carta in aliados:
        deck_jogador.nova_carta(carta)
    return deck_herois, deck_jogador

if __name__ == "__main__":
    with open(sys.argv[1],'r') as f:
        linhas = [linha for linha in [
             linha.replace('\n','') for linha in f.readlines()
             ] if linha]
    #print('Nome do deck:',linhas[0])
    #print(linhas[1].replace('Packs:','Extensões:'))
    num_herois, pos_herois = procurar_cabecalho_tipo(linhas,'Heroes')
    num_aliados, pos_aliados = procurar_cabecalho_tipo(linhas,'Allies')
    num_acessorios, pos_acessorios = procurar_cabecalho_tipo(linhas,'Attachments')
    herois = lista_de_cartas(pos_herois, pos_aliados, linhas)
    herois = criar_cartas_herois(herois)
    for i in herois:
        print(i.nome)
    aliados = lista_de_cartas(pos_aliados, pos_acessorios, linhas)
    aliados = criar_cartas_aliados(aliados)
    for i in aliados:
        print(i.nome)



    #print(linhas)
