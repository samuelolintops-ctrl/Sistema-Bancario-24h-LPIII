from usuario import Cliente

class Conta:
    def __init__(self, numero: str, cliente: Cliente, saldo: float = 0.0):
        self.numero = numero
        self.cliente = cliente
        self.saldo = saldo

    def depositar(self, valor):
        pass

    def sacar(self, valor):
        pass

    def __str__(self):
        return (f"Conta {self.numero} | Titular: {self.cliente.nome} "
                f"| Saldo: R$ {self.saldo:.2f}")