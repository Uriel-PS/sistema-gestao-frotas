import pytest
from models.manutencao import Manutencao

# 4 TESTES NA CLASSE MANUTENCAO

def test_manutencao_criacao_valida(oficina, hoje): #verificando se a criação da classe funciona corretamente
    m = Manutencao(hoje, "preventiva", "Troca de óleo", 300.0, 5000.0, oficina)
    assert m.tipo == "preventiva"
    assert m.custoTotal == 300.0


def test_manutencao_tipo_case_insensitive(oficina, hoje): # no caso aceitamos (.lower), verificando se a conversão é feita
    m = Manutencao(hoje, "CORRETIVA", "Freios", 500.0, 5000.0, oficina)
    assert m.tipo == "corretiva"


def test_manutencao_tipo_inventado_falha(oficina, hoje):
    with pytest.raises(ValueError): #verificando se aceita os tipos existentes de manutencao (corretiva, preventiva) e joga o erro correto
        Manutencao(hoje, "estetica", "Pintura", 200.0, 5000.0, oficina)


def test_manutencao_km_negativo_falha(oficina, hoje):
    with pytest.raises(ValueError): # verificando se o erro jogado é o correto para quando kmAtual negativo
        Manutencao(hoje, "preventiva", "Óleo", 300.0, -100.0, oficina)