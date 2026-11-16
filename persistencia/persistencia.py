import pickle
from pathlib import Path
from typing import Optional

from classes_banco import Banco


class PersistenciaBanco:
    '''
    Gerencia a persistência de dados do sistema bancário utilizando o módulo pickle.
    Salva e carrega a instância completa do Banco no diretório 'data'.
    '''
    def __init__(
        self,
        diretorio: str = "data",
        nome_arquivo: str = "banco.pkl"
    ):
        self.__diretorio: Path = Path(diretorio)
        self.__caminho_arquivo: Path = self.__diretorio / nome_arquivo
        self.__garantir_diretorio()

    @property
    def caminho_arquivo(self) -> Path:
        return self.__caminho_arquivo

    def __garantir_diretorio(self) -> None:
        '''
        Cria o diretório de dados caso ele ainda não exista no sistema de arquivos.
        '''
        self.__diretorio.mkdir(parents=True, exist_ok=True)

    def salvar(self, banco: Banco) -> bool:
        '''
        Serializa e salva o objeto Banco (com seus clientes, gerentes, contas e históricos)
        no arquivo binário configurado.
        '''
        if not isinstance(banco, Banco):
            return False

        try:
            self.__garantir_diretorio()
            with open(self.__caminho_arquivo, "wb") as arquivo:
                pickle.dump(banco, arquivo, protocol=pickle.HIGHEST_PROTOCOL)
            return True
        except (OSError, pickle.PickleError):
            return False

    def carregar(self, nome_banco_padrao: str = "Banco Python") -> Banco:
        '''
        Carrega e retorna a instância do Banco salva no arquivo binário.
        Caso o arquivo não exista ou esteja corrompido, retorna uma nova instância vazia.
        '''
        if not self.__caminho_arquivo.exists():
            return Banco(nome_banco_padrao)

        try:
            with open(self.__caminho_arquivo, "rb") as arquivo:
                objeto = pickle.load(arquivo)
                if isinstance(objeto, Banco):
                    return objeto
        except (OSError, EOFError, pickle.PickleError):
            pass

        return Banco(nome_banco_padrao)

    def limpar_dados(self) -> bool:
        '''
        Remove o arquivo de persistência do diretório 'data', caso exista.
        '''
        try:
            if self.__caminho_arquivo.exists():
                self.__caminho_arquivo.unlink()
                return True
        except OSError:
            pass
        return False
