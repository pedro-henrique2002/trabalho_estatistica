import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D  # Necessário para criar as legendas customizadas do Boxplot
from scipy import stats


def correlacao_pearson(x: np.ndarray, y: np.ndarray) -> float:
    """
    Função 1: Calcula o coeficiente de correlação de Pearson 'r' entre duas variáveis.
    """
    if len(x) != len(y) or len(x) == 0:
        raise ValueError("Os vetores x e y devem ter o mesmo tamanho.")
    r = np.corrcoef(x, y)[0, 1]
    return float(r)


def regressao_linear(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """
    Função 2: Calcula os coeficientes da reta de regressão linear (y = a + bx) e R².
    Retorna: (a, b, r2)
    """
    if len(x) != len(y) or len(x) == 0:
        raise ValueError("Os vetores x e y devem ter o mesmo tamanho.")
    b, a = np.polyfit(x, y, 1)
    r = correlacao_pearson(x, y)
    r2 = r ** 2
    return float(a), float(b), float(r2)


def prever(x: np.ndarray | float, a: float, b: float) -> np.ndarray | float:
    """
    Função 3: Realiza a previsão de valores de y baseado na reta (y = a + bx).
    """
    return a + b * x


def gerar_grafico_densidade(
    dados: np.ndarray, 
    titulo: str, 
    x_label: str, 
    y_label: str, 
    nome_arquivo: str, 
    pasta_destino: str = "graficos"
) -> None:
    """
    Gera um gráfico de densidade contínua (KDE preenchido vs. Curva Normal Teórica),
    marcando visualmente as linhas de média e mediana na distribuição.
    """
    os.makedirs(pasta_destino, exist_ok=True)
    
    plt.figure(figsize=(8, 5))
    
    # Cálculos estatísticos da amostra lida
    media = float(np.mean(dados))
    mediana = float(np.median(dados))
    std_estimado = float(np.std(dados, ddof=1))
    
    # Ajuste de limites com folga confortável de 10% nas pontas
    xmin = np.min(dados) - (std_estimado * 0.5)
    xmax = np.max(dados) + (std_estimado * 0.5)
    x_linha = np.linspace(xmin, xmax, 200)
    
    # Estimativa de Densidade por Kernel (KDE) - Curva empírica suavizada com preenchimento
    try:
        kde = stats.gaussian_kde(dados)
        plt.plot(x_linha, kde(x_linha), color="#2b5c8f", linewidth=2, label="Densidade Empírica (KDE)")
        plt.fill_between(x_linha, kde(x_linha), alpha=0.25, color="#2b5c8f")
    except Exception:
        pass
        
    # Ajuste da curva normal teórica com parâmetros dos dados
    mu, std = stats.norm.fit(dados)
    p_linha = stats.norm.pdf(x_linha, mu, std)
    
    plt.plot(
        x_linha, 
        p_linha, 
        color="red", 
        linewidth=1.8, 
        linestyle="--",
        label=f"Ajuste Normal Teórico (mu={mu:.2f}, std={std:.2f})"
    )
    
    # Linhas verticais indicadoras de Média e Mediana
    plt.axvline(media, color="blue", linestyle=":", linewidth=1.5, label=f"Média Amostral: {media:.2f}")
    plt.axvline(mediana, color="red", linestyle="-", linewidth=1.5, label=f"Mediana Amostral: {mediana:.2f}")
    
    # Rug plot: Marcações dos pontos individuais observados na base do gráfico
    # Para amostras gigantescas (n > 5000), reduz o alpha do Rug Plot para não poluir o eixo
    alpha_rug = 0.1 if len(dados) > 5000 else 0.5
    plt.plot(dados, np.zeros_like(dados), '|', color="#2c3e50", alpha=alpha_rug, markersize=10, label="Pontos Observados")
    
    plt.title(titulo, fontsize=12, fontweight="bold", pad=15, color="#2c3e50")
    plt.xlabel(x_label, fontsize=10)
    plt.ylabel(y_label, fontsize=10)
    
    plt.grid(True, linestyle=":", alpha=0.6, color="#bdc3c7")
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#bdc3c7')
    ax.spines['bottom'].set_color('#bdc3c7')
    
    plt.legend(frameon=True, facecolor="white", edgecolor="none", fontsize=9)
    
    caminho_salvar = os.path.join(pasta_destino, nome_arquivo)
    plt.savefig(caminho_salvar, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()


def gerar_grafico_boxplot(
    dados: np.ndarray, 
    titulo: str, 
    x_label: str, 
    nome_arquivo: str, 
    pasta_destino: str = "graficos"
) -> None:
    """
    Gera um diagrama de caixa (boxplot) horizontal estilizado com legenda estatística rica.
    Otimizado para amostras pequenas e massivas (n > 100.000).
    """
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Altura ligeiramente maior para acomodar a legenda descritiva confortavelmente
    plt.figure(figsize=(8, 4.2))
    
    media = float(np.mean(dados))
    mediana = float(np.median(dados))
    std_estimado = float(np.std(dados, ddof=1))
    
    # Identificação matemática e quantificação de Outliers
    q1, q3 = np.percentile(dados, [25, 75])
    iqr = q3 - q1
    limite_inf = q1 - 1.5 * iqr
    limite_sup = q3 + 1.5 * iqr
    outliers = dados[(dados < limite_inf) | (dados > limite_sup)]
    total_outliers = len(outliers)
    pct_outliers = (total_outliers / len(dados)) * 100
    
    # Criação do boxplot horizontal exibindo também a linha da média amostral
    plt.boxplot(
        dados, 
        vert=False, 
        widths=0.15,
        patch_artist=True,
        showmeans=True,
        meanline=True,
        boxprops=dict(facecolor="#2b5c8f", color="#2c3e50", alpha=0.7),
        capprops=dict(color="#2c3e50", linewidth=1.2),
        whiskerprops=dict(color="#2c3e50", linewidth=1.2),
        # Flierprops otimizado para grandes volumes (ponto menor, sem borda e com alta transparência)
        flierprops=dict(
            marker="o", 
            markerfacecolor="red", 
            markeredgecolor="none", 
            markersize=3 if len(dados) > 5000 else 5, 
            alpha=0.15 if len(dados) > 5000 else 0.6,
            linestyle="none"
        ),
        meanprops=dict(color="blue", linewidth=1.5, linestyle=":"),
        medianprops=dict(color="red", linewidth=2)
    )
    
    plt.title(titulo, fontsize=12, fontweight="bold", pad=20, color="#2c3e50")
    plt.xlabel(x_label, fontsize=10)
    
    ax = plt.gca()
    ax.set_yticks([])
    ax.grid(True, linestyle=":", alpha=0.6, color="#bdc3c7")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#bdc3c7')
    
    # Criação da legenda descritiva rica que identifica os Outliers e exibe sua quantidade real
    elementos_legenda = [
        Line2D([0], [0], color="red", lw=2, label=f"Mediana: {mediana:.2f}"),
        Line2D([0], [0], color="blue", lw=1.5, linestyle=":", label=f"Média: {media:.2f}"),
        Line2D([0], [0], color="#2c3e50", lw=1.2, label=f"Desvio Padrão: {std_estimado:.2f}"),
        Line2D([0], [0], color="#2b5c8f", alpha=0.7, marker="s", markersize=8, linestyle="none", label="Int. Interquartil (IQR)"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="red", markeredgecolor="none", markersize=5, label=f"Outliers: {total_outliers} ({pct_outliers:.2f}%)")
    ]
    
    # Posiciona a legenda no topo direito de forma segura
    plt.legend(handles=elementos_legenda, frameon=True, facecolor="white", edgecolor="none", fontsize=9, loc="upper right")
    
    caminho_salvar = os.path.join(pasta_destino, nome_arquivo)
    plt.savefig(caminho_salvar, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()


def gerar_e_salvar_graficos(x: np.ndarray, y: np.ndarray, a: float, b: float, pasta_destino: str = "graficos") -> None:
    """
    Gera, salva e exibe 2 arquivos gráficos distintos para o Cenário C:
    1. 'dispersao_simples.png': Gráfico com os pontos observados.
    2. 'dispersao_regressao.png': Gráfico com os pontos e a reta de regressão.
    """
    os.makedirs(pasta_destino, exist_ok=True)
    
    # ----------------- GRÁFICO 1: Dispersão Simples -----------------
    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, color="blue", alpha=0.7, edgecolors="k", label="Dados Observados (Cache vs IPC)")
    
    plt.title("Gráfico de Dispersão: Cache L2 vs IPC", fontsize=12, pad=15)
    plt.xlabel("Tamanho da Cache L2 (MB)", fontsize=10)
    plt.ylabel("IPC (Instruções por Ciclo)", fontsize=10)
    
    # Grade suave
    plt.grid(True, linestyle=":", alpha=0.6, color="#bdc3c7")
    
    # Limpeza de bordas superior e direita
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.legend()
    
    caminho_simples = os.path.join(pasta_destino, "dispersao_simples.png")
    plt.savefig(caminho_simples, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()
    
    # ----------- GRÁFICO 2: Dispersão com Reta de Regressão -----------
    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, color="blue", alpha=0.7, edgecolors="k", label="Dados Observados")
    
    x_linha = np.linspace(np.min(x) - 0.5, np.max(x) + 0.5, 100)
    y_linha = prever(x_linha, a, b)
    
    plt.plot(
        x_linha, 
        y_linha, 
        color="red", 
        linewidth=2.5, 
        label=f"Reta de Regressão: y = {a:.4f} + {b:.4f}x"
    )
    
    plt.title("Ajuste de Regressão Linear: Cache L2 vs IPC", fontsize=12, pad=15)
    plt.xlabel("Tamanho da Cache L2 (MB)", fontsize=10)
    plt.ylabel("IPC (Instruções por Ciclo)", fontsize=10)
    
    # Grade suave
    plt.grid(True, linestyle=":", alpha=0.6, color="#bdc3c7")
    
    # Limpeza de bordas superior e direita
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.legend()
    
    caminho_regressao = os.path.join(pasta_destino, "dispersao_regressao.png")
    plt.savefig(caminho_regressao, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()