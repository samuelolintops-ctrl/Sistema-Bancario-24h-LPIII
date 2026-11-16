import re


class CPF:
    '''
    Representa e valida o Cadastro de Pessoa Física (CPF) de um usuário.
    Armazena o número de forma privada e fornece métodos para validação dos
    dígitos verificadores e formatação visual.
    '''
    def __init__(self, numero: str):
        # Remove caracteres não numéricos antes de armazenar
        self.__numero = re.sub(r'\D', '', numero)

    @property
    def numero(self) -> str:
        return self.__numero

    def validar(self) -> bool:
        '''
        Valida se o CPF possui 11 dígitos e se os dígitos verificadores são válidos.
        '''
        if len(self.__numero) != 11 or self.__numero == self.__numero[0] * 11:
            return False

        for i in range(9, 11):
            soma = sum(int(self.__numero[num]) * ((i + 1) - num) for num in range(0, i))
            digito = ((soma * 10) % 11) % 10
            if digito != int(self.__numero[i]):
                return False
        return True

    def formatar(self) -> str:
        '''
        Retorna o CPF no formato padrão 012.345.678-90.
        '''
        if len(self.__numero) == 11:
            return f"{self.__numero[:3]}.{self.__numero[3:6]}.{self.__numero[6:9]}-{self.__numero[9:]}"
        return self.__numero

    def __str__(self) -> str:
        return self.formatar()


class Endereco:
    '''
    Representa o endereço residencial de um usuário do sistema bancário.
    Seus atributos são privados e expostos apenas para leitura via propriedades.
    '''
    def __init__(
        self,
        rua: str,
        numero: str,
        bairro: str,
        cidade: str,
        estado: str,
        cep: str
    ):
        self.__rua: str = rua
        self.__numero: str = numero
        self.__bairro: str = bairro
        self.__cidade: str = cidade
        self.__estado: str = estado
        self.__cep: str = re.sub(r'\D', '', cep)

    @property
    def rua(self) -> str:
        return self.__rua

    @property
    def numero(self) -> str:
        return self.__numero

    @property
    def bairro(self) -> str:
        return self.__bairro

    @property
    def cidade(self) -> str:
        return self.__cidade

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def cep(self) -> str:
        return self.__cep

    def __str__(self) -> str:
        cep_fmt = f"{self.__cep[:5]}-{self.__cep[5:]}" if len(self.__cep) == 8 else self.__cep
        return f"{self.__rua}, {self.__numero} - {self.__bairro}, {self.__cidade}/{self.__estado} - CEP: {cep_fmt}"
