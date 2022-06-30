import sys
import re
import json

import requests
from bs4 import BeautifulSoup

def montar_parser_url(link):
    r = requests.get(link)
    return BeautifulSoup(r.text, 'html.parser')

def pegar_carta_jogador(codigo: str) -> dict:
    r = requests.get(f'https://ringsdb.com/api/public/card/{codigo}.json')
    if r.status_code == 200:
        return r.json()
    return {}

def pegar_cartas_jogador_por_pacote(codigo: str) -> dict:
    r = requests.get(f'https://ringsdb.com/api/public/cards/{codigo}.json')
    if r.status_code == 200:
        return r.json()
    return {}

def pegar_deck_jogador(codigo: str) -> dict:
    r = requests.get(f'https://ringsdb.com/api/public/decklist/{codigo}.json')
    if r.status_code == 200:
        return r.json()
    return {}

def pegar_deck_aventura(codigo: str) -> dict:
    r = requests.get(f'https://ringsdb.com/api/public/scenario/{codigo}.json')
    if r.status_code == 200:
        return r.json()
    return {}

def pegar_packs() -> dict:
    r = requests.get(f'https://ringsdb.com/api/public/packs')
    if r.status_code == 200:
        return r.json()
    return {}

