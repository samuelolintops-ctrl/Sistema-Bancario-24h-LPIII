from usuario import Cliente

class Conta:
    def __init__(self, numero: str, cliente: Cliente, saldo: float = 0.0):
        self.numero = numero
        self.cliente = cliente
        self.saldo = saldo

    def depositar(self, valor: float):
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        self.saldo += valor

    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= valor

    def transferir(self, destino: Cliente, valor: float):
        self.sacar(valor)
        destino.depositar(valor)

    def __str__(self):
        return (f"Conta {self.numero} | Titular: {self.cliente.nome} "
                f"| Saldo: R$ {self.saldo:.2f}")
