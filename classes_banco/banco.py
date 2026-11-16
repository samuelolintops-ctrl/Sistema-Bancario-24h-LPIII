import re
from typing import List, Optional

from classes_banco.conta import Conta
from classes_banco.usuario import Usuario, Cliente, Gerente


class Banco:
    '''
    Representa a instituição bancária que centraliza o gerenciamento de clientes,
    gerentes e contas. Protege suas coleções internas com atributos privados.
    '''
    def __init__(self, nome_do_banco: str):
        self.__nome_do_banco: str = nome_do_banco
        self.__clientes: List[Cliente] = []
        self.__gerentes: List[Gerente] = []
        self.__contas: List[Conta] = []

    @property
    def nome_do_banco(self) -> str:
        return self.__nome_do_banco

    @property
    def clientes(self) -> List[Cliente]:
        return list(self.__clientes)

    @property
    def gerentes(self) -> List[Gerente]:
        return list(self.__gerentes)

    @property
    def contas(self) -> List[Conta]:
        return list(self.__contas)

    def add_cliente(self, cliente: Cliente) -> bool:
        '''
        Adiciona um novo cliente ao banco caso o CPF seja válido e ainda não esteja cadastrado.
        '''
        if not isinstance(cliente, Cliente) or not cliente.cpf.validar():
            return False

        if self.buscar_usuario(cliente.cpf.numero) is not None:
            return False

        self.__clientes.append(cliente)
        return True

    def add_gerente(self, gerente: Gerente) -> bool:
        '''
        Adiciona um novo gerente ao banco caso o CPF seja válido e ainda não esteja cadastrado.
        '''
        if not isinstance(gerente, Gerente) or not gerente.cpf.validar():
            return False

        if self.buscar_usuario(gerente.cpf.numero) is not None:
            return False

        self.__gerentes.append(gerente)
        return True

    def add_conta(self, conta: Conta) -> bool:
        '''
        Registra uma nova conta no banco caso o ID ainda não exista.
        '''
        if not isinstance(conta, Conta):
            return False

        if self.buscar_conta(conta.id) is not None:
            return False

        self.__contas.append(conta)
        return True

    def remover_conta(self, id_conta: str) -> bool:
        '''
        Remove uma conta do banco caso ela exista e seu saldo esteja zerado.
        '''
        conta = self.buscar_conta(id_conta)
        if conta is not None and conta.saldo == 0.0:
            self.__contas.remove(conta)
            return True
        return False

    def buscar_usuario(self, cpf: str) -> Optional[Usuario]:
        '''
        Busca e retorna um usuário (Cliente ou Gerente) pelo número do CPF.
        '''
        cpf_limpo = re.sub(r'\D', '', cpf)
        for cliente in self.__clientes:
            if cliente.cpf.numero == cpf_limpo:
                return cliente

        for gerente in self.__gerentes:
            if gerente.cpf.numero == cpf_limpo:
                return gerente

        return None

    def buscar_conta(self, id_conta: str) -> Optional[Conta]:
        '''
        Busca e retorna uma conta bancária pelo seu identificador (ID).
        '''
        for conta in self.__contas:
            if conta.id == id_conta:
                return conta
        return None
