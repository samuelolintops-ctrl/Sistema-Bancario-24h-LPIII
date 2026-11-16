'''
Ponto de entrada principal da aplicação do sistema bancário.
Inicializa a persistência, carrega o banco de dados e executa a interface CLI.
'''

from classes_banco import (
    Banco,
    CPF,
    Endereco,
    Cliente,
    Gerente,
    Deposito,
    Saque
)
from persistencia import PersistenciaBanco
from cli import SistemaCLI


def popular_dados_iniciais(banco: Banco, persistencia: PersistenciaBanco) -> None:
    '''
    Popula o banco com dados iniciais de teste (1 gerente, 2 clientes e 3 contas)
    caso o banco recém-carregado não possua nenhum gerente ou cliente cadastrado.
    '''
    if len(banco.gerentes) > 0 or len(banco.clientes) > 0:
        return

    # 1. Criação de Gerente padrão (CPF matematicamente válido)
    end_gerente = Endereco("Av. Paulista", "1000", "Bela Vista", "São Paulo", "SP", "01310-100")
    gerente = Gerente(
        nome="Carlos Silva (Gerente)",
        cpf=CPF("52998224725"),
        email="carlos@bancopython.com",
        data_nascimento="10/05/1980",
        senha="admin",
        endereco=end_gerente,
        matricula="GER-001"
    )
    banco.add_gerente(gerente)

    # 2. Criação do Cliente 1 (com Conta Corrente e Conta Poupança)
    end_cli1 = Endereco("Rua das Flores", "123", "Centro", "Itabuna", "BA", "45600-000")
    cliente1 = Cliente(
        nome="Ana Souza",
        cpf=CPF("11144477735"),
        email="ana@email.com",
        data_nascimento="22/08/1995",
        senha="123",
        endereco=end_cli1
    )
    gerente.cadastrar_cliente(banco, cliente1)

    conta_c1 = gerente.abrir_conta(banco, cliente1, id_conta="1001-C", tipo="corrente")
    conta_p1 = gerente.abrir_conta(banco, cliente1, id_conta="1001-P", tipo="poupanca")

    if conta_c1 is not None:
        cliente1.realizar_operacao(conta_c1, Deposito(1500.00))
        cliente1.realizar_operacao(conta_c1, Saque(200.00))
    if conta_p1 is not None:
        cliente1.realizar_operacao(conta_p1, Deposito(500.00))

    # 3. Criação do Cliente 2 (para testar Transferências entre contas)
    end_cli2 = Endereco("Rua Sete de Setembro", "45", "Barra", "Salvador", "BA", "40000-000")
    cliente2 = Cliente(
        nome="Bruno Oliveira",
        cpf=CPF("12345678909"),
        email="bruno@email.com",
        data_nascimento="15/03/1992",
        senha="123",
        endereco=end_cli2
    )
    gerente.cadastrar_cliente(banco, cliente2)
    conta_c2 = gerente.abrir_conta(banco, cliente2, id_conta="2002-C", tipo="corrente")

    if conta_c2 is not None:
        cliente2.realizar_operacao(conta_c2, Deposito(800.00))

    # Salva o estado inicial no arquivo data/banco.pkl
    persistencia.salvar(banco)


def main() -> None:
    '''
    Função principal que orquestra o carregamento dos dados e início do sistema.
    '''
    persistencia = PersistenciaBanco(diretorio="data", nome_arquivo="banco.pkl")
    banco = persistencia.carregar(nome_banco_padrao="Banco Grêmio (fuck Inter)")

    # Cria dados de teste se for a primeira execução
    popular_dados_iniciais(banco, persistencia)

    sistema_cli = SistemaCLI(banco=banco, persistencia=persistencia)
    try:
        sistema_cli.iniciar()
    except KeyboardInterrupt:
        persistencia.salvar(banco)
        print("\n\n[!] Interrupção detectada. Dados salvos com segurança.")


if __name__ == "__main__":
    main()
