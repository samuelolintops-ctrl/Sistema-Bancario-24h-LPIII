from classes_banco.usuario import Conta, Cliente
import persistencia.persistencia as persistencia

def main():
    '''print("=== ETAPA 1: CRIANDO OBJETOS E SALVANDO ===")
    
    # 1. Instanciando clientes
    c1 = Cliente("Ana Silva", "111.222.333-44")
    c2 = Cliente("Carlos Souza", "555.666.777-88")
    
    # 2. Criando contas associadas aos clientes
    conta1 = Conta(numero=1001, titular=c1, saldo_inicial=500.0)
    conta2 = Conta(numero=1002, titular=c2, saldo_inicial=1200.0)
    
    # Operações de teste
    conta1.depositar(250.0)  # Saldo deve ir para 750.0
    conta2.sacar(200.0)      # Saldo deve ir para 1000.0
    
    contas_cadastradas = [conta1, conta2]
    
    # Salvando no arquivo com Pickle
    persistencia.salvar_dados(contas_cadastradas)
    
    print("\n=== ETAPA 2: LIMPANDO MEMÓRIA E RECARREGANDO DO ARQUIVO ===")
    del contas_cadastradas
    
    # Recuperando as contas gravadas
    contas_recuperadas = persistencia.carregar_dados()
    
    print(f"Quantidade de contas carregadas: {len(contas_recuperadas)}\n")
    for conta in contas_recuperadas:
        print(conta)
        print(f" -> Detalhes do titular: {conta.titular}")'''
    pass

if __name__ == "__main__":
    main()

"""from datetime import datetime
agora = datetime.now()
data_hora = agora.strftime("%d/%m/%Y %H:%M")"""
