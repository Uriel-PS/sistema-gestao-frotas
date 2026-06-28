from datetime import date
from models.veiculos import Veiculos
from models.pessoa import Gestor, Motorista, PermissaoNegadaError
from models.abastecimento import Abastecimento
from models.manutencao import Manutencao
from models.oficina import Oficina
from models.dashboard import Dashboard
from patterns.estados import TransicaoInvalidaError
# Acoplamento aceitável, interfaces todas estáveis

class FrotaController:
    """
    Camada de controle do sistema (MVC).
    Recebe ações da View, executa nos Models e retorna resultados
    """

    def __init__(self):
        self.__veiculos: list[Veiculos] = []
        self.__usuarios: list = []
        self.__oficinas: list[Oficina] = []
        self.__dashboard = Dashboard()
        self.__usuario_logado = None

    @property
    def veiculos(self):
        return self.__veiculos

    @property
    def usuarios(self):
        return self.__usuarios

    @property
    def oficinas(self):
        return self.__oficinas

    @property
    def usuario_logado(self):
        return self.__usuario_logado

    @usuario_logado.setter
    def usuario_logado(self, valor):
        self.__usuario_logado = valor

    @property
    def dashboard(self):
        return self.__dashboard


    # Autenticação (RF08)
    def login(self, login: str, senha: str):
        for u in self.usuarios: #verifica se existe na lista de usuários cadastrados
            if u.login == login and u.autenticar(senha):
                self.usuario_logado = u
                return u
        return None

    def logout(self):
        self.usuario_logado = None

    def _exigir_gestor(self): #protected
        if not self.usuario_logado or self.usuario_logado.perfil() != "Gestor":
            raise PermissaoNegadaError("Acesso restrito ao Gestor.")


    # Veículos (RF01, RF02)
    def cadastrarVeiculo(self, placa: str, modelo: str,
                         capacidadeCarga: float, kmAtual: float) -> Veiculos:
        self._exigir_gestor()
        v = Veiculos(placa, modelo, capacidadeCarga, kmAtual)
        v.registrar(self.usuario_logado)  # Gestor observa o veículo (RF05)
        self.veiculos.append(v)
        return v

    def inativarVeiculo(self, placa: str) -> None:
        self._exigir_gestor()
        v = self._buscarVeiculo(placa)
        v.inativar()

    def alterarEstadoVeiculo(self, placa: str, acao: str) -> None:
        """
        acao: 'iniciar_operacao' | 'iniciar_manutencao' | 'finalizar_manutencao'
        """
        v = self._buscarVeiculo(placa)
        if acao == "iniciar_operacao":
            v.inicializarOperacao()
        elif acao == "iniciar_manutencao":
            v.iniciarManutencao()
        elif acao == "finalizar_manutencao":
            v.finalizarManutencao()
        else:
            raise ValueError(f"Ação desconhecida: {acao}")

    def listarVeiculos(self) -> list:
        return [v for v in self.veiculos if v.ativo]

    # Abastecimento (RF03)
    def registrarAbastecimento(self, placa: str, tipoCombustivel: str,
                                litros: float, valorTotal: float,
                                kmNoMomento: float) -> Abastecimento:
        v = self._buscarVeiculo(placa)

        # RNF07: apenas motorista ou gestor logado pode registrar
        if not self.usuario_logado:
            raise PermissaoNegadaError("Nenhum usuário logado.")

        motorista = (self.usuario_logado
                     if self.usuario_logado.perfil() == "Motorista"
                     else None)

        a = Abastecimento(
            data=date.today(),
            tipoCombustivel=tipoCombustivel,
            litros=litros,
            valorTotal=valorTotal,
            kmNoMomento=kmNoMomento,
            motorista=motorista,
        )
        v.registrarAbastecimento(a)
        return a


    # Manutenção (RF04)
    def registrarManutencao(self, placa: str, tipo: str, pecasTrocadas: str,
                             custoTotal: float, kmDaManutencao: float,
                             nome_oficina: str) -> Manutencao:
        self._exigir_gestor()
        v = self._buscarVeiculo(placa)
        o = self._buscarOficina(nome_oficina)

        m = Manutencao(
            data=date.today(),
            tipo=tipo,
            pecasTrocadas=pecasTrocadas,
            custoTotal=custoTotal,
            kmDaManutencao=kmDaManutencao,
            oficina=o,
        )
        v.registrarManutencao(m)
        return m


    # Usuários (RF07)
    def cadastrarGestor(self, nome: str, cpf: str, login: str,
                        senha: str, email: str) -> Gestor:
        g = Gestor(nome, cpf, login, senha, email)
        self.usuarios.append(g)
        return g

    def cadastrarMotorista(self, nome: str, cpf: str, login: str,
                           senha: str, cnh: str) -> Motorista:
        self._exigir_gestor()
        m = Motorista(nome, cpf, login, senha, cnh)
        self.usuarios.append(m)
        return m

    def inativarUsuario(self, login: str) -> None:
        self._exigir_gestor()
        u = self._buscarUsuario(login)
        u.inativar()

    # Oficinas (RF09)
    def cadastrarOficina(self, nome: str, cnpj: str,
                         telefone: str, endereco: str) -> Oficina:
        self._exigir_gestor()
        o = Oficina.cadastrarOficina(nome, cnpj, telefone, endereco)
        self.oficinas.append(o)
        return o

    def listarOficinas(self) -> list:
        return self.oficinas


    # Dashboard (RF06)
    def verDashboard(self, placa: str):
        self._exigir_gestor()
        v = self._buscarVeiculo(placa)
        return self.dashboard.gerarRelatorio(v)


    # Alertas do Gestor (RF05)
    def verAlertas(self) -> list:
        self._exigir_gestor()
        return self.usuario_logado.alertas_recebidos


    # Métodos auxiliares
    def _buscarVeiculo(self, placa: str) -> Veiculos:
        for v in self.veiculos:
            if v.placa == placa:
                return v
        raise ValueError(f"Veículo com placa {placa!r} não encontrado.")

    def _buscarOficina(self, nome: str) -> Oficina:
        for o in self.oficinas:
            if o.nome == nome:
                return o
        raise ValueError(f"Oficina {nome!r} não encontrada.")

    def _buscarUsuario(self, login: str):
        for u in self.usuarios:
            if u.login == login:
                return u
        raise ValueError(f"Usuário {login!r} não encontrado.")
    