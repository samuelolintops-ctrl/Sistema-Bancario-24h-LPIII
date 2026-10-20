import pickle
import os

ARQUIVO_DADOS = "banco_dados.pkl"

def salvar_dados(dados, nome_arquivo: str = ARQUIVO_DADOS):
    with open(nome_arquivo, "wb") as arquivo:
        pickle.dump(dados, arquivo)
    print(f"Dados salvos em '{nome_arquivo}'.")

def carregar_dados(nome_arquivo: str = ARQUIVO_DADOS):
    if not os.path.exists(nome_arquivo):
        return []
    
    with open(nome_arquivo, "rb") as arquivo:
        return pickle.load(arquivo)