from abc import ABC, abstractmethod
from patterns.observer import Observer # gestor implementa observer


class Pessoa(ABC): # pessoa (abstract)
    _proximo_id = 1

    def __init__(self, nome: str, cpf: str, login: str, senha: str) -> None:
        self.__id = Pessoa._proximo_id
        Pessoa._proximo_id += 1
        self.__nome = nome
        self.cpf = cpf
        self.__login = login
        self.__senha = senha
        self.__ativo = True

    @property
    def ativo(self):
        return self.__ativo
    
    @property
    def nome(self):
        return self.__nome

    @property
    def login(self):
        return self.__login

    def autenticar(self, senha: str) -> bool:
        if not self.__ativo:
            return False
        return self.__senha == senha

    def editar(self, dados: dict) -> None:
        campos_validos = {"nome", "cpf", "login", "senha"}
        for chave, valor in dados.items():
            if chave in campos_validos:
                setattr(self, f"_Pessoa__{chave}", valor)

    def inativar(self) -> None:
        self.__ativo = False

    @abstractmethod
    def perfil(self) -> str:
        raise NotImplementedError


class PermissaoNegadaError(Exception):
    """Lançada quando um usuário tenta executar ação fora do seu perfil (RNF07)."""


class Motorista(Pessoa): # Herda Pessoa
    def __init__(self, nome: str, cpf: str,
                 login: str, senha: str, cnh: str) -> None:
        super().__init__(nome, cpf, login, senha)
        self.__cnh = cnh

    @property
    def cnh(self) -> str:
        return self.__cnh

    def perfil(self) -> str:
        return "Motorista"


class Gestor(Pessoa, Observer): # herda pessoa e assina observer
    def __init__(self, nome: str, cpf: str,
                 login: str, senha: str, emailContato: str) -> None:
        super().__init__(nome, cpf, login, senha)
        self.__emailContato = emailContato
        self.__alertas_recebidos: list = []

    @property
    def alertas_recebidos(self):
        return self.__alertas_recebidos

    def atualizar(self, veiculo) -> None: # RF05
        mensagem = (
            f"[ALERTA] Veículo {veiculo.placa} atingiu {veiculo.kmAtual} km "
            f"(limite de revisão: {veiculo.kmProximaRevisao} km)."
        )
        self.__alertas_recebidos.append(mensagem)

    def acessarDashboard(self, dashboard) -> None:
        if not self.ativo:
            raise PermissaoNegadaError("Gestor inativo não pode acessar o dashboard.")
        return dashboard

    def cadastrarUsuario(self, p) -> None:
        if not isinstance(p, Pessoa): # verifica se p é do 'tipo' Pessoa
            raise TypeError("Apenas instâncias de Pessoa podem ser cadastradas.")

    def inativarUsuario(self, p) -> None:
        p.inativar()

    def cadastrarOficina(self, o) -> None:
        from models.oficina import Oficina
        if not isinstance(o, Oficina):
            raise TypeError("Oficina inválida.")

    def perfil(self) -> str:
        return "Gestor"