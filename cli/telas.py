import os
import re
from datetime import datetime
from typing import Optional

from classes_banco import (
    Banco,
    CPF,
    Endereco,
    Cliente,
    Gerente,
    Conta,
    ContaPoupanca,
    Saque,
    Deposito,
    Transferencia
)
from persistencia import PersistenciaBanco


class SistemaCLI:
    '''
    Gerencia a interface de linha de comando (CLI) do sistema bancário.
    Controla a exibição de menus, captura e validação rigorosa de entradas
    e fluxo de navegação entre clientes e gerentes.
    '''
    def __init__(self, banco: Banco, persistencia: PersistenciaBanco):
        self.__banco: Banco = banco
        self.__persistencia: PersistenciaBanco = persistencia

    def __limpar_tela(self) -> None:
        '''
        Limpa o terminal de acordo com o sistema operacional.
        '''
        os.system("cls" if os.name == "nt" else "clear")

    def __pausar(self) -> None:
        '''
        Aguarda o usuário pressionar ENTER antes de continuar.
        '''
        input("\nPressione ENTER para continuar...")

    # =========================================================================
    # MÉTODOS AUXILIARES DE VALIDAÇÃO DE ENTRADA
    # =========================================================================

    def __ler_texto_obrigatorio(self, mensagem: str, min_tam: int = 1) -> str:
        '''
        Solicita uma string em loop até que o usuário digite um valor não vazio
        e com o tamanho mínimo exigido.
        '''
        while True:
            valor = input(mensagem).strip()
            if len(valor) >= min_tam:
                return valor
            print(f"  [!] Entrada inválida. Preencha com pelo menos {min_tam} caractere(s).")

    def __ler_cpf_valido(self, verificar_duplicidade: bool = True) -> Optional[CPF]:
        '''
        Solicita o CPF em loop até que seja matematicamente válido (ou permite cancelar com 0).
        '''
        while True:
            entrada = input("CPF (11 dígitos ou '0' para cancelar): ").strip()
            if entrada == "0":
                return None

            cpf_obj = CPF(entrada)
            if not cpf_obj.validar():
                print("  [!] CPF inválido! Verifique os 11 dígitos e tente novamente.")
                continue

            if verificar_duplicidade and self.__banco.buscar_usuario(cpf_obj.numero) is not None:
                print("  [!] Já existe um usuário cadastrado com este CPF.")
                continue

            return cpf_obj

    def __ler_email_valido(self) -> str:
        '''
        Solicita um e-mail em loop até que atenda ao formato padrão usuario@dominio.com.
        '''
        padrao = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        while True:
            email = input("E-mail: ").strip()
            if re.match(padrao, email):
                return email
            print("  [!] Formato de e-mail inválido (exemplo: nome@dominio.com).")

    def __ler_data_valida(self) -> str:
        '''
        Solicita uma data de nascimento válida no formato DD/MM/AAAA e que não seja futura.
        '''
        while True:
            data_str = input("Data de nascimento (DD/MM/AAAA): ").strip()
            try:
                data_obj = datetime.strptime(data_str, "%d/%m/%Y")
                if data_obj > datetime.now():
                    print("  [!] A data de nascimento não pode ser no futuro.")
                    continue
                return data_str
            except ValueError:
                print("  [!] Data inválida! Use exatamente o formato DD/MM/AAAA.")

    def __ler_cep_valido(self) -> str:
        '''
        Solicita um CEP em loop até que contenha exatamente 8 dígitos numéricos.
        '''
        while True:
            cep = re.sub(r"\D", "", input("CEP (8 dígitos): ").strip())
            if len(cep) == 8:
                return cep
            print("  [!] CEP inválido! Digite os 8 números do CEP.")

    def __ler_uf_valida(self) -> str:
        '''
        Solicita a sigla do estado (UF) com 2 letras.
        '''
        while True:
            uf = input("Estado (UF - 2 letras): ").strip().upper()
            if len(uf) == 2 and uf.isalpha():
                return uf
            print("  [!] UF inválida! Digite a sigla com 2 letras (ex: BA, SP, RJ).")

    def __ler_valor_monetario(self, mensagem: str) -> float:
        '''
        Solicita um valor numérico positivo para transações financeiras.
        '''
        while True:
            entrada = input(mensagem).strip().replace(",", ".")
            try:
                valor = float(entrada)
                if valor > 0:
                    return valor
                print("  [!] O valor deve ser maior que zero.")
            except ValueError:
                print("  [!] Digite um número válido (ex: 150.50).")

    def __ler_dados_endereco(self) -> Endereco:
        '''
        Solicita e valida todos os campos do endereço residencial.
        '''
        print("\n--- Dados de Endereço ---")
        rua = self.__ler_texto_obrigatorio("Rua/Logradouro: ", min_tam=3)
        numero = self.__ler_texto_obrigatorio("Número (ou 'S/N'): ", min_tam=1)
        bairro = self.__ler_texto_obrigatorio("Bairro: ", min_tam=2)
        cidade = self.__ler_texto_obrigatorio("Cidade: ", min_tam=2)
        estado = self.__ler_uf_valida()
        cep = self.__ler_cep_valido()
        return Endereco(rua, numero, bairro, cidade, estado, cep)

    # =========================================================================
    # MENU INICIAL E LOGIN
    # =========================================================================

    def iniciar(self) -> None:
        '''
        Inicia o loop principal da interface de linha de comando.
        '''
        while True:
            self.__limpar_tela()
            print("==========================================")
            print(f"   BEM-VINDO AO {self.__banco.nome_do_banco.upper()}")
            print("==========================================")
            print("1. Login (Cliente / Gerente)")
            print("2. Cadastrar Primeiro Gerente")
            print("0. Sair do Sistema")
            print("------------------------------------------")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.__tela_login()
            elif opcao == "2":
                self.__tela_cadastro_gerente_inicial()
            elif opcao == "0":
                self.__persistencia.salvar(self.__banco)
                print("\nDados salvos. Encerrando o sistema...")
                break
            else:
                print("\n[!] Opção inválida.")
                self.__pausar()

    def __tela_login(self) -> None:
        '''
        Realiza a autenticação do usuário via CPF e senha, direcionando ao menu correspondente.
        '''
        self.__limpar_tela()
        print("=== AUTENTICAÇÃO DE USUÁRIO ===")
        cpf_str = self.__ler_texto_obrigatorio("CPF: ")
        senha = self.__ler_texto_obrigatorio("Senha: ")

        usuario = self.__banco.buscar_usuario(cpf_str)
        if usuario is None or not usuario.autenticar(senha):
            print("\n[!] CPF ou senha incorretos.")
            self.__pausar()
            return

        if isinstance(usuario, Gerente):
            self.__menu_gerente(usuario)
        elif isinstance(usuario, Cliente):
            self.__menu_cliente(usuario)

    def __tela_cadastro_gerente_inicial(self) -> None:
        '''
        Permite cadastrar um gerente validando todos os campos obrigatórios.
        '''
        self.__limpar_tela()
        print("=== CADASTRO DE GERENTE ===")
        cpf_obj = self.__ler_cpf_valido(verificar_duplicidade=True)
        if cpf_obj is None:
            return

        nome = self.__ler_texto_obrigatorio("Nome completo: ", min_tam=3)
        email = self.__ler_email_valido()
        data_nasc = self.__ler_data_valida()
        matricula = self.__ler_texto_obrigatorio("Matrícula funcional: ", min_tam=2)
        senha = self.__ler_texto_obrigatorio("Defina uma senha (mín. 3 caracteres): ", min_tam=3)
        endereco = self.__ler_dados_endereco()

        gerente = Gerente(nome, cpf_obj, email, data_nasc, senha, endereco, matricula)
        if self.__banco.add_gerente(gerente):
            self.__persistencia.salvar(self.__banco)
            print("\n[✓] Gerente cadastrado com sucesso!")
        else:
            print("\n[!] Não foi possível cadastrar o gerente.")
        self.__pausar()

    # =========================================================================
    # FLUXO DO GERENTE
    # =========================================================================

    def __menu_gerente(self, gerente: Gerente) -> None:
        '''
        Exibe o menu de operações administrativas exclusivas do Gerente.
        '''
        while True:
            self.__limpar_tela()
            print(f"=== PAINEL DO GERENTE: {gerente.nome} (Matrícula: {gerente.matricula}) ===")
            print("1. Cadastrar Novo Cliente")
            print("2. Abrir Conta para Cliente")
            print("3. Encerrar Conta")
            print("4. Gerar Relatório Bancário")
            print("0. Desconectar (Logout)")
            print("------------------------------------------")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.__acao_cadastrar_cliente(gerente)
            elif opcao == "2":
                self.__acao_abrir_conta(gerente)
            elif opcao == "3":
                self.__acao_encerrar_conta(gerente)
            elif opcao == "4":
                self.__limpar_tela()
                print(gerente.gerar_relatorio_bancario(self.__banco))
                self.__pausar()
            elif opcao == "0":
                break
            else:
                print("\n[!] Opção inválida.")
                self.__pausar()

    def __acao_cadastrar_cliente(self, gerente: Gerente) -> None:
        '''
        Coleta e valida os dados no terminal para o gerente cadastrar um novo cliente.
        '''
        self.__limpar_tela()
        print("=== CADASTRAR NOVO CLIENTE ===")
        cpf_obj = self.__ler_cpf_valido(verificar_duplicidade=True)
        if cpf_obj is None:
            return

        nome = self.__ler_texto_obrigatorio("Nome completo: ", min_tam=3)
        email = self.__ler_email_valido()
        data_nasc = self.__ler_data_valida()
        senha = self.__ler_texto_obrigatorio("Senha inicial (mín. 3 caracteres): ", min_tam=3)
        endereco = self.__ler_dados_endereco()

        novo_cliente = Cliente(nome, cpf_obj, email, data_nasc, senha, endereco)
        if gerente.cadastrar_cliente(self.__banco, novo_cliente):
            self.__persistencia.salvar(self.__banco)
            print(f"\n[✓] Cliente {nome} cadastrado com sucesso!")
        else:
            print("\n[!] Falha ao cadastrar cliente.")
        self.__pausar()

    def __acao_abrir_conta(self, gerente: Gerente) -> None:
        '''
        Coleta o CPF do cliente e valida o ID e o tipo de conta para abertura pelo gerente.
        '''
        self.__limpar_tela()
        print("=== ABRIR NOVA CONTA ===")
        cpf_str = self.__ler_texto_obrigatorio("Informe o CPF do cliente titular: ")
        usuario = self.__banco.buscar_usuario(cpf_str)

        if not isinstance(usuario, Cliente):
            print("\n[!] Cliente não encontrado com este CPF.")
            self.__pausar()
            return

        while True:
            id_conta = self.__ler_texto_obrigatorio("Número/ID da nova conta (ex: 1001-X): ", min_tam=2)
            if self.__banco.buscar_conta(id_conta) is None:
                break
            print("  [!] Já existe uma conta com este ID. Escolha outro.")

        while True:
            print("Tipo de Conta: [1] Corrente | [2] Poupança")
            tipo_op = input("Escolha o tipo (1 ou 2): ").strip()
            if tipo_op in ("1", "2"):
                tipo_str = "corrente" if tipo_op == "1" else "poupanca"
                break
            print("  [!] Opção inválida! Digite 1 para Corrente ou 2 para Poupança.")

        nova_conta = gerente.abrir_conta(self.__banco, usuario, id_conta, tipo_str)
        if nova_conta is not None:
            self.__persistencia.salvar(self.__banco)
            print(f"\n[✓] Conta {nova_conta.id} ({tipo_str.capitalize()}) aberta para {usuario.nome}!")
        else:
            print("\n[!] Erro ao abrir a conta.")
        self.__pausar()

    def __acao_encerrar_conta(self, gerente: Gerente) -> None:
        '''
        Solicita o ID da conta e realiza o encerramento caso o saldo seja zero.
        '''
        self.__limpar_tela()
        print("=== ENCERRAR CONTA BANCÁRIA ===")
        id_conta = self.__ler_texto_obrigatorio("Informe o ID da conta a ser encerrada: ")

        if gerente.encerrar_conta(self.__banco, id_conta):
            self.__persistencia.salvar(self.__banco)
            print(f"\n[✓] Conta {id_conta} encerrada com sucesso!")
        else:
            print("\n[!] Não foi possível encerrar. Verifique se a conta existe e se o saldo está zerado.")
        self.__pausar()

    # =========================================================================
    # FLUXO DO CLIENTE
    # =========================================================================

    def __menu_cliente(self, cliente: Cliente) -> None:
        '''
        Exibe o menu de seleção de contas e operações financeiras do Cliente.
        '''
        conta_ativa: Optional[Conta] = (
            cliente.contas[0] if len(cliente.contas) > 0 else None
        )

        while True:
            self.__limpar_tela()
            print(f"=== ÁREA DO CLIENTE: {cliente.nome} (CPF: {cliente.cpf}) ===")
            if conta_ativa is not None:
                print(f"Conta Selecionada: [{conta_ativa.id}] | Saldo: R$ {conta_ativa.saldo:.2f}")
            else:
                print("Conta Selecionada: Nenhuma conta vinculada.")
            print("------------------------------------------")
            print("1. Listar / Trocar Conta Ativa")
            print("2. Realizar Depósito")
            print("3. Realizar Saque")
            print("4. Realizar Transferência")
            print("5. Consultar Extrato")
            if isinstance(conta_ativa, ContaPoupanca):
                print("6. Simular Rendimento da Poupança")
            print("0. Desconectar (Logout)")
            print("------------------------------------------")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                conta_ativa = self.__acao_selecionar_conta(cliente, conta_ativa)
            elif opcao in ("2", "3", "4", "5", "6") and conta_ativa is None:
                print("\n[!] Você não possui uma conta selecionada. Solicite abertura ao gerente.")
                self.__pausar()
            elif opcao == "2" and conta_ativa is not None:
                self.__acao_depositar(cliente, conta_ativa)
            elif opcao == "3" and conta_ativa is not None:
                self.__acao_sacar(cliente, conta_ativa)
            elif opcao == "4" and conta_ativa is not None:
                self.__acao_transferir(cliente, conta_ativa)
            elif opcao == "5" and conta_ativa is not None:
                self.__acao_extrato(conta_ativa)
            elif opcao == "6" and isinstance(conta_ativa, ContaPoupanca):
                conta_ativa.aplicar_rendimento()
                self.__persistencia.salvar(self.__banco)
                print(f"\n[✓] Rendimento aplicado! Novo saldo: R$ {conta_ativa.saldo:.2f}")
                self.__pausar()
            elif opcao == "0":
                break
            else:
                print("\n[!] Opção inválida.")
                self.__pausar()

    def __acao_selecionar_conta(
        self,
        cliente: Cliente,
        conta_atual: Optional[Conta]
    ) -> Optional[Conta]:
        '''
        Lista as contas do cliente e permite alternar a conta ativa.
        '''
        self.__limpar_tela()
        print("=== MINHAS CONTAS ===")
        contas = cliente.listar_contas()
        if not contas:
            print("Você ainda não possui contas abertas.")
            self.__pausar()
            return None

        for idx, c in enumerate(contas, start=1):
            tipo = "Poupança" if isinstance(c, ContaPoupanca) else "Corrente"
            print(f"[{idx}] {tipo} - {c}")

        while True:
            escolha = input("\nDigite o número da conta para selecioná-la (ou ENTER para manter): ").strip()
            if escolha == "":
                return conta_atual
            if escolha.isdigit():
                indice = int(escolha) - 1
                if 0 <= indice < len(contas):
                    return contas[indice]
            print("  [!] Número inválido. Escolha uma das opções listadas.")

    def __acao_depositar(self, cliente: Cliente, conta: Conta) -> None:
        '''
        Executa uma operação de depósito na conta ativa do cliente.
        '''
        valor = self.__ler_valor_monetario("\nValor do depósito: R$ ")
        operacao = Deposito(valor)
        if cliente.realizar_operacao(conta, operacao):
            self.__persistencia.salvar(self.__banco)
            print(f"\n[✓] Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("\n[!] Operação recusada.")
        self.__pausar()

    def __acao_sacar(self, cliente: Cliente, conta: Conta) -> None:
        '''
        Executa uma operação de saque na conta ativa do cliente.
        '''
        valor = self.__ler_valor_monetario("\nValor do saque: R$ ")
        operacao = Saque(valor)
        if cliente.realizar_operacao(conta, operacao):
            self.__persistencia.salvar(self.__banco)
            print(f"\n[✓] Saque de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("\n[!] Saque recusado. Verifique saldo, limite ou quantidade de saques diários.")
        self.__pausar()

    def __acao_transferir(self, cliente: Cliente, conta_origem: Conta) -> None:
        '''
        Executa uma operação de transferência da conta ativa para outra conta do banco.
        '''
        id_destino = self.__ler_texto_obrigatorio("\nInforme o ID da conta de destino: ")
        if id_destino == conta_origem.id:
            print("\n[!] A conta de destino não pode ser a mesma conta de origem.")
            self.__pausar()
            return

        conta_destino = self.__banco.buscar_conta(id_destino)
        if conta_destino is None:
            print("\n[!] Conta de destino não encontrada.")
            self.__pausar()
            return

        valor = self.__ler_valor_monetario("Valor da transferência: R$ ")
        operacao = Transferencia(valor, conta_destino)
        if cliente.realizar_operacao(conta_origem, operacao):
            self.__persistencia.salvar(self.__banco)
            print(
                f"\n[✓] Transferência de R$ {valor:.2f} para {conta_destino.titular.nome} "
                f"(Conta {conta_destino.id}) realizada com sucesso!"
            )
        else:
            print("\n[!] Transferência não realizada. Verifique seu saldo disponível.")
        self.__pausar()

    def __acao_extrato(self, conta: Conta) -> None:
        '''
        Exibe no terminal o histórico detalhado de operações e o saldo atual da conta.
        '''
        self.__limpar_tela()
        print(f"=== EXTRATO BANCÁRIO - CONTA {conta.id} ===")
        print(f"Titular: {conta.titular.nome}")
        print("------------------------------------------")
        relatorio = conta.historico.gerar_relatorio()
        if not relatorio:
            print("Nenhuma movimentação registrada.")
        else:
            for linha in relatorio:
                print(linha)
        print("------------------------------------------")
        print(f"SALDO ATUAL: R$ {conta.saldo:.2f}")
        self.__pausar()
