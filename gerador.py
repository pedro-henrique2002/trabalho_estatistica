import os
import csv
import numpy as np


def calcula_media(dados: list[float] | np.ndarray) -> float:
    """
    Calcula a média aritmética simples de um conjunto de dados utilizando NumPy.
    """
    if len(dados) == 0:
        return 0.0
    return float(np.mean(dados))


class GeradorDeDados:
    """
    Classe para simular e salvar os dados estatísticos dos cenários utilizando
    as funções de geração de distribuição nativas do NumPy ao máximo.
    """
    
    seed: int | None

    def __init__(self, seed: int | None = None) -> None:
        """
        Inicializa o gerador configurando a semente global do NumPy.
        """
        self.seed = seed
        if self.seed is not None:
            np.random.seed(self.seed)

    def gerar_cenario_a(self) -> np.ndarray:
        """
        Cenário A: 40 tempos de resposta de API REST.
        Gera uma amostra de tamanho 40 a partir de uma distribuição Normal 
        com média de 320 ms e desvio padrão de 45 ms.
        """
        return np.random.normal(loc=320.0, scale=45.0, size=40)

    def gerar_cenario_b(self) -> np.ndarray:
        """
        Cenário B: 25 tempos de execução de compilador.
        Gera uma amostra de tamanho 25 a partir de uma distribuição Normal 
        com média de 47 s e desvio padrão de 8 s.
        """
        return np.random.normal(loc=47.0, scale=8.0, size=25)

    def gerar_cenario_c(self) -> np.ndarray:
        """
        Cenário C: 15 pares (X, Y) correspondentes a Cache L2 (MB) e IPC.
        Gera dados normais bivariados baseados na matriz de covariância teórica calculada 
        a partir da prova (Variância de X = 3.5714, Variância de Y = 2.1429, Covariância = 2.5).
        """
        # Médias das duas variáveis (X: Cache L2, Y: IPC)
        medias = [5.0, 3.0]
        
        # Matriz de covariância teórica construída a partir dos somatórios:
        # SS_xx = 50 -> variância_x = 50 / 14 = 3.5714
        # SS_yy = 30 -> variância_y = 30 / 14 = 2.1429
        # SS_xy = 35 -> covariância_xy = 35 / 14 = 2.5
        covariancia = [
            [3.5714, 2.5],
            [2.5, 2.1429]
        ]
        
        # Geração direta usando distribuição normal bivariada
        return np.random.multivariate_normal(mean=medias, cov=covariancia, size=15)

    def salvar_csv(self, caminho_arquivo: str, cabecalho: list[str], dados: np.ndarray) -> None:
        """
        Salva os dados de um array NumPy no arquivo CSV especificado.
        Cria as pastas necessárias no caminho caso elas não existam.
        """
        diretorio = os.path.dirname(caminho_arquivo)
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)
            
        with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(cabecalho)
            
            for linha in dados:
                if isinstance(linha, np.ndarray) or hasattr(linha, '__iter__'):
                    escritor.writerow([round(float(val), 4) for val in linha])
                else:
                    escritor.writerow([round(float(linha), 4)])

    def gerar_e_salvar_todos(self, pasta_destino: str = "dados") -> None:
        """
        Gera e salva todos os cenários na pasta de destino utilizando as funções do NumPy.
        """
        dados_a = self.gerar_cenario_a()
        dados_b = self.gerar_cenario_b()
        dados_c = self.gerar_cenario_c()
        
        self.salvar_csv(os.path.join(pasta_destino, "cenario_a.csv"), ["tempo_resposta"], dados_a)
        self.salvar_csv(os.path.join(pasta_destino, "cenario_b.csv"), ["tempo_execucao"], dados_b)
        self.salvar_csv(os.path.join(pasta_destino, "cenario_c.csv"), ["cache_l2", "ipc"], dados_c)