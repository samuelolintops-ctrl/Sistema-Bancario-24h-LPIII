from __future__ import annotations
from abc import ABC
from typing import List, Optional, TYPE_CHECKING

from classes_banco.dados_cadastro import CPF, Endereco
from classes_banco.conta import Conta, ContaCorrente, ContaPoupanca
from classes_banco.historico import Operacao

if TYPE_CHECKING:
    from classes_banco.banco import Banco


class Usuario(ABC):
    '''
    Classe abstrata que representa um usuário genérico do sistema bancário.
    Mantém os dados cadastrais protegidos e a senha estritamente privada.
    '''
    def __init__(
        self,
        nome: str,
        cpf: CPF,
        email: str,
        data_nascimento: str,
        senha: str,
        endereco: Endereco
    ):
        self._nome: str = nome
        self._cpf: CPF = cpf
        self._email: str = email
        self._data_nascimento: str = data_nascimento
        self.__senha: str = senha
        self._endereco: Endereco = endereco

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def cpf(self) -> CPF:
        return self._cpf

    @property
    def email(self) -> str:
        return self._email

    @property
    def data_nascimento(self) -> str:
        return self._data_nascimento

    @property
    def endereco(self) -> Endereco:
        return self._endereco

    def autenticar(self, senha_informada: str) -> bool:
        '''
        Verifica se a senha informada corresponde à senha privada do usuário.
        '''
        return self.__senha == senha_informada


class Cliente(Usuario):
    '''
    Subclasse de Usuario que representa um cliente do banco.
    Gerencia a lista privada de contas associadas ao cliente e a execução de operações.
    '''
    def __init__(
        self,
        nome: str,
        cpf: CPF,
        email: str,
        data_nascimento: str,
        senha: str,
        endereco: Endereco
    ):
        super().__init__(nome, cpf, email, data_nascimento, senha, endereco)
        self.__contas: List[Conta] = []

    @property
    def contas(self) -> List[Conta]:
        return list(self.__contas)

    def add_conta(self, conta: Conta) -> None:
        '''
        Associa uma nova conta bancária à lista de contas do cliente.
        '''
        if isinstance(conta, Conta) and conta not in self.__contas:
            self.__contas.append(conta)

    def listar_contas(self) -> List[Conta]:
        '''
        Retorna uma cópia da lista de contas pertencentes ao cliente.
        '''
        return list(self.__contas)

    def realizar_operacao(self, conta: Conta, operacao: Operacao) -> bool:
        '''
        Executa uma operação financeira em uma conta pertencente ao cliente.
        '''
        if conta in self.__contas:
            return operacao.executar(conta)
        return False


class Gerente(Usuario):
    '''
    Subclasse de Usuario que representa um gerente (administrador) do banco.
    Possui permissões para cadastrar clientes, abrir/encerrar contas e emitir relatórios.
    '''
    def __init__(
        self,
        nome: str,
        cpf: CPF,
        email: str,
        data_nascimento: str,
        senha: str,
        endereco: Endereco,
        matricula: str
    ):
        super().__init__(nome, cpf, email, data_nascimento, senha, endereco)
        self.__matricula: str = matricula

    @property
    def matricula(self) -> str:
        return self.__matricula

    def cadastrar_cliente(self, banco: Banco, cliente: Cliente) -> bool:
        '''
        Registra um novo cliente no banco informado.
        '''
        return banco.add_cliente(cliente)

    def abrir_conta(
        self,
        banco: Banco,
        cliente: Cliente,
        id_conta: str,
        tipo: str = "corrente"
    ) -> Optional[Conta]:
        '''
        Cria uma nova conta (corrente ou poupança), vincula ao cliente e registra no banco.
        '''
        # Garante que o cliente está cadastrado no banco
        if banco.buscar_usuario(cliente.cpf.numero) is None:
            banco.add_cliente(cliente)

        tipo_normalizado = tipo.strip().lower()
        if tipo_normalizado == "corrente":
            nova_conta: Conta = ContaCorrente(id=id_conta, titular=cliente)
        elif tipo_normalizado in ("poupanca", "poupança"):
            nova_conta = ContaPoupanca(id=id_conta, titular=cliente)
        else:
            return None

        if banco.add_conta(nova_conta):
            cliente.add_conta(nova_conta)
            return nova_conta
        return None

    def encerrar_conta(self, banco: Banco, id_conta: str) -> bool:
        '''
        Encerra uma conta existente no banco, desde que o saldo esteja zerado.
        '''
        return banco.remover_conta(id_conta)

    def gerar_relatorio_bancario(self, banco: Banco) -> str:
        '''
        Gera um relatório geral com o resumo de clientes, gerentes e contas do banco.
        '''
        linhas = [
            f"=== RELATÓRIO BANCÁRIO: {banco.nome_do_banco} ===",
            f"Total de Clientes: {len(banco.clientes)}",
            f"Total de Gerentes: {len(banco.gerentes)}",
            f"Total de Contas Ativas: {len(banco.contas)}",
            "--- Detalhamento de Contas ---"
        ]
        for conta in banco.contas:
            linhas.append(str(conta))
        return "\n".join(linhas)
