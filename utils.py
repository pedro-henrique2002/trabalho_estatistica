import csv
import os
import numpy as np


def calcula_media(dados: list[float] | np.ndarray) -> float:
    """
    Calcula a média aritmética simples de um conjunto de dados utilizando NumPy.
    """
    if len(dados) == 0:
        return 0.0
    return float(np.mean(dados))


def ler_coluna_csv(caminho_arquivo: str, coluna_nome: str) -> np.ndarray:
    """
    Lê uma coluna específica de um arquivo CSV pelo nome do cabeçalho
    e retorna os valores correspondentes em um array NumPy.
    """
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"O arquivo {caminho_arquivo} não foi encontrado.")
        
    valores = []
    with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            valores.append(float(linha[coluna_nome]))
            
    return np.array(valores)


def ler_par_csv(caminho_arquivo: str, coluna_x: str, coluna_y: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Lê duas colunas específicas de um arquivo CSV e retorna um par de arrays NumPy (X, Y).
    Útil para as análises bivariadas e regressões.
    """
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"O arquivo {caminho_arquivo} não foi encontrado.")
        
    valores_x = []
    valores_y = []
    with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            valores_x.append(float(linha[coluna_x]))
            valores_y.append(float(linha[coluna_y]))
            
    return np.array(valores_x), np.array(valores_y)