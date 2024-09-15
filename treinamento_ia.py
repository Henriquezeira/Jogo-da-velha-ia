import numpy as np
import random
from config import ALPHA, GAMMA, EPSILON, q_table, atualizar_q_table, carregar_q_table, salvar_q_table, tabuleiro_para_estado

def inicializar_tabuleiro():
    return np.zeros((3, 3), dtype=int)

def escolher_acao(tabuleiro):
    estado = tabuleiro_para_estado(tabuleiro)
    if np.random.uniform(0, 1) < EPSILON:
        jogadas_possiveis = [(i, j) for i in range(3) for j in range(3) if tabuleiro[i, j] == 0]
        return random.choice(jogadas_possiveis)
    else:
        if estado not in q_table:
            q_table[estado] = {}
        max_q = -float('inf')
        melhor_acao = None
        for i in range(3):
            for j in range(3):
                if tabuleiro[i, j] == 0:
                    q_value = q_table[estado].get((i, j), 0)
                    if q_value > max_q:
                        max_q = q_value
                        melhor_acao = (i, j)
        return melhor_acao

def fazer_jogada(tabuleiro, jogador, linha, coluna):
    if tabuleiro[linha, coluna] == 0:
        tabuleiro[linha, coluna] = jogador
        return True
    return False

def verificar_vitoria(tabuleiro):
    for i in range(3):
        if np.all(tabuleiro[i, :] == 1) or np.all(tabuleiro[:, i] == 1):
            return 1
        if np.all(tabuleiro[i, :] == -1) or np.all(tabuleiro[:, i] == -1):
            return -1
    if np.all(np.diag(tabuleiro) == 1) or np.all(np.diag(np.fliplr(tabuleiro)) == 1):
        return 1
    if np.all(np.diag(tabuleiro) == -1) or np.all(np.diag(np.fliplr(tabuleiro)) == -1):
        return -1
    return 0

def treinar_ia(num_partidas):
    for _ in range(num_partidas):
        tabuleiro = inicializar_tabuleiro()
        jogo_ativo = True
        while jogo_ativo:
            estado_atual = tabuleiro_para_estado(tabuleiro)
            acao = escolher_acao(tabuleiro)
            fazer_jogada(tabuleiro, -1, acao[0], acao[1])
            resultado = verificar_vitoria(tabuleiro)
            if resultado != 0 or np.all(tabuleiro != 0):
                recompensa = resultado
                novo_tabuleiro = tabuleiro
                atualizar_q_table(estado_atual, acao, recompensa, novo_tabuleiro)
                jogo_ativo = False
            else:
                jogador_acao = escolher_acao(tabuleiro)
                fazer_jogada(tabuleiro, 1, jogador_acao[0], jogador_acao[1])
                resultado = verificar_vitoria(tabuleiro)
                if resultado != 0 or np.all(tabuleiro != 0):
                    recompensa = resultado
                    novo_tabuleiro = tabuleiro
                    atualizar_q_table(estado_atual, acao, recompensa, novo_tabuleiro)
                    jogo_ativo = False

# Carrega a tabela Q antes de começar o treinamento
carregar_q_table()

# Treina a IA jogando contra ela mesma por um número de partidas
treinar_ia(num_partidas=10000)  # Ajuste o número de partidas conforme necessário

# Salva a tabela Q após o treinamento
salvar_q_table()
