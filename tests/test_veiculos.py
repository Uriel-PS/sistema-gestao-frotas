import pytest
from models.veiculos import Veiculos
from models.abastecimento import Abastecimento
from models.manutencao import Manutencao
from patterns.estados import EstadoDisponivel, EstadoEmManutencao, TransicaoInvalidaError

#obs, considerar as instanciações de conftest
# 8 TESTES NA CLASSE VEICULOS

def test_veiculo_nasce_disponivel(veiculo): 
    assert isinstance(veiculo.estadoAtual, EstadoDisponivel)


def test_veiculo_transicao_para_manutencao(veiculo):
    veiculo.iniciarManutencao()
    assert isinstance(veiculo.estadoAtual, EstadoEmManutencao)


def test_veiculo_transicao_invalida_gera_erro(veiculo):
    veiculo.iniciarManutencao()
    with pytest.raises(TransicaoInvalidaError): # verifica se o erro dado é do tipo "TransicaoInvalidaError"
        veiculo.inicializarOperacao()

# recibo inicial (conftest, o veículo tinha 0KM atual) e no momento do abastecimento, marcava 5000km.
# Verificação se atualizou o hodometro do veículo
def test_veiculo_atualiza_hodometro(veiculo, motorista, hoje):
    veiculo.registrarAbastecimento(Abastecimento(hoje, "Diesel", 100.0, 500.0, 5000.0, motorista))
    assert veiculo.kmAtual == 5000.0


# Inicialmente, kmAtual = 0. Por padrão deverá ser notificado manutenção após 10000km rodados 
# verifica se o alerta foi recebido e se o veiculo que notificou é o correto
def test_veiculo_dispara_alerta_observer(veiculo, gestor, motorista, hoje):
    veiculo.registrar(gestor)
    veiculo.registrarAbastecimento(Abastecimento(hoje, "Diesel", 400.0, 2000.0, 10500.0, motorista))
    assert len(gestor.alertas_recebidos) == 1
    assert "ABC-1234" in gestor.alertas_recebidos[0]

# verifica o contrário do teste anterior, se não notifica o gestor quando não passou do limite de revisão (10mil km)
def test_veiculo_silencio_observer(veiculo, gestor, motorista, hoje):
    veiculo.registrar(gestor)
    veiculo.registrarAbastecimento(Abastecimento(hoje, "Diesel", 100.0, 500.0, 5000.0, motorista))
    assert len(gestor.alertas_recebidos) == 0

# verifica se a tag ficou falsa após inativar
def test_veiculo_inativacao_logica(veiculo):
    veiculo.inativar()
    assert veiculo.ativo is False

# verifica se ao registrar uma manutencao para um veiculo, ela consta na lista de manutencoes
def test_veiculo_guardar_manutencao(veiculo, oficina, hoje):
    m = Manutencao(hoje, "corretiva", "Freios", 500.0, 5000.0, oficina)
    veiculo.registrarManutencao(m)
    assert m in veiculo.manutencoes