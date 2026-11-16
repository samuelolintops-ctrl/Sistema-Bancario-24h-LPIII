from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from classes_banco.conta import Conta


class Operacao(ABC):
    '''
    Classe abstrata que representa uma transação financeira no sistema bancário.
    Define a interface padrão para execução e detalhamento de operações nas contas.
    '''
    def __init__(self, valor: float):
        self._valor: float = valor
        self._data_hora: datetime = datetime.now()

    @property
    def valor(self) -> float:
        return self._valor

    @property
    def data_hora(self) -> datetime:
        return self._data_hora

    @abstractmethod
    def executar(self, conta: Conta) -> bool:
        '''
        Executa a operação financeira na conta informada e registra no histórico.
        '''
        pass

    @abstractmethod
    def detalhes(self) -> str:
        '''
        Retorna uma string formatada com os dados da operação para o extrato.
        '''
        pass


class Saque(Operacao):
    '''
    Representa uma operação de retirada de valores de uma conta bancária.
    '''
    def __init__(self, valor: float):
        super().__init__(valor)

    def executar(self, conta: Conta) -> bool:
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False

    def detalhes(self) -> str:
        data_fmt = self._data_hora.strftime("%d/%m/%Y %H:%M:%S")
        return f"[{data_fmt}] SAQUE: -R$ {self._valor:.2f}"


class Deposito(Operacao):
    '''
    Representa uma operação de entrada de valores em uma conta bancária.
    '''
    def __init__(self, valor: float):
        super().__init__(valor)

    def executar(self, conta: Conta) -> bool:
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False

    def detalhes(self) -> str:
        data_fmt = self._data_hora.strftime("%d/%m/%Y %H:%M:%S")
        return f"[{data_fmt}] DEPÓSITO: +R$ {self._valor:.2f}"


class Transferencia(Operacao):
    '''
    Representa uma transferência de valores entre uma conta de origem e uma de destino.
    Armazena a conta de destino de forma privada.
    '''
    def __init__(self, valor: float, conta_destino: Conta):
        super().__init__(valor)
        self.__conta_destino: Conta = conta_destino

    @property
    def conta_destino(self) -> Conta:
        return self.__conta_destino

    def executar(self, conta: Conta) -> bool:
        if conta == self.__conta_destino:
            return False

        if conta.sacar(self._valor):
            if self.__conta_destino.depositar(self._valor):
                conta.historico.adicionar_transacao(self)
                self.__conta_destino.historico.adicionar_transacao(self)
                return True
            else:
                # Estorna o valor para a conta de origem caso o depósito falhe
                conta.depositar(self._valor)
        return False

    def detalhes(self) -> str:
        data_fmt = self._data_hora.strftime("%d/%m/%Y %H:%M:%S")
        return (
            f"[{data_fmt}] TRANSFERÊNCIA: R$ {self._valor:.2f} "
            f"(Para Conta ID: {self.__conta_destino.id})"
        )


class Historico:
    '''
    Gerencia o registro cronológico de todas as operações realizadas em uma conta.
    Protege a lista interna de transações contra modificações externas diretas.
    '''
    def __init__(self):
        self.__transacoes: List[Operacao] = []

    @property
    def transacoes(self) -> List[Operacao]:
        # Retorna uma cópia da lista para evitar alterações externas (ex: .append() direto)
        return list(self.__transacoes)

    def adicionar_transacao(self, operacao: Operacao) -> bool:
        '''
        Adiciona uma nova operação validada à lista de transações da conta.
        '''
        if isinstance(operacao, Operacao):
            self.__transacoes.append(operacao)
            return True
        return False

    def gerar_relatorio(self) -> List[str]:
        '''
        Gera uma lista de strings contendo os detalhes de cada operação realizada.
        '''
        return [op.detalhes() for op in self.__transacoes]
