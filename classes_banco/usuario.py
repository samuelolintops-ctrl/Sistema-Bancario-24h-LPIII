from banco import Banco
from conta import Conta

class Usuario:
    '''
    <<Documentação da classe>>
    '''
    def __init__(self):
        pass


class Cliente(Usuario):
    '''
    <<Documentação da classe>>
    '''
    def __init__(self):
        super().__init__()
        pass


class Administrador(Usuario):
    '''
    <<Documentação da classe>>
    '''
    def __init__(self):
        super().__init__()
        pass

    def cadastrar_cliente(self, bank: Banco) -> Cliente:
        pass

    def abrir_conta(self, bank: Banco, client: Cliente) -> Conta:
        pass

    def encerrar_conta(self, bank: Banco) -> bool:
        pass

    def gerar_relatorio(self, bank: Banco) -> str:
        pass