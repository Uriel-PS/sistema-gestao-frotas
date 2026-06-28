from abc import ABC, abstractmethod 
"""
Como não há a palavra "interface" como em JAVA, importamos de ABSTRACT BASE CLASS (classes abstratas)
"""



class Observer(ABC): 
    @abstractmethod # Decorador
    def atualizar(self, veiculo) -> None: # Não retorna nada (None), apenas executa uma ação
        raise NotImplementedError # Se tentar usar diretamente (interface não implementa), dar ERRO


class Subject(ABC):
    @abstractmethod
    def registrar(self, obs: Observer) -> None:
        raise NotImplementedError

    @abstractmethod
    def notificar(self) -> None:
        raise NotImplementedError