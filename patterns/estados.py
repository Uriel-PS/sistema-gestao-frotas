from abc import ABC, abstractmethod
# Implementação do RF02 (Controle de Estados do Veículo) e RNF05 (Restrição de Transição de Estado)

class TransicaoInvalidaError(Exception):
    """Lançada quando uma transição de estado não é permitida (RNF05)."""


class EstadoVeiculo(ABC):
    @abstractmethod
    def inicializarOperacao(self, v) -> None:
        raise NotImplementedError

    @abstractmethod
    def finalizarManutencao(self, v) -> None:
        raise NotImplementedError

    @abstractmethod
    def iniciarManutencao(self, v) -> None:
        raise NotImplementedError


class EstadoDisponivel(EstadoVeiculo): # Herda de EstadoVeiculo
    def inicializarOperacao(self, v) -> None:
        v.estadoAtual = EstadoEmOperacao() # troca o estado do veiculo

    def iniciarManutencao(self, v) -> None:
        v.estadoAtual = EstadoEmManutencao()

    def finalizarManutencao(self, v) -> None:
        raise TransicaoInvalidaError(
            "Veículo já está disponível; não está em manutenção."
        )

    def __repr__(self): # Método de representação, quando algum método pedir para imprimir um objeto desse tipo, irá imprimir o retorno disso.
        return "EstadoDisponivel"


class EstadoEmOperacao(EstadoVeiculo):
    def inicializarOperacao(self, v) -> None:
        raise TransicaoInvalidaError("Veículo já está em operação.")

    def iniciarManutencao(self, v) -> None:
        v.estadoAtual = EstadoEmManutencao()

    def finalizarManutencao(self, v) -> None:
        raise TransicaoInvalidaError(
            "Veículo está em operação; não está em manutenção."
        )

    def __repr__(self):
        return "EstadoEmOperacao"


class EstadoEmManutencao(EstadoVeiculo):
    def inicializarOperacao(self, v) -> None:
        raise TransicaoInvalidaError(
            "Não é possível iniciar operação: veículo está em manutenção."
        )

    def iniciarManutencao(self, v) -> None:
        raise TransicaoInvalidaError("Veículo já está em manutenção.")

    def finalizarManutencao(self, v) -> None:
        v.estadoAtual = EstadoDisponivel()

    def __repr__(self):
        return "EstadoEmManutencao"