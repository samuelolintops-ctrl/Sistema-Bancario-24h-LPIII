import os

def limpar_tela():
    '''
    Limpa a tela do terminal (multiplataforma: Windows, Linux e MacOs)
    '''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')