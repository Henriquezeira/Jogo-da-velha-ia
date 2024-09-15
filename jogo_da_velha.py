import tkinter as tk
import numpy as np
import random
from config import ALPHA, GAMMA, EPSILON, q_table, atualizar_q_table, carregar_q_table, salvar_q_table

def inicializar_tabuleiro():
    return np.zeros((3, 3), dtype=int)

def tabuleiro_para_estado(tabuleiro):
    return tuple(map(tuple, tabuleiro))

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

def iniciar_interface():
    root = tk.Tk()
    root.title("Jogo da Velha")

    # Inicializar o tabuleiro e a interface
    global tabuleiro
    tabuleiro = inicializar_tabuleiro()
    
    botoes = [[None for _ in range(3)] for _ in range(3)]
    
    def jogar(linha, coluna):
        if tabuleiro[linha, coluna] == 0:
            fazer_jogada(tabuleiro, 1, linha, coluna)
            atualizar_interface()
            if verificar_vitoria(tabuleiro) == 1:
                status_var.set("Você venceu!")
                desativar_botoes()
                return
            if np.all(tabuleiro != 0):
                status_var.set("Empate!")
                desativar_botoes()
                return
            ia_linha, ia_coluna = escolher_acao(tabuleiro)
            fazer_jogada(tabuleiro, -1, ia_linha, ia_coluna)
            atualizar_interface()
            if verificar_vitoria(tabuleiro) == -1:
                status_var.set("A IA venceu!")
                desativar_botoes()
                return
            if np.all(tabuleiro != 0):
                status_var.set("Empate!")

    def atualizar_interface():
        for i in range(3):
            for j in range(3):
                botoes[i][j].config(text="X" if tabuleiro[i, j] == 1 else ("O" if tabuleiro[i, j] == -1 else ""), state="disabled" if tabuleiro[i, j] != 0 else "normal")

    def desativar_botoes():
        for i in range(3):
            for j in range(3):
                botoes[i][j].config(state="disabled")
    
    def reiniciar_jogo():
        global tabuleiro
        tabuleiro = inicializar_tabuleiro()
        atualizar_interface()
        status_var.set("Seu vez!")
        for i in range(3):
            for j in range(3):
                botoes[i][j].config(state="normal")

    status_var = tk.StringVar()
    status_var.set("Seu vez!")
    status_label = tk.Label(root, textvariable=status_var)
    status_label.grid(row=3, column=0, columnspan=3)

    for i in range(3):
        for j in range(3):
            botoes[i][j] = tk.Button(root, text="", width=10, height=3, command=lambda i=i, j=j: jogar(i, j))
            botoes[i][j].grid(row=i, column=j)

    reiniciar_button = tk.Button(root, text="Reiniciar", command=reiniciar_jogo)
    reiniciar_button.grid(row=4, column=0, columnspan=3)

    root.mainloop()

if __name__ == "__main__":
    carregar_q_table()
    iniciar_interface()
