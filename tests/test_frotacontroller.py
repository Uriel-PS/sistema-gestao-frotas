import pytest
from controllers.frotaController import FrotaController
from models.pessoa import PermissaoNegadaError

# 2 TESTES NA CLASSE CONTROLLER

def test_controller_login_atribui_usuario():
    controller = FrotaController()
    controller.cadastrarGestor("Admin", "000", "admin", "admin123", "admin@frota.com")
    usuario = controller.login("admin", "admin123")
    assert usuario is not None #verifica se o usuario foi cadastrado corretamente
    assert controller.usuario_logado.perfil() == "Gestor" # verifica se o perfil do usuario é correto de acordo com o login (Gestor)


def test_controller_protecao_exigir_gestor(): #verificação de permissão
    controller = FrotaController()
    controller.cadastrarGestor("Admin", "000", "admin", "admin123", "admin@frota.com")
    controller.login("admin", "admin123")
    controller.cadastrarMotorista("Maria", "111", "maria", "senha456", "CNH999")
    controller.logout() # desloguei do gestor
    controller.login("maria", "senha456") # login de motorista
    with pytest.raises(PermissaoNegadaError):
        controller.cadastrarVeiculo("XYZ-0000", "Volvo", 1000.0, 0.0) # Motorista não pode cadastrar veículo, verificar se o erro é lançado