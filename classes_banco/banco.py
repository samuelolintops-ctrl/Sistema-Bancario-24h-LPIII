from classes_banco.usuario import Cliente
from classes_banco.conta import Conta


class Banco:
    '''
    Os clientes e as contas ficam em um dicionario com a chave de acesso de cliente sendo o cpf e a de conta o numero da propria conta 
    '''
    def __init__(self):
        self.clientes: dict[str, Cliente] = {}
        self.contas: dict[str, Conta] = {}
        
    def adicionar_cliente(self, cliente: Cliente) -> None:
    
        ''' validação para saber se nao escreveram nenhum cpf, nome ou se o cpf já esta cadastrado'''
        if not cliente.cpf:
            raise ValueError("o CPF precisa ser digitado")
        if not cliente.nome:
            raise ValueError("O nome precisa ser digitado")
        if cliente.cpf in self.clientes: 
            raise ValueError("Ja existe esse cpf cadastrado")
    
        self.clientes[cliente.cpf] = cliente
        
    def remover_cliente(self, cpf: str) -> Cliente:
        
        cliente = self.clientes.get(cpf)
        if cliente is None:
            raise ValueError("Cliente nao foi encontrado")
        if any(conta.saldo > 0 for conta in cliente.contas):
            raise ValueError("o clente possui saldo na conta")
        
        for conta in cliente.contas:
            self.contas.pop(conta.numero, None)
        
        del self.clientes[cpf]
        return cliente
    
    def abrir_conta(self, cpf: str, numero:str, saldo_inicial: float = 0.0) -> Conta:
        cliente = self.clientes.get(cpf)
        
        if cliente is None:
            raise ValueError("Cliente não foi encontrado")
        if numero in self.contas:
            raise ValueError("Uma conta com esse numero ja existe")
        
        conta = Conta(numero, cliente, saldo_inicial)
        self.contas[numero] = conta
        cliente.adicionar_conta(conta)
        return conta
    
    def listar_clientes(self) -> list[Cliente]:
        return list(self.clientes.values())