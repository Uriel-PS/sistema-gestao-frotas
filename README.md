# Sistema de Gestão de Frotas

Projeto da disciplina de Engenharia de Software (UDESC/CCT — Bacharelado em
Ciência da Computação). Implementa o backend de um sistema de controle de
frotas de veículos, com regras de negócio para abastecimento, manutenção,
controle de status dos veículos e cálculo de indicadores de custo.

## Sumário

- [Arquitetura](#arquitetura)
- [Padrões de projeto utilizados](#padrões-de-projeto-utilizados)
- [Como executar o sistema](#como-executar-o-sistema)
- [Como executar os testes](#como-executar-os-testes)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Usuário padrão (dados de exemplo)](#usuário-padrão-dados-de-exemplo)
- [Rastreabilidade com os requisitos](#rastreabilidade-com-os-requisitos)

## Arquitetura

O projeto segue o padrão **MVC (Model-View-Controller)**:

- **`models/`** — as classes de domínio (regras de negócio puras): `Veiculos`,
  `Pessoa`/`Motorista`/`Gestor`, `Abastecimento`, `Manutencao`, `Oficina` e
  `Dashboard`. Não dependem de nada de interface — podem ser testadas
  isoladamente.
- **`patterns/`** — as interfaces e classes que implementam os padrões de
  projeto **State** e **Observer**, usadas pelos models.
- **`controllers/`** — a classe `FrotaController`, que recebe ações da
  *view*, aciona os *models* corretos e devolve o resultado. É também onde
  ficam as regras de **controle de acesso por perfil** (RNF07), como exigir
  que o usuário logado seja Gestor antes de cadastrar um veículo.
- **`views/`** — a classe `CLI` (`terminalView.py`), responsável apenas por
  exibir menus e capturar entradas do teclado. Não contém lógica de negócio:
  toda decisão é delegada ao controller.

```
View (CLI)  →  Controller (FrotaController)  →  Models (Veiculos, Pessoa, ...)
                                                       ↑
                                              Patterns (State, Observer)
```

## Padrões de projeto utilizados

### State (Estado)

Implementado em `patterns/estados.py`. Controla o status de um veículo
(Disponível, Em Operação, Em Manutenção) e impede transições inválidas —
em especial, a restrição central do projeto: **um veículo não pode iniciar
uma operação enquanto estiver em manutenção**. Cada estado concreto
(`EstadoDisponivel`, `EstadoEmOperacao`, `EstadoEmManutencao`) sabe para qual
estado pode transicionar e lança `TransicaoInvalidaError` quando a
transição pedida não é permitida.

### Observer (Observador)

Implementado em `patterns/observer.py`. A classe `Veiculos` é o `Subject`:
mantém uma lista de observadores e os notifica via `notificar()`. A classe
`Gestor` implementa `Observer` (método `atualizar()`), recebendo um alerta
automático sempre que a quilometragem do veículo atinge o limite da
próxima revisão durante um abastecimento.

## Como executar o sistema

Pré-requisito: Python 3.10 ou superior.

Na pasta raiz do projeto (onde está o `main.py`):

```bash
python main.py
```

Isso abre a CLI do sistema com um conjunto de dados de exemplo já
carregado (veja a seção [Usuário padrão](#usuário-padrão-dados-de-exemplo)
abaixo), permitindo logar e navegar pelos menus de Gestor ou Motorista.

> No Windows, se o comando `python` não for reconhecido, tente `py main.py`.

## Como executar os testes

O projeto usa **pytest**. A única dependência externa é o próprio pytest
(e, opcionalmente, `pytest-cov` para relatório de cobertura).

```bash
pip install pytest pytest-cov
```

Rodar todos os testes:

```bash
pytest
```

Rodar com o nome de cada teste individualmente (recomendado para
acompanhar a execução):

```bash
pytest -v
```

Rodar com relatório de cobertura de código:

```bash
pytest --cov=models --cov=patterns --cov=controllers --cov-report=term-missing
```

**Resultado atual:** **32 testes**, 100% aprovados.

| Arquivo de teste | Quantidade | Cobre |
|---|---|---|
| `test_veiculos.py` | 8 | `Veiculos`: padrão State, padrão Observer, atualização de hodômetro |
| `test_pessoa.py` | 5 | Autenticação, perfis, recebimento de alertas pelo Gestor |
| `test_dashboard.py` | 7 | Cálculo de CPK, média de consumo, geração de relatório |
| `test_abastecimento.py` | 4 | Validações de criação (litros/valor negativos ou zero) |
| `test_manutencao.py` | 4 | Validações de tipo e quilometragem |
| `test_oficina.py` | 2 | Fábrica de cadastro e geração de IDs |
| `test_frotacontroller.py` | 2 | Login e bloqueio de ações restritas ao Gestor |
| **Total** | **32** | |

> **Nota sobre cobertura:** os `models/` e `patterns/` (onde está a lógica
> de negócio e os padrões de projeto) têm cobertura entre 67% e 100%,
> concentrada nos métodos mais críticos — cálculo de indicadores
> (`Dashboard`), transições de estado e disparo de alertas. O
> `controllers/frotaController.py` tem cobertura mais baixa (~52%), pois os
> testes atuais focam o controller apenas no fluxo de login e no bloqueio
> de permissão (RNF07); os demais métodos do controller são, em sua
> maioria, repasses diretos para os models já testados individualmente.

## Estrutura do repositório

```
gestao_frotas/
├── main.py                       # ponto de entrada: inicia a CLI
├── pytest.ini                    # configuração do pytest
├── conftest.py                   # (vazio, necessário para o pytest localizar a raiz)
├── models/
│   ├── veiculos.py                # classe Veiculos (Subject do Observer)
│   ├── pessoa.py                  # Pessoa, Motorista, Gestor (Observer)
│   ├── abastecimento.py
│   ├── manutencao.py
│   ├── oficina.py
│   └── dashboard.py                # cálculo de CPK e consumo médio
├── patterns/
│   ├── estados.py                  # padrão State
│   └── observer.py                 # padrão Observer
├── controllers/
│   └── frotaController.py         # camada de controle (MVC)
├── views/
│   └── terminalView.py            # CLI (RNF04)
└── tests/
    ├── conftest.py                 # fixtures compartilhadas entre os testes
    ├── test_veiculos.py
    ├── test_pessoa.py
    ├── test_dashboard.py
    ├── test_abastecimento.py
    ├── test_manutencao.py
    ├── test_oficina.py
    └── test_frotacontroller.py
```

## Usuário padrão (dados de exemplo)

Ao iniciar o sistema (`python main.py`), os seguintes dados já são criados
automaticamente para facilitar os testes manuais:

- **Gestor padrão:** login `admin`, senha `admin123`
- **Motorista de exemplo:** login `joao`, senha `123`
- **Oficina de exemplo:** "Mecânica Diesel Express"
- **Três veículos de exemplo**, já configurados para demonstrar:
  - `ABC-1234`: cálculo normal de CPK e média de consumo (5 km/L esperado)
  - `DEF-5678`: já em estado "Em Manutenção" (para testar o padrão State)
  - `XYZ-9876`: abastecimento que ultrapassa o limite de revisão, disparando
    o alerta automático (para testar o padrão Observer)

## Rastreabilidade com os requisitos

| Requisito | Onde está implementado |
|---|---|
| RF01 – Gerenciamento de Veículos | `Veiculos.editar()`, `Veiculos.inativar()`, `FrotaController.cadastrarVeiculo()` |
| RF02 – Controle de Estado do Veículo | `patterns/estados.py` (padrão State) |
| RF03 – Registro de Abastecimentos | `Abastecimento`, `Veiculos.registrarAbastecimento()` |
| RF04 – Registro de Manutenções | `Manutencao`, `Veiculos.registrarManutencao()` |
| RF05 – Sistema de Alertas | `patterns/observer.py`, `Gestor.atualizar()` (padrão Observer) |
| RF06 – Cálculo de Indicadores (Dashboard) | `Dashboard.calcularCustoPorKm()`, `calcularMediaConsumo()`, `gerarRelatorio()` |
| RF07 – Gerenciamento de Usuários | `FrotaController.cadastrarMotorista()`, `cadastrarGestor()`, `inativarUsuario()` |
| RF08 – Autenticação no Sistema | `Pessoa.autenticar()`, `FrotaController.login()` |
| RF09 – Cadastro de Oficinas Parceiras | `Oficina`, `FrotaController.cadastrarOficina()` |
| RNF04 – Interface de Linha de Comando | `views/terminalView.py` |
| RNF05 – Restrição de Transição de Estado | `patterns/estados.py` (`TransicaoInvalidaError`) |
| RNF06 – Atualização Automática de Hodômetro | `Veiculos.registrarAbastecimento()` |
| RNF07 – Controle de Acesso por Perfil | `FrotaController._exigir_gestor()`, `Pessoa.perfil()` |
