from patterns.observer import Subject, Observer
from patterns.estados import EstadoVeiculo, EstadoDisponivel


class Veiculos(Subject):
    def __init__(self, placa: str, modelo: str,
                 capacidadeCarga: float, kmAtual: float = 0.0) -> None:
        self.__placa = placa
        self.__modelo = modelo
        self.__capacidadeCarga = capacidadeCarga
        self.__kmAtual = kmAtual
        self.__kmProximaRevisao = kmAtual + 10000.0
        self.__estadoAtual: EstadoVeiculo = EstadoDisponivel() # Implementação Padrão State
        self.__observadores: list[Observer] = []
        self.__ativo = True
        # Veiculo pode ter registros de vários abastecimentos ou manuntencoes (Agregação)
        # Começa com underlinwe, modificador PROTECTED (1 underline)
        self.__abastecimentos = [] 
        self.__manutencoes = []

    # Transforma método em getter, funciona igual uma variável normal (sem poder alterar, somente visualizar) mesmo sendo Protected
    @property 
    def abastecimentos(self):
        return tuple(self.__abastecimentos)
    @property
    def manutencoes(self):
        return tuple(self.__manutencoes)

    @property
    def kmAtual(self):
        return self.__kmAtual

    @property
    def placa(self):
        return self.__placa
    
    @property
    def estadoAtual(self):
        return self.__estadoAtual

    @estadoAtual.setter
    def estadoAtual(self, novo_estado):
        self.__estadoAtual = novo_estado

    @property
    def ativo(self):
        return self.__ativo

    @ativo.setter
    def ativo(self, valor):
        self.__ativo = valor

    @property
    def modelo(self):
        return self.__modelo

    @property
    def kmProximaRevisao(self):
        return self.__kmProximaRevisao

    @kmProximaRevisao.setter
    def kmProximaRevisao(self, valor):
        self.__kmProximaRevisao = valor    

    # Implementa os métodos herdados de Subject
    def registrar(self, obs: Observer) -> None:
        if obs not in self.__observadores:
            self.__observadores.append(obs)

    def notificar(self) -> None:
        for obs in self.__observadores:
            obs.atualizar(self)

    # Regras de negócio

    def registrarAbastecimento(self, a) -> None:
        self.__abastecimentos.append(a)
        self.__kmAtual = max(self.__kmAtual, a.kmNoMomento)
        # self.kmAtual = a.kmNoMomento
        if self.__kmAtual >= self.__kmProximaRevisao: # Se passar do limite de quilometragem, notificar para avisar o Gestor
            self.notificar()

    def registrarManutencao(self, m) -> None:
        self.__manutencoes.append(m)
        if m.tipo.lower() == "preventiva":
            self.__kmProximaRevisao = m.kmDaManutencao + 10000.0

    def editar(self, dados: dict) -> None:
        campos_validos = {"placa", "modelo", "capacidadeCarga", "kmProximaRevisao"}
        for chave, valor in dados.items():
            if chave in campos_validos:
                setattr(self, chave, valor) # método para alterar atributo dentro de uma classe (do python), ele faz self.placa = valor; automatico

    def inativar(self) -> None:
        self.ativo = False

    # Métodos Padrão State, delega a responsabilidade para o estado do veículo (a classe)
    def inicializarOperacao(self) -> None:
        self.estadoAtual.inicializarOperacao(self)

    def iniciarManutencao(self) -> None:
        self.estadoAtual.iniciarManutencao(self)

    def finalizarManutencao(self) -> None:
        self.estadoAtual.finalizarManutencao(self)

    def __repr__(self):
        return f"Veiculos(placa={self.__placa!r}, estado={self.__estadoAtual!r})"