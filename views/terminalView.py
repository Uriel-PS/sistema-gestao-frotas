from controllers.frotaController import FrotaController
from patterns.estados import TransicaoInvalidaError
from models.pessoa import PermissaoNegadaError


class CLI:
    """
    View do sistema, interface de linha de comando (RNF04).
    Só exibe dados e lê inputs, toda lógica fica no controller
    """

    def __init__(self):
        self.controller = FrotaController()
        self._dados_iniciais()

    def iniciar(self):
        print("=== Sistema de Gestão de Frotas ===")
        self._tela_login()

    # Login
    def _tela_login(self):
        while True:
            print("\n--- Login ---")
            login = input("Login: ").strip() #.strip remove caracteres em branco
            senha = input("Senha: ").strip()

            usuario = self.controller.login(login, senha)
            if usuario:
                print(f"\nBem-vindo, {usuario.nome} ({usuario.perfil()})!")
                if usuario.perfil() == "Gestor":
                    self._menu_gestor()
                else:
                    self._menu_motorista()
            else:
                print("Login ou senha inválidos.")


    # Menu Gestor
    def _menu_gestor(self):
        opcoes = {
            "1": ("Cadastrar veículo",         self._cadastrar_veiculo),
            "2": ("Alterar estado do veículo", self._alterar_estado),
            "3": ("Registrar abastecimento",   self._registrar_abastecimento),
            "4": ("Registrar manutenção",      self._registrar_manutencao),
            "5": ("Cadastrar motorista",       self._cadastrar_motorista),
            "6": ("Cadastrar oficina",         self._cadastrar_oficina),
            "7": ("Ver dashboard",             self._ver_dashboard),
            "8": ("Ver alertas",               self._ver_alertas),
            "9": ("Listar veículos",           self._listar_veiculos),
            "0": ("Sair",                      None),
        }
        self._executar_menu(opcoes)


    # Menu Motorista
    def _menu_motorista(self):
        opcoes = {
            "1": ("Registrar abastecimento", self._registrar_abastecimento),
            "0": ("Sair",                    None),
        }
        self._executar_menu(opcoes)

    # Ações Gestor
    def _cadastrar_veiculo(self):
        print("\n--- Cadastrar Veículo ---")
        placa    = input("Placa: ").strip().upper()
        modelo   = input("Modelo: ").strip()
        cap      = float(input("Capacidade de carga (kg): "))
        km       = float(input("Km atual (hodômetro): "))
        try:
            v = self.controller.cadastrarVeiculo(placa, modelo, cap, km)
            print(f"Veículo {v.placa} cadastrado com sucesso.")
        except Exception as e:
            print(f"Erro: {e}")

    def _alterar_estado(self):
        print("\n--- Alterar Estado do Veículo ---")
        placa = input("Placa: ").strip().upper()
        print("1. Iniciar operação")
        print("2. Iniciar manutenção")
        print("3. Finalizar manutenção")
        op = input("Opção: ").strip()
        acoes = {
            "1": "iniciar_operacao",
            "2": "iniciar_manutencao",
            "3": "finalizar_manutencao",
        }
        if op not in acoes:
            print("Opção inválida.")
            return
        try:
            self.controller.alterarEstadoVeiculo(placa, acoes[op])
            print("Estado alterado com sucesso.")
        except (TransicaoInvalidaError, ValueError) as e:
            print(f"Erro: {e}")

    # AMBOS (GESTOR E MOTORISTA)
    def _registrar_abastecimento(self):
        print("\n--- Registrar Abastecimento ---")
        placa      = input("Placa do veículo: ").strip().upper()
        combustivel = input("Tipo de combustível: ").strip()
        litros     = float(input("Litros abastecidos: "))
        valor      = float(input("Valor total (R$): "))
        km         = float(input("Km no momento: "))
        try:
            self.controller.registrarAbastecimento(
                placa, combustivel, litros, valor, km
            )
            print("Abastecimento registrado com sucesso.")
            self._exibir_alertas()
        except Exception as e:
            print(f"Erro: {e}")

    def _registrar_manutencao(self):
        print("\n--- Registrar Manutenção ---")
        placa   = input("Placa do veículo: ").strip().upper()
        tipo    = input("Tipo (preventiva/corretiva): ").strip()
        pecas   = input("Peças trocadas / serviço: ").strip()
        custo   = float(input("Custo total (R$): "))
        km      = float(input("Km no momento: "))

        if not self.controller.listarOficinas():
            print("Nenhuma oficina cadastrada. Cadastre uma oficina primeiro.")
            return

        print("Oficinas disponíveis:")
        for o in self.controller.listarOficinas():
            print(f"  - {o.nome}")
        oficina = input("Nome da oficina: ").strip()

        try:
            self.controller.registrarManutencao(
                placa, tipo, pecas, custo, km, oficina
            )
            print("Manutenção registrada com sucesso.")
        except Exception as e:
            print(f"Erro: {e}")

    def _cadastrar_motorista(self):
        print("\n--- Cadastrar Motorista ---")
        nome  = input("Nome: ").strip()
        cpf   = input("CPF: ").strip()
        login = input("Login: ").strip()
        senha = input("Senha: ").strip()
        cnh   = input("CNH: ").strip()
        try:
            self.controller.cadastrarMotorista(nome, cpf, login, senha, cnh)
            print("Motorista cadastrado com sucesso.")
        except Exception as e:
            print(f"Erro: {e}")

    def _cadastrar_oficina(self):
        print("\n--- Cadastrar Oficina ---")
        nome     = input("Nome: ").strip()
        cnpj     = input("CNPJ/CPF: ").strip()
        telefone = input("Telefone: ").strip()
        endereco = input("Endereço: ").strip()
        try:
            self.controller.cadastrarOficina(nome, cnpj, telefone, endereco)
            print("Oficina cadastrada com sucesso.")
        except Exception as e:
            print(f"Erro: {e}")

    def _ver_dashboard(self):
        print("\n--- Dashboard ---")
        placa = input("Placa do veículo: ").strip().upper()
        try:
            r = self.controller.verDashboard(placa)
            print(f"\nVeículo:              {r.placa}")
            print(f"Custo por km (CPK):   R$ {r.custoPorKm:.2f}")
            print(f"Média de consumo:     {r.mediaConsumo:.2f} km/L")
            print(f"Total combustível:    R$ {r.totalGastoCombustivel:.2f}")
            print(f"Total manutenção:     R$ {r.totalGastoManutencao:.2f}")
            if r.detalhes:
                print("Observações:")
                for d in r.detalhes:
                    print(f"  - {d}")
        except Exception as e:
            print(f"Erro: {e}")

    def _ver_alertas(self):
        print("\n--- Alertas de Manutenção ---")
        alertas = self.controller.verAlertas()
        if not alertas:
            print("Nenhum alerta no momento.")
        else:
            for a in alertas:
                print(a)

    def _listar_veiculos(self):
        print("\n--- Veículos Ativos ---")
        veiculos = self.controller.listarVeiculos()
        if not veiculos:
            print("Nenhum veículo cadastrado.")
        else:
            for v in veiculos:
                print(f"  {v.placa} | {v.modelo} | "
                      f"Estado: {v.estadoAtual} | Km: {v.kmAtual}")


    # Funções auxiliares
    def _executar_menu(self, opcoes: dict):
        while True:
            print("\n--- Menu ---")
            for k, (desc, _) in opcoes.items():
                print(f"  {k}. {desc}")
            escolha = input("Opção: ").strip()
            if escolha == "0":
                self.controller.logout()
                print("Sessão encerrada.")
                break
            elif escolha in opcoes:
                try:
                    opcoes[escolha][1]()
                except PermissaoNegadaError as e:
                    print(f"Acesso negado: {e}")
            else:
                print("Opção inválida.")

    def _exibir_alertas(self):
        """Exibe alertas pendentes logo após um abastecimento."""
        try:
            alertas = self.controller.verAlertas()
            for a in alertas:
                print(a)
        except PermissaoNegadaError:
            pass

    def _dados_iniciais(self):
        """Cria um gestor padrão para o sistema poder ser usado imediatamente."""
        self.controller.cadastrarGestor(
            nome="Administrador",
            cpf="000.000.000-00",
            login="admin",
            senha="admin123",
            email="admin@frota.com",
        )

        # simulando login
        self.controller.login("admin", "admin123")

        # cadastro motorista (gestor logado)
        self.controller.cadastrarMotorista(
            nome="João Motorista",
            cpf="111.111.111-11",
            login="joao",
            senha="123",
            cnh="AB123456"
        )

        # cadastro oficina
        self.controller.cadastrarOficina(
            nome="Mecânica Diesel Express",
            cnpj="12.345.678/0001-99",
            telefone="(11) 99999-9999",
            endereco="Rua das Engrenagens, 100"
        )

        # CRIANDO VEÍCULOS 

        # CRIANDO CAMINHÃO 1 (normal, testar cálculos)
        self.controller.cadastrarVeiculo("ABC-1234", "Volvo", 20000.0, 1000.0)
        # Abastecimento 1: Enchendo o tanque
        self.controller.registrarAbastecimento(
            placa="ABC-1234", tipoCombustivel="Diesel", litros=200.0, valorTotal=1000.0, kmNoMomento=1000.0
        )
        # Abastecimento 2: Andou 500km (Média deve dar 5km/L)
        self.controller.registrarAbastecimento(
            placa="ABC-1234", tipoCombustivel="Diesel", litros=100.0, valorTotal=500.0, kmNoMomento=1500.0
        )

        # Manutenção: Custo fixo
        self.controller.registrarManutencao(
            placa="ABC-1234", tipo="preventiva", pecasTrocadas="Filtros de Óleo", 
            custoTotal=800.0, kmDaManutencao=1500.0, nome_oficina="Mecânica Diesel Express"
        )

        # CRIANDO CAMINHÃO 2 (testar padrão state)
        self.controller.cadastrarVeiculo("DEF-5678", "Mercedes", 15000.0, 5000.0)
        # Mudando estado para manutenção 
        self.controller.alterarEstadoVeiculo("DEF-5678", "iniciar_manutencao")

        # CRIANDO O CAMINHÃO 3 (testar observer)
        # Nasce com 0km, o limite de revisão será 10.000km.
        self.controller.cadastrarVeiculo("XYZ-9876", "Scania", 25000.0, 0.0)
        # Abastecimento que estoura o limite do hodômetro e aciona o Observer silenciosamente!
        self.controller.registrarAbastecimento(
            placa="XYZ-9876", tipoCombustivel="Diesel", litros=400.0, valorTotal=2000.0, kmNoMomento=10050.0
        )

        # DESLOGAR O GESTOR
        self.controller.logout()