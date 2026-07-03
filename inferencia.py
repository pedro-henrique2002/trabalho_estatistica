import math
import numpy as np
from scipy import stats
import utils


def intervalo_confianca(dados: list[float] | np.ndarray, alpha: float = 0.05) -> tuple[float, float, float, float]:
    """
    Função 1: Constrói o intervalo de confiança bicaudal (1 - alpha) para a média 
    utilizando a distribuição t de Student (adequado para variância populacional desconhecida).
    
    Retorna: (limite_inf, limite_sup, media, desvio)
    """
    dados_arr = np.asarray(dados)
    n = len(dados_arr)
    if n <= 1:
        raise ValueError("A amostra deve conter mais de 1 elemento para calcular o desvio padrão.")
        
    media = float(np.mean(dados_arr))
    desvio = float(np.std(dados_arr, ddof=1))  # ddof=1 aplica o desvio amostral (n-1)
    df = n - 1
    
    # Calcula o IC bicaudal de Student de forma nativa pela distribuição do scipy
    limite_inf, limite_sup = stats.t.interval(
        confidence=1.0 - alpha, 
        df=df, 
        loc=media, 
        scale=desvio / np.sqrt(n)
    )
    
    return float(limite_inf), float(limite_sup), media, desvio


def teste_t_unilateral(dados: list[float] | np.ndarray, mu0: float, alpha: float = 0.05) -> tuple[float, float, bool, str]:
    """
    Função 2: Realiza o teste t de Student unilateral inferior (H0: mu >= mu0 vs H1: mu < mu0) 
    útil para validar se o tempo de execução foi reduzido.
    
    Retorna: (t_calc, t_critico, rejeita_h0, conclusao)
    """
    dados_arr = np.asarray(dados)
    n = len(dados_arr)
    if n <= 1:
        raise ValueError("A amostra deve conter mais de 1 elemento.")
        
    media = float(np.mean(dados_arr))
    desvio = float(np.std(dados_arr, ddof=1))
    df = n - 1
    
    # Estatística do teste t de Student
    t_calc = (media - mu0) / (desvio / np.sqrt(n))
    
    # Valor crítico para a cauda esquerda (unilateral inferior)
    t_critico = float(stats.t.ppf(alpha, df))
    
    # Decisão: Rejeita-se H0 se t_calculado estiver na região crítica (esquerda de t_critico)
    rejeita_h0 = bool(t_calc < t_critico)
    
    if rejeita_h0:
        conclusao = (
            f"Rejeita-se H0 ao nível de significância de {alpha*100:.0f}%. "
            f"Há evidências estatísticas significativas de que a média real ({media:.4f}) é menor que {mu0}."
        )
    else:
        conclusao = (
            f"Não se rejeita H0 ao nível de significância de {alpha*100:.0f}%. "
            f"Não há evidências estatísticas significativas para provar que a média real é menor que {mu0}."
        )
        
    return float(t_calc), t_critico, rejeita_h0, conclusao


def tamanho_amostra(desvio: float, amplitude: float, alpha: float = 0.05) -> int:
    """
    Função 3: Calcula o tamanho amostral mínimo necessário para estimar a média 
    com base em uma amplitude total máxima especificada para o intervalo de confiança.
    
    Retorna: n_mínimo
    """
    # A margem de erro permitida (E) é exatamente metade da amplitude total do IC
    margem_erro = amplitude / 2.0
    
    # Obtém o quantil bicaudal correspondente na distribuição normal (Z)
    z_critico = stats.norm.ppf(1.0 - alpha / 2.0)
    
    # Fórmula do tamanho amostral para estimação de médias
    n_estimado = ((z_critico * desvio) / margem_erro) ** 2
    
    # Arredondamento para cima obrigatório para manter a conservação estatística
    n_minimo = int(math.ceil(n_estimado))
    
    return n_minimo