from abc import ABC, abstractmethod

class Sujeito(ABC):

    @abstractmethod
    def anexar(self, observador: Observador) -> None:
        pass

    @abstractmethod
    def desanexar(self, observador: Observador) -> None:
        pass

    @abstractmethod
    def notificar(self) -> None:
        pass

class Observador(ABC):

    @abstractmethod
    def update(self, sujeito: Sujeito) -> None:
        pass