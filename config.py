import numpy as np
import pickle

# Definindo parâmetros do Q-Learning
ALPHA = 0.1  # Taxa de aprendizado
GAMMA = 0.9  # Fator de desconto
EPSILON = 0.1  # Probabilidade de escolher uma ação aleatória (exploração)

q_table = {}

def tabuleiro_para_estado(tabuleiro):
    return tuple(map(tuple, tabuleiro))

def atualizar_q_table(tabuleiro, acao, recompensa, novo_tabuleiro):
    estado = tabuleiro_para_estado(tabuleiro)
    novo_estado = tabuleiro_para_estado(novo_tabuleiro)
    
    if estado not in q_table:
        q_table[estado] = {}
    if novo_estado not in q_table:
        q_table[novo_estado] = {}
    
    q_atual = q_table[estado].get(acao, 0)
    max_q_novo_estado = max(q_table[novo_estado].values(), default=0)
    q_table[estado][acao] = q_atual + ALPHA * (recompensa + GAMMA * max_q_novo_estado - q_atual)

def carregar_q_table():
    global q_table
    try:
        with open('q_table.pkl', 'rb') as f:
            q_table = pickle.load(f)
    except FileNotFoundError:
        q_table = {}

def salvar_q_table():
    with open('q_table.pkl', 'wb') as f:
        pickle.dump(q_table, f)
