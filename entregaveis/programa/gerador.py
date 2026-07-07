import os
import csv
import numpy as np


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

    def gerar_cenario_a(self, n: int = 40, media_alvo: float = 320.0, desvio_alvo: float = 45.0) -> np.ndarray:
        """
        Cenário A: Tempos de resposta de API REST. Parâmetros padrão da prova: n=40, média=320, desvio=45.
        Gera dados puramente estocásticos (amostragem real com variação e erro amostral).
        """
        return np.random.normal(loc=media_alvo, scale=desvio_alvo, size=n)

    def gerar_cenario_b(self, n: int = 25, media_alvo: float = 47.0, desvio_alvo: float = 8.0) -> np.ndarray:
        """
        Cenário B: Tempos de execução de compilador. Parâmetros padrão da prova: n=25, média=47, desvio=8.
        Gera dados puramente estocásticos (amostragem real com variação e erro amostral).
        """
        return np.random.normal(loc=media_alvo, scale=desvio_alvo, size=n)

    def gerar_cenario_c(self) -> np.ndarray:
        """
        Cenário C: 15 pares (X, Y) correspondentes a Cache L2 (MB) e IPC.
        Gera dados bivariados normais puros (com flutuação amostral real) a partir da covariância teórica.
        """
        medias = [5.0, 3.0]
        covariancia = [
            [3.5714, 2.5],
            [2.5, 2.1429]
        ]
        return np.random.multivariate_normal(mean=medias, cov=covariancia, size=15)

    def salvar_csv(self, caminho_arquivo: str, cabecalho: list[str], dados: np.ndarray) -> None:
        """
        Salva os dados de um array NumPy no arquivo CSV especificado.
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
        Gera e salva todos os cenários na pasta de destino utilizando as configurações originais da prova.
        """
        dados_a = self.gerar_cenario_a()
        dados_b = self.gerar_cenario_b()
        dados_c = self.gerar_cenario_c()
        
        self.salvar_csv(os.path.join(pasta_destino, "cenario_a.csv"), ["tempo_resposta"], dados_a)
        self.salvar_csv(os.path.join(pasta_destino, "cenario_b.csv"), ["tempo_execucao"], dados_b)
        self.salvar_csv(os.path.join(pasta_destino, "cenario_c.csv"), ["cache_l2", "ipc"], dados_c)

    def calcula_media(self, dados: list[float] | np.ndarray) -> float:
        """
        Calcula a média aritmética simples de um conjunto de dados utilizando NumPy.
        """
        if len(dados) == 0:
            return 0.0
        return float(np.mean(dados))