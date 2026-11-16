from __future__ import annotations
from abc import ABC
from typing import List, TYPE_CHECKING

from classes_banco.historico import Historico, Operacao, Saque

if TYPE_CHECKING:
    from classes_banco.usuario import Cliente


class Conta(ABC):
    '''
    Classe abstrata que representa uma conta bancária genérica.
    Encapsula os dados fundamentais da conta (agência, id, titular, saldo e histórico)
    como protegidos, permitindo leitura controlada via propriedades.
    '''
    def __init__(
        self,
        id: str,
        titular: Cliente,
        saldo: float = 0.0,
        agencia: str = "0001"
    ):
        self._agencia: str = agencia
        self._id: str = id
        self._titular: Cliente = titular
        self._saldo: float = saldo
        self._historico: Historico = Historico()

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def id(self) -> str:
        return self._id

    @property
    def titular(self) -> Cliente:
        return self._titular

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def historico(self) -> Historico:
        return self._historico

    def depositar(self, valor: float) -> bool:
        '''
        Adiciona um valor positivo ao saldo da conta.
        '''
        if valor > 0:
            self._saldo += valor
            return True
        return False

    def sacar(self, valor: float) -> bool:
        '''
        Retira um valor do saldo da conta, caso haja saldo suficiente.
        '''
        if 0 < valor <= self._saldo:
            self._saldo -= valor
            return True
        return False

    def transferir(self, valor: float, destino: Conta) -> bool:
        '''
        Transfere um valor desta conta para uma conta de destino.
        '''
        if destino == self or valor <= 0:
            return False

        if self.sacar(valor):
            if destino.depositar(valor):
                return True
            # Estorna caso o depósito no destino falhe
            self.depositar(valor)
        return False

    def obter_extrato(self) -> List[Operacao]:
        '''
        Retorna a lista de operações registradas no histórico da conta.
        '''
        return self._historico.transacoes

    def __str__(self) -> str:
        return (
            f"Agência: {self._agencia} | Conta: {self._id} | "
            f"Titular: {self._titular.nome} | Saldo: R$ {self._saldo:.2f}"
        )


class ContaCorrente(Conta):
    '''
    Subclasse de Conta que representa uma Conta Corrente.
    Possui regras específicas de limite de cheque especial e limite de saques.
    '''
    def __init__(
        self,
        id: str,
        titular: Cliente,
        saldo: float = 0.0,
        agencia: str = "0001",
        limite_cheque_especial: float = 500.0,
        limite_saques_diarios: int = 3
    ):
        super().__init__(id, titular, saldo, agencia)
        self.__limite_cheque_especial: float = limite_cheque_especial
        self.__limite_saques_diarios: int = limite_saques_diarios

    @property
    def limite_cheque_especial(self) -> float:
        return self.__limite_cheque_especial

    @property
    def limite_saques_diarios(self) -> int:
        return self.__limite_saques_diarios

    def sacar(self, valor: float) -> bool:
        '''
        Sobrescreve o método sacar para considerar o limite de saques realizados
        e o saldo somado ao limite do cheque especial.
        '''
        saques_realizados = len(
            [op for op in self._historico.transacoes if isinstance(op, Saque)]
        )
        if saques_realizados >= self.__limite_saques_diarios:
            return False

        saldo_disponivel = self._saldo + self.__limite_cheque_especial
        if 0 < valor <= saldo_disponivel:
            self._saldo -= valor
            return True
        return False


class ContaPoupanca(Conta):
    '''
    Subclasse de Conta que representa uma Conta Poupança.
    Possui uma taxa de rendimento aplicável sobre o saldo positivo.
    '''
    def __init__(
        self,
        id: str,
        titular: Cliente,
        saldo: float = 0.0,
        agencia: str = "0001",
        taxa_rendimento: float = 0.005
    ):
        super().__init__(id, titular, saldo, agencia)
        self.__taxa_rendimento: float = taxa_rendimento

    @property
    def taxa_rendimento(self) -> float:
        return self.__taxa_rendimento

    def aplicar_rendimento(self) -> None:
        '''
        Aplica a taxa de rendimento ao saldo atual, caso seja positivo.
        '''
        if self._saldo > 0:
            self._saldo += self._saldo * self.__taxa_rendimento
