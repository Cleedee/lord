import sys
import re
import json

import requests
from bs4 import BeautifulSoup

from . import Hero, Card, Deck

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

def pegar_deck_aventura(link: str) -> dict:
    deck = {}
    soup = montar_parser_url(link)
    return deck
