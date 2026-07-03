import os
import utils
import inferencia
import regressao
from gerador import GeradorDeDados


def obter_semente() -> int | None:
    """
    Solicita uma semente ao usuário. Se o input for vazio, retorna None (aleatória).
    """
    print("\n" + "="*55)
    print(" CONFIGURAÇÃO DE INICIALIZAÇÃO")
    print("="*55)
    entrada = input("Digite uma semente (ou pressione ENTER para semente aleatória): ").strip()
    
    if entrada == "":
        print("-> Inicializando com semente de sistema (aleatória).")
        return None
    try:
        semente = int(entrada)
        print(f"-> Inicializando com a semente definida: {semente}")
        return semente
    except ValueError:
        print("-> Entrada inválida! Utilizando semente aleatória por padrão.")
        return None


def exibir_cenario_a() -> None:
    """
    Processa e exibe as análises estatísticas do Cenário A (API REST).
    """
    caminho_csv = os.path.join("dados", "cenario_a.csv")
    print("\n" + "-"*55)
    print(" PROCESSANDO: CENÁRIO A - API REST")
    print("-"*55)
    
    try:
        dados = utils.ler_coluna_csv(caminho_csv, "tempo_resposta")
        
        # 1. Intervalo de Confiança
        lim_inf, lim_sup, media, desvio = inferencia.intervalo_confianca(dados, alpha=0.05)
        
        # 2. Tamanho mínimo da amostra para amplitude máxima de 20 ms
        n_min = inferencia.tamanho_amostra(desvio, amplitude=20.0, alpha=0.05)
        
        print(f"Número de observações (n): {len(dados)}")
        print(f"Média Amostral:           {media:.4f} ms")
        print(f"Desvio Padrão Amostral:   {desvio:.4f} ms")
        print(f"Intervalo de Confiança:   [{lim_inf:.4f} ms, {lim_sup:.4f} ms]")
        print(f"Tamanho Mínimo Amostra (IC Amplitude 20ms): {n_min} amostras")
        
        # Validação do SLA (SLA deve ser inferior a 350 ms)
        print("\nAnálise de SLA (Limite: 350 ms):")
        if lim_sup < 350.0:
            print(f"-> Em conformidade. O limite superior do IC ({lim_sup:.2f} ms) é inferior a 350 ms.")
        else:
            print(f"-> Alerta. O limite superior do IC ({lim_sup:.2f} ms) ultrapassa ou atinge os 350 ms.")
            
    except Exception as e:
        print(f"Erro no processamento do Cenário A: {e}")


def exibir_cenario_b() -> None:
    """
    Processa e exibe as análises estatísticas do Cenário B (Compilador).
    """
    caminho_csv = os.path.join("dados", "cenario_b.csv")
    print("\n" + "-"*55)
    print(" PROCESSANDO: CENÁRIO B - COMPILADOR")
    print("-"*55)
    
    try:
        dados = utils.ler_coluna_csv(caminho_csv, "tempo_execucao")
        
        # Teste T Unilateral (mu0 = 50 segundos)
        t_calc, t_crit, rejeita, conclusao = inferencia.teste_t_unilateral(dados, mu0=50.0, alpha=0.05)
        
        print(f"Número de observações (n): {len(dados)}")
        print(f"Média Amostral:           {utils.calcula_media(dados):.4f} s")
        print(f"Estatística t calculada:  {t_calc:.4f}")
        print(f"Valor crítico de t:       {t_crit:.4f}")
        print(f"Decisão (Rejeita H0?):    {rejeita}")
        print(f"\nConclusão:\n{conclusao}")
        
    except Exception as e:
        print(f"Erro no processamento do Cenário B: {e}")


def exibir_cenario_c() -> None:
    """
    Processa e exibe as análises estatísticas do Cenário C (Cache vs IPC).
    """
    caminho_csv = os.path.join("dados", "cenario_c.csv")
    print("\n" + "-"*55)
    print(" PROCESSANDO: CENÁRIO C - CACHE L2 VS IPC")
    print("-"*55)
    
    try:
        x, y = utils.ler_par_csv(caminho_csv, "cache_l2", "ipc")
        
        # 1. Correlação de Pearson
        r = regressao.correlacao_pearson(x, y)
        
        # 2. Regressão Linear
        a, b, r2 = regressao.regressao_linear(x, y)
        
        # 3. Geração e salvamento automático dos gráficos em PNG
        regressao.gerar_e_salvar_graficos(x, y, a, b, "graficos")
        
        # 4. Previsão para Cache de 8 MB
        previsao_8mb = regressao.prever(8.0, a, b)
        
        print(f"Número de Pares (n):             {len(x)}")
        print(f"Correlação de Pearson (r):       {r:.4f}")
        print(f"Coeficiente de Determinação (R²): {r2:.4f}")
        print(f"Equação Ajustada da Reta:        y = {a:.4f} + ({b:.4f}) * x")
        print(f"IPC previsto para Cache de 8MB:  {previsao_8mb:.4f}")
        print("\n-> Gráficos gerados com sucesso na pasta 'graficos/'")
        
    except Exception as e:
        print(f"Erro no processamento do Cenário C: {e}")


def main() -> None:
    """
    Função de controle principal da interface no terminal.
    """
    semente = obter_semente()
    
    # Gera e salva os arquivos CSV na pasta 'dados/' logo no início
    print("\nGerando base de dados nos arquivos CSV...")
    gerador = GeradorDeDados(seed=semente)
    gerador.gerar_e_salvar_todos(pasta_destino="dados")
    print("-> Arquivos de dados preparados com sucesso.")
    
    while True:
        print("\n" + "="*55)
        print(" PROJETO: ESTATÍSTICA DE DESEMPENHO DE SISTEMAS")
        print("="*55)
        print("1. Cenário A - API REST")
        print("2. Cenário B - Compilador")
        print("3. Cenário C - Cache vs IPC")
        print("0. Sair do Programa")
        print("="*55)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "0":
            print("\nFinalizando o programa de análise de sistemas. Até logo!")
            break
        elif opcao == "1":
            exibir_cenario_a()
        elif opcao == "2":
            exibir_cenario_b()
        elif opcao == "3":
            exibir_cenario_c()
        else:
            print("\n[Erro] Opção inválida! Selecione um número correspondente do menu.")
            
        input("\nPressione ENTER para voltar ao menu principal...")


if __name__ == "__main__":
    main()