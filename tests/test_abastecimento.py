import pytest
from models.abastecimento import Abastecimento

# 4 TESTES

def test_abastecimento_criacao_valida(motorista, hoje): # Verificação se os dados são armazenados corretamente na instanciação
    a = Abastecimento(hoje, "Diesel", 100.0, 500.0, 1000.0, motorista)
    assert a.litros == 100.0
    assert a.valorTotal == 500.0
    assert a.kmNoMomento == 1000.0


def test_abastecimento_litros_negativos_falha(motorista, hoje): 
    with pytest.raises(ValueError):
        Abastecimento(hoje, "Diesel", -10.0, 500.0, 1000.0, motorista) # verificando o erro de litros negativos (definido no construtor)


def test_abastecimento_valor_negativo_falha(motorista, hoje):
    with pytest.raises(ValueError):
        Abastecimento(hoje, "Diesel", 100.0, -500.0, 1000.0, motorista) # custo não deve ser negativo, verificando erro (definido no construtor)


def test_abastecimento_litros_zero_falha(motorista, hoje):
    with pytest.raises(ValueError):
        Abastecimento(hoje, "Diesel", 0.0, 500.0, 1000.0, motorista) # abastecimento não pode ser de 0 litros, verificando erro (getter)