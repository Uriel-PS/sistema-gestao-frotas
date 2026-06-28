import pytest
from models.pessoa import Gestor, Motorista, PermissaoNegadaError
from models.dashboard import Dashboard

# 5 TESTES NA CLASSE PESSOA

def test_pessoa_autenticacao_sucesso(motorista): # verifica se o retorno pra o login do motorista é true (a senha definida em conftest é senha456)
    assert motorista.autenticar("senha456") is True


def test_pessoa_autenticacao_falha_senha_errada(motorista): # caso contrário do anterior
    assert motorista.autenticar("senhaerrada") is False


def test_pessoa_inativa_bloqueia_login(motorista): # verifica se o login é bloqueado (False) ao inativar a conta
    motorista.inativar()
    assert motorista.autenticar("senha456") is False


def test_polimorfismo_perfis(gestor, motorista): # verificando se a divisão por perfis está correta em cada classe (getters)
    assert gestor.perfil() == "Gestor"
    assert motorista.perfil() == "Motorista"


def test_gestor_recebe_alerta(gestor, veiculo):
    gestor.atualizar(veiculo) #atualiza forçadamente para verificar se alertas são recebidos pelo Observer (gestor)
    assert len(gestor.alertas_recebidos) == 1
    assert "ABC-1234" in gestor.alertas_recebidos[0]