import pytest
from models.oficina import Oficina

# 2 TESTES NA CLASSE OFICINA

def test_oficina_factory_method(): #verificação da instaciação (factory), se é da classe esperada
    o = Oficina.cadastrarOficina("Mecânica Silva", "98.765.432/0001-11", "(47) 8888-1111", "Av. B, 200")
    assert isinstance(o, Oficina)
    assert o.nome == "Mecânica Silva"


def test_oficina_id_incremental(): # verificando se o id é incrementado corretamente
    o1 = Oficina("Oficina A", "111", "111", "End A")
    o2 = Oficina("Oficina B", "222", "222", "End B")
    assert o2.id == o1.id + 1