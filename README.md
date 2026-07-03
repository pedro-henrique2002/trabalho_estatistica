# Análise Estatística de Desempenho de Sistemas com Python

Trabalho de Estatística aplicado à análise e simulação de desempenho de sistemas.

*   **Versão do Python recomendada:** configurado especificamente para Python 3.14.2 (Só garanto o funcionamento nessa versão).

---

## 📂 Estrutura do Projeto

*   **`main.py`**: Ponto de entrada do sistema contendo a interface interativa em terminal.
*   **`gerador.py`**: Módulo responsável pela simulação dos dados dos cenários com base em parâmetros da prova (utilizando NumPy).
*   **`utils.py`**: Funções auxiliares compartilhadas, como cálculo de média e leitura estruturada de arquivos CSV.
*   **`inferencia.py`**: Funções para construção de Intervalo de Confiança ($t$ de Student), cálculo de tamanho amostral mínimo e Teste T Unilateral.
*   **`regressao.py`**: Funções para cálculo do Coeficiente de Correlação de Pearson ($r$), ajuste de Regressão Linear Simples, predição de valores e geração de gráficos com Matplotlib.
*   **`dados/`**: Pasta gerada automaticamente onde são salvos os datasets (`cenario_a.csv`, `cenario_b.csv` e `cenario_c.csv`).
*   **`graficos/`**: Pasta gerada automaticamente que armazena os gráficos exportados em formato PNG (`dispersao_simples.png` e `dispersao_regressao.png`).

---

## 🚀 Como Executar o Projeto

Você pode executar este projeto de duas formas: utilizando o gerenciador de dependências **Poetry** (recomendado para os alunos) ou o instalador tradicional **pip** (Recomendado para a professora por ser mais facil).

### Método 1: Utilizando o pip (Tradicional)
Se preferir o método convencional utilizando ambientes virtuais do Python (venv) e o arquivo `requirements.txt`:

1.  Crie e ative o ambiente virtual (opcional, mas recomendado):
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  Instale as dependências necessárias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Execute o script principal:
    ```bash
    python main.py
    ```

---

### Método 2: Utilizando o Poetry (Recomendado)
Se você possui o Poetry instalado, execute os seguintes comandos no diretório raiz do projeto:

1.  Instale as dependências definidas no `pyproject.toml`:
    ```bash
    poetry install
    ```
2.  Inicie a aplicação:
    ```bash
    poetry run python main.py
    ```

---

## 📊 Instruções de Uso no Terminal

Ao iniciar o programa `main.py`, a interface do terminal solicitará as seguintes etapas:

1.  **Configuração da Semente (Seed):**
    *   Digite um número inteiro para fixar uma semente de geração (garantindo a reprodutibilidade exata dos testes).
    *   Ou apenas pressione **ENTER** para que o sistema utilize uma semente aleatória gerada pelo sistema operacional.
2.  **Menu Interativo:**
    *   **Opção 1 (Cenário A - API REST):** Calcula e exibe o Intervalo de Confiança, avalia a conformidade com o SLA limite de 350 ms e calcula o tamanho amostral mínimo para uma amplitude de 20 ms.
    *   **Opção 2 (Cenário B - Compilador):** Executa o Teste t Unilateral esquerdo para verificar a redução do tempo médio em relação a 50 segundos, exibindo o valor crítico, o t calculado e a decisão estatística com conclusão textual.
    *   **Opção 3 (Cenário C - Cache vs IPC):** Calcula a correlação de Pearson, o coeficiente de determinação ($R^2$), a reta de regressão ajustada, projeta o IPC para uma cache de 8 MB e gera/salva os gráficos de dispersão na pasta `graficos/`.
    *   **Opção 0 (Sair):** Encerra a execução do loop e fecha o programa.
