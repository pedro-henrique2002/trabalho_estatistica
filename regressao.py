import os
import numpy as np
import matplotlib.pyplot as plt


def correlacao_pearson(x: np.ndarray, y: np.ndarray) -> float:
    """
    Função 1: Calcula o coeficiente de correlação de Pearson 'r' entre duas variáveis.
    """
    if len(x) != len(y) or len(x) == 0:
        raise ValueError("Os vetores x e y devem ter o mesmo tamanho e não estarem vazios.")
        
    # np.corrcoef retorna a matriz de correlação. O elemento [0, 1] é a correlação cruzada entre x e y.
    r = np.corrcoef(x, y)[0, 1]
    return float(r)


def regressao_linear(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """
    Função 2: Calcula os coeficientes da reta de regressão linear ajustada (y = a + bx) 
    e o coeficiente de determinação (R²).
    
    Retorna: (a, b, r2)
    Onde:
        'a' é o intercepto (coeficiente linear).
        'b' é a inclinação (coeficiente angular / slope).
        'r2' é o coeficiente de determinação (R²).
    """
    if len(x) != len(y) or len(x) == 0:
        raise ValueError("Os vetores x e y devem ter o mesmo tamanho.")
        
    # np.polyfit de grau 1 ajusta uma reta (y = bx + a)
    # Retorna os coeficientes em ordem decrescente de potência: [inclinação (b), intercepto (a)]
    b, a = np.polyfit(x, y, 1)
    
    r = correlacao_pearson(x, y)
    r2 = r ** 2
    
    return float(a), float(b), float(r2)


def prever(x: np.ndarray | float, a: float, b: float) -> np.ndarray | float:
    """
    Função 3: Realiza a previsão de valores de y baseado nos coeficientes da reta de regressão (y = a + bx).
    """
    return a + b * x


def gerar_e_salvar_graficos(x: np.ndarray, y: np.ndarray, a: float, b: float, pasta_destino: str = "graficos") -> None:
    """
    Função 4: Gera e salva 2 arquivos gráficos distintos em formato PNG:
    1. 'dispersao_simples.png': Gráfico contendo apenas os pontos observados.
    2. 'dispersao_regressao.png': Gráfico com os pontos e a reta de regressão sobreposta.
    """
    # Garante a existência do diretório de destino
    os.makedirs(pasta_destino, exist_ok=True)
    
    # ----------------- GRÁFICO 1: Dispersão Simples -----------------
    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, color="blue", alpha=0.7, edgecolors="k", label="Dados Observados (Cache vs IPC)")
    
    plt.title("Gráfico de Dispersão: Cache L2 vs IPC", fontsize=12, pad=15)
    plt.xlabel("Tamanho da Cache L2 (MB)", fontsize=10)
    plt.ylabel("IPC (Instruções por Ciclo)", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    
    caminho_simples = os.path.join(pasta_destino, "dispersao_simples.png")
    plt.savefig(caminho_simples, dpi=300, bbox_inches="tight")
    plt.close()
    
    # ----------- GRÁFICO 2: Dispersão com Reta de Regressão -----------
    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, color="blue", alpha=0.7, edgecolors="k", label="Dados Observados")
    
    # Geração dos limites para desenhar a linha contínua da reta
    x_linha = np.linspace(np.min(x) - 0.5, np.max(x) + 0.5, 100)
    y_linha = prever(x_linha, a, b)
    
    # Desenha a linha vermelha da regressão
    plt.plot(
        x_linha, 
        y_linha, 
        color="red", 
        linewidth=2, 
        label=f"Reta de Regressão: y = {a:.4f} + {b:.4f}x"
    )
    
    plt.title("Ajuste de Regressão Linear: Cache L2 vs IPC", fontsize=12, pad=15)
    plt.xlabel("Tamanho da Cache L2 (MB)", fontsize=10)
    plt.ylabel("IPC (Instruções por Ciclo)", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    
    caminho_regressao = os.path.join(pasta_destino, "dispersao_regressao.png")
    plt.savefig(caminho_regressao, dpi=300, bbox_inches="tight")
    plt.close()