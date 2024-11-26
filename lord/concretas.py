from typing import List

from lord import Carta, Jogo
from lord.bases import Sujeito, Observador

class JogoConcreto(Jogo, Sujeito):

    _observadores: List[Observador] = []
    
    def __init__(self, **kwargs):
        Jogo.__init__(self, kwargs)

    def anexar(self, observador: Observador) -> None:
        self._observadores.append(observador)

    def desanexar(self, observador: Observador) -> None:
        return self._observadores.remove(observador)

    def notificar(self) -> None:
        for observador in self._observadores:
            observador.atualizar()

    def comprar(self) -> Carta:
        carta = super().comprar()
        return carta

class CartaConcreta(Carta, Observador):

    def __init__(self, nome, **kwargs):
        Carta.__init__(nome, **kwargs)

    def atualizar(self, sujeito: Sujeito) -> None:
        print('CartaConcreta: reagiu ao evento')
