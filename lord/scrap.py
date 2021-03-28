import sys
import re
import json

import requests
from bs4 import BeautifulSoup

from . import Hero, Card, Deck

def montar_parser_url(link):
    r = requests.get(link)
    return BeautifulSoup(r.text, 'html.parser')

def pegar_deck_jogador(link):
    soup = montar_parser_url(link)
    script_json = soup.find_all('script',type='text/javascript')[1].contents[0]
    pattern = r'app.deck.init\((?P<deck>.*)\)'
    m = re.search(pattern, str(script_json))
    if m:
        return json.loads(m.group('deck'))
    return {}

def pegar_heroi(soup) -> dict:
    carta = {}
    props = soup.find('span','card-props')
    texto = props.contents[0]
    carta['threat'] = ''.join([c for c in texto if c.isdigit()])
    stats = props.contents[1]
    texto = stats.contents[0]
    carta['willpower'] = ''.join([c for c in texto if c.isdigit()])
    texto = stats.contents[2]
    carta['attack'] = ''.join([c for c in texto if c.isdigit()])
    texto = stats.contents[4]
    carta['defense'] = ''.join([c for c in texto if c.isdigit()])
    texto = stats.contents[6]
    carta['health'] = ''.join([c for c in texto if c.isdigit()])
    return carta

def pegar_aliado(soup) -> dict:
    carta = {}
    props = soup.find('span','card-props')
    texto = props.contents[0]
    carta['cost'] = ''.join([c for c in texto if c.isdigit()])
    stats = props.contents[1]
    texto = stats.contents[0]
    carta['willpower'] = ''.join([c for c in texto if c.isdigit()])
    texto = stats.contents[2]
    carta['attack'] = ''.join([c for c in texto if c.isdigit()])
    texto = stats.contents[4]
    carta['defense'] = ''.join([c for c in texto if c.isdigit()])
    texto = stats.contents[6]
    carta['health'] = ''.join([c for c in texto if c.isdigit()])
    return carta

def pegar_contrato(soup: BeautifulSoup) -> dict:
    carta = {}
    props = soup.find('span','card-props')
    texto = props.contents[0]
    carta['cost'] = ''.join([c for c in texto if c.isdigit()])
    return carta

def pegar_acessorio(soup: BeautifulSoup) -> dict:
    carta = {}
    props = soup.find('span','card-props')
    texto = props.contents[0]
    carta['cost'] = ''.join([c for c in texto if c.isdigit()])
    return carta

def pegar_evento(soup: BeautifulSoup) -> dict:
    carta = {}
    props = soup.find('span','card-props')
    texto = props.contents[0]
    carta['cost'] = ''.join([c for c in texto if c.isdigit()])
    return carta

def pegar_missao_jogador(soup: BeautifulSoup) -> dict:
    carta = {}
    props = soup.find('span','card-props')
    texto = props.contents[0]
    carta['cost'] = ''.join([c for c in texto if c.isdigit()])
    stats = props.contents[1]
    texto = stats.contents[0]
    carta['victory'] = ''.join([c for c in texto if c.isdigit()])
    return carta

def pegar_carta(link: str) -> dict:
    carta = {}
    soup = montar_parser_url(link)
    card_type = soup.find('span','card-type').string.replace('.','')
    carta['card-type'] = card_type
    texto = soup.find('span','card-name').string
    carta['card-name'] = texto
    if card_type in ['Contract','Player Side Quest']:
        texto = ''.join([ str(x) for x in soup.find('div','card-text').contents ])
    else:
        texto = str( soup.find('div','card-text').contents[0] )
    carta['text'] = texto
    texto = soup.find('p','card-traits').string if soup.find('p','card-traits') else ''
    carta['traits'] = texto
    texto = soup.find('span','card-pack').string if soup.find('span','card-pack') else ''
    carta['pack'] = texto
    texto = soup.find('span','card-sphere').string if soup.find('span','card-sphere') else ''
    carta['sphere'] = texto
    if card_type == 'Ally':
        carta.update(pegar_aliado(soup))
    if card_type == 'Hero':
        carta.update(pegar_heroi(soup))
    if card_type == 'Contract':
        carta.update(pegar_contrato(soup))
    if card_type == 'Attachment':
        carta.update(pegar_acessorio(soup))
    if card_type == 'Event':
        carta.update(pegar_evento(soup))
    if card_type == 'Player Side Quest':
        carta.update(pegar_missao_jogador(soup))
    return carta
