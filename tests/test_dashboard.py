import pytest
from models.dashboard import Dashboard, Relatorio
from models.abastecimento import Abastecimento
from models.manutencao import Manutencao

# 7 TESTES NA CLASSE DASHBOARD

def test_calcular_cpk_sucesso(veiculo, motorista, oficina, hoje):
    # Custo variável (Abastecimento): 1500, Custo fixo (manuntencao): 1500, km = 1500
    # CPK = (1500 + 1500) / 1500 = 2
    veiculo.registrarAbastecimento(Abastecimento(hoje, "Diesel", 200.0, 1500.0, 1500.0, motorista))
    veiculo.registrarManutencao(Manutencao(hoje, "corretiva", "Óleo", 1500.0, 1500.0, oficina))
    cpk = Dashboard().calcularCustoPorKm(veiculo)
    assert cpk == pytest.approx(3000.0 / 1500.0)


def test_calcular_cpk_divisao_por_zero(veiculo): # obs, conftest inicia o veiculo com 0km
    # Veículo com 0 km rodados
    with pytest.raises(ZeroDivisionError): # verifica se o erro do calculo é de ZeroDivisionError (pois km atual = 0)
        Dashboard().calcularCustoPorKm(veiculo)


def test_calcular_media_consumo_sucesso(veiculo, motorista, hoje):
    # 1º abastecimento: ponto de partida (km=1000)
    # 2º abastecimento: andou 500km, gastou 100L --> consumo medio deve ser de 5 km/L
    veiculo.registrarAbastecimento(Abastecimento(hoje, "Diesel", 200.0, 1000.0, 1000.0, motorista))
    veiculo.registrarAbastecimento(Abastecimento(hoje, "Diesel", 100.0, 500.0, 1500.0, motorista))
    media = Dashboard().calcularMediaConsumo(veiculo)
    assert media == pytest.approx(5.0)


def test_calcular_media_falta_de_dados(veiculo, motorista, hoje):
    # Apenas 1 abastecimento: insuficiente para calcular (precisa de dois)
    veiculo.registrarAbastecimento(Abastecimento(hoje, "Diesel", 100.0, 500.0, 1000.0, motorista))
    with pytest.raises(ValueError): # verifica se o erro é o esperado (definido em dashboard.py  def calcularMediaConsumo)
        Dashboard().calcularMediaConsumo(veiculo)


def test_calcular_media_litros_zero(veiculo, motorista, hoje):
    # Situação improvável, mas verificar se permite divisão por zero (casos de quebra de ocultamento de informação)
    # ou seja, usuario conseguir mudar valores 
    veiculo.registrarAbastecimento(Abastecimento(hoje, "Diesel", 50.0, 300.0, 1000.0, motorista))
    veiculo.registrarAbastecimento(Abastecimento(hoje, "Diesel", 50.0, 300.0, 1500.0, motorista))
    # força litros do segundo abastecimento pra 0 (alteração forçada)
    veiculo._Veiculos__abastecimentos[1]._Abastecimento__litros = 0.0
    with pytest.raises(ZeroDivisionError):
        Dashboard().calcularMediaConsumo(veiculo)


def test_gerar_relatorio_captura_erros(veiculo):
    # Veículo sem dados, km atual vai ser 0 e abastecimento 0
    # verificando se o método gerarRelatorio trata esses erros de forma correta (e se armazena as mensagens de erro na lista detalhes)
    r = Dashboard().gerarRelatorio(veiculo)
    assert r.custoPorKm == 0.0
    assert r.mediaConsumo == 0.0
    assert len(r.detalhes) == 2  # uma mensagem por indicador com erro


def test_gerar_relatorio_dados_perfeitos(veiculo, motorista, oficina, hoje): # verifica se o relatorio gerado (em um caso ideal) está correto
    veiculo.registrarAbastecimento(Abastecimento(hoje, "Diesel", 200.0, 1000.0, 1000.0, motorista))
    veiculo.registrarAbastecimento(Abastecimento(hoje, "Diesel", 100.0, 500.0, 1500.0, motorista))
    veiculo.registrarManutencao(Manutencao(hoje, "corretiva", "Óleo", 800.0, 1500.0, oficina))
    r = Dashboard().gerarRelatorio(veiculo)
    assert isinstance(r, Relatorio)
    assert r.placa == "ABC-1234"
    assert r.totalGastoCombustivel == pytest.approx(1500.0)
    assert r.totalGastoManutencao == pytest.approx(800.0)
    assert r.detalhes == [] # deve estar vazio, já que não houve erros