import numpy as np
def inicializar_tabuleiro():
    #cria tabuleiro 3x3
    return np.zeros((3, 3), dtype=int)

def exibir_tabuleiro(tabuleiro):
    #exibe o tabuleiro
    for linha in tabuleiro:
        print(' '.join(str(celula) for celula in linha))
    print()

def verificar_vitoria(tabuleiro):
    #verica vitoria
    for i in range(3):
        #verifica linha e colunas 
        if np.all(tabuleiro[i, :] == 1) or np.all(tabuleiro[:, i] == 1):
            return 1
        if np.all(tabuleiro[i, :] == -1) or np.all(tabuleiro[:, i] == -1):
            return -1 
    if np.all(np.diag(tabuleiro) == 1) or np.all(np.diag(np.flipr(tabuleiro)) == 1):
        return 1
    if np.all(np.diag(tabuleiro) == -1) or np.all(np.diag(np.flipr(tabuleiro)) == -1):
        return -1
    
    return 0

#testando a inicialização
tabuleiro =  inicializar_tabuleiro()
exibir_tabuleiro(tabuleiro)