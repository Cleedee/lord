from abc import ABC, abstractmethod

class Observador(ABC):

    @abstractmethod
    def atualizar(self) -> None:
        pass

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

