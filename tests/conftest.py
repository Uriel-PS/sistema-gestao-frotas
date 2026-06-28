import pytest
import datetime
from models.veiculos import Veiculos
from models.pessoa import Motorista, Gestor
from models.oficina import Oficina

# EQUIVALENTE AO setUp (@Before) do JUNIT. Instancia objetos pra CADA teste
# o Pytest reconhece o nome "conftest" automaticamente
# TOTAL DE TESTES: 32

@pytest.fixture
def veiculo():
    return Veiculos("ABC-1234", "Volvo", 20000.0, 0.0)

@pytest.fixture
def gestor():
    return Gestor("João", "111.111.111-11", "joao", "senha123", "joao@frota.com")

@pytest.fixture
def motorista():
    return Motorista("Maria", "222.222.222-22", "maria", "senha456", "CNH123")

@pytest.fixture
def oficina():
    return Oficina("Mecânica Central", "12.345.678/0001-99", "(47) 99999-0000", "Rua A, 1")

@pytest.fixture
def hoje():
    return datetime.date(2026, 6, 26)