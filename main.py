import os
import inferencia
import regressao
from gerador import GeradorDeDados


def obter_semente() -> int | None:
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


# ---------------- SUBMENU CENÁRIO A ----------------
def gerenciar_cenario_a(gerador: GeradorDeDados) -> None:
    caminho_csv = os.path.join("dados", "cenario_a.csv")
    
    # Parâmetros atuais do gerador (guardados em memória)
    n_atual, media_atual, desvio_atual = 40, 320.0, 45.0
    
    while True:
        print("\n" + "="*55)
        print(" SUBMENU: CENÁRIO A - API REST")
        print("="*55)
        # Exibe os parâmetros dinâmicos de distribuição no topo do menu
        print(f"Parâmetros Ativos: n = {n_atual} | Média = {media_atual:.1f} ms | Desvio = {desvio_atual:.1f} ms")
        print("-"*55)
        print("1. Executar Análise Estatística (IC, SLA e Amostra Mínima)")
        print("2. Visualizar Gráficos de Distribuição (Leitura do CSV)")
        print("3. Alterar Parâmetros de Geração de Dados")
        print("0. Voltar ao Menu Anterior")
        print("="*55)
        
        op = input("Escolha uma opção: ").strip()
        
        if op == "0":
            break
            
        elif op == "1":
            print("\n--- Estatísticas (Lendo do CSV) ---")
            try:
                dados = inferencia.ler_coluna_csv(caminho_csv, "tempo_resposta")
                lim_inf, lim_sup, media, desvio = inferencia.intervalo_confianca(dados, alpha=0.05)
                n_min = inferencia.tamanho_amostra(desvio, amplitude=20.0, alpha=0.05)
                
                print(f"Amostra Lida (n):         {len(dados)}")
                print(f"Média Amostral Lida:      {media:.4f} ms")
                print(f"Desvio Padrão Lodo:       {desvio:.4f} ms")
                print(f"Intervalo de Confiança:   [{lim_inf:.4f} ms, {lim_sup:.4f} ms]")
                print(f"Tamanho Mínimo Amostra (IC Amplitude 20ms): {n_min} amostras")
                
                print("\nAnálise de SLA (Limite: 350 ms):")
                if lim_sup < 350.0:
                    print(f"-> Em conformidade. Limite superior ({lim_sup:.2f} ms) é menor que 350 ms.")
                else:
                    print(f"-> Fora de conformidade. Limite superior ({lim_sup:.2f} ms) ultrapassa ou iguala 350 ms.")
            except Exception as e:
                print(f"Erro ao ler/processar dados: {e}")
            input("\nPressione ENTER para continuar...")
                
        elif op == "2":
            print("\n--- Visualização de Gráficos (Lendo do CSV) ---")
            try:
                dados = inferencia.ler_coluna_csv(caminho_csv, "tempo_resposta")
                
                print("1. Exibindo Curva de Densidade de Probabilidade (KDE)...")
                regressao.gerar_grafico_densidade(
                    dados=dados,
                    titulo="Curva de Densidade: Tempos de Resposta - API REST",
                    x_label="Tempo de Resposta (ms)",
                    y_label="Densidade de Probabilidade",
                    nome_arquivo="distribuicao_cenario_a.png"
                )
                
                print("2. Exibindo Diagrama de Caixa (Boxplot)...")
                regressao.gerar_grafico_boxplot(
                    dados=dados,
                    titulo="Diagrama de Caixa (Boxplot): Tempos de Resposta - API REST",
                    x_label="Tempo de Resposta (ms)",
                    nome_arquivo="boxplot_cenario_a.png"
                )
                
                print("-> Gráficos exibidos e salvos na pasta 'graficos/'")
            except Exception as e:
                print(f"Erro ao carregar gráfico: {e}")
            input("\nPressione ENTER para continuar...")
                
        elif op == "3":
            print("\n--- Redefinição de Parâmetros de Geração ---")
            try:
                n_in = input(f"Novo tamanho da amostra (n) [Atual: {n_atual}]: ").strip()
                media_in = input(f"Nova média populacional [Atual: {media_atual} ms]: ").strip()
                desvio_in = input(f"Novo desvio padrão [Atual: {desvio_atual} ms]: ").strip()
                
                n_atual = int(n_in) if n_in != "" else n_atual
                media_atual = float(media_in) if media_in != "" else media_atual
                desvio_atual = float(desvio_in) if desvio_in != "" else desvio_atual
                
                # Regenera o arquivo CSV com as novas configurações
                novos_dados = gerador.gerar_cenario_a(n=n_atual, media_alvo=media_atual, desvio_alvo=desvio_atual)
                gerador.salvar_csv(caminho_csv, ["tempo_resposta"], novos_dados)
                print("-> Base de dados do Cenário A regenerada com sucesso no arquivo CSV.")
            except ValueError:
                print("[Erro] Entrada de valores inválida. Parâmetros não alterados.")
            input("\nPressione ENTER para continuar...")


# ---------------- SUBMENU CENÁRIO B ----------------
def gerenciar_cenario_b(gerador: GeradorDeDados) -> None:
    caminho_csv = os.path.join("dados", "cenario_b.csv")
    n_atual, media_atual, desvio_atual = 25, 47.0, 8.0
    
    while True:
        print("\n" + "="*55)
        print(" SUBMENU: CENÁRIO B - COMPILADOR")
        print("="*55)
        # Exibe os parâmetros dinâmicos de distribuição no topo do menu
        print(f"Parâmetros Ativos: n = {n_atual} | Média = {media_atual:.1f} s | Desvio = {desvio_atual:.1f} s")
        print("-"*55)
        print("1. Executar Teste de Hipóteses (Teste T Unilateral)")
        print("2. Visualizar Gráfico de Distribuição (Leitura do CSV)")
        print("3. Alterar Parâmetros de Geração de Dados")
        print("0. Voltar ao Menu Anterior")
        print("="*55)
        
        op = input("Escolha uma opção: ").strip()
        
        if op == "0":
            break
            
        elif op == "1":
            print("\n--- Teste de Hipótese (Lendo do CSV) ---")
            try:
                dados = inferencia.ler_coluna_csv(caminho_csv, "tempo_execucao")
                t_calc, t_crit, rejeita, conclusao = inferencia.teste_t_unilateral(dados, mu0=50.0, alpha=0.05)
                
                print(f"Amostra Lida (n):         {len(dados)}")
                print(f"Média Amostral Lida:      {gerador.calcula_media(dados):.4f} s")
                print(f"Estatística t calculada:  {t_calc:.4f}")
                print(f"Valor crítico de t:       {t_crit:.4f}")
                print(f"Decisão (Rejeita H0?):    {rejeita}")
                print(f"\nConclusão:\n{conclusao}")
            except Exception as e:
                print(f"Erro ao ler/processar dados: {e}")
            input("\nPressione ENTER para continuar...")
                
        elif op == "2":
            print("\n--- Visualização de Gráficos (Lendo do CSV) ---")
            try:
                dados = inferencia.ler_coluna_csv(caminho_csv, "tempo_execucao")
                
                print("1. Exibindo Curva de Densidade de Probabilidade (KDE)...")
                regressao.gerar_grafico_densidade(
                    dados=dados,
                    titulo="Curva de Densidade: Tempos de Execução - Compilador",
                    x_label="Tempo de Execução (s)",
                    y_label="Densidade de Probabilidade",
                    nome_arquivo="distribuicao_cenario_b.png"
                )
                
                print("2. Exibindo Diagrama de Caixa (Boxplot)...")
                regressao.gerar_grafico_boxplot(
                    dados=dados,
                    titulo="Diagrama de Caixa (Boxplot): Tempos de Execução - Compilador",
                    x_label="Tempo de Execução (s)",
                    nome_arquivo="boxplot_cenario_b.png"
                )
                
                print("-> Gráficos exibidos e salvos na pasta 'graficos/'")
            except Exception as e:
                print(f"Erro ao carregar gráfico: {e}")
            input("\nPressione ENTER para continuar...")
                
        elif op == "3":
            print("\n--- Redefinição de Parâmetros de Geração ---")
            try:
                n_in = input(f"Novo tamanho da amostra (n) [Atual: {n_atual}]: ").strip()
                media_in = input(f"Nova média populacional [Atual: {media_atual} s]: ").strip()
                desvio_in = input(f"Novo desvio padrão [Atual: {desvio_atual} s]: ").strip()
                
                n_atual = int(n_in) if n_in != "" else n_atual
                media_atual = float(media_in) if media_in != "" else media_atual
                desvio_atual = float(desvio_in) if desvio_in != "" else desvio_atual
                
                novos_dados = gerador.gerar_cenario_b(n=n_atual, media_alvo=media_atual, desvio_alvo=desvio_atual)
                gerador.salvar_csv(caminho_csv, ["tempo_execucao"], novos_dados)
                print("-> Base de dados do Cenário B regenerada com sucesso no arquivo CSV.")
            except ValueError:
                print("[Erro] Entrada de valores inválida. Parâmetros não alterados.")
            input("\nPressione ENTER para continuar...")


# ---------------- SUBMENU CENÁRIO C ----------------
def gerenciar_cenario_c() -> None:
    caminho_csv = os.path.join("dados", "cenario_c.csv")
    
    while True:
        print("\n" + "="*55)
        print(" SUBMENU: CENÁRIO C - CACHE L2 VS IPC")
        print("="*55)
        # Exibe os somatórios populacionais fixos estabelecidos pela prova
        print("Parâmetros Fixos da Prova:")
        print("  - Amostra (n):  15 pares de dados")
        print("  - Somatório X:  75 (Média Cache = 5.0 MB)")
        print("  - Somatório Y:  45 (Média IPC = 3.0)")
        print("  - Somatórios Quadráticos: Sum(x²)=425, Sum(y²)=165, Sum(xy)=260")
        print("-"*55)
        print("1. Executar Análise de Regressão e Correlação (Pearson, R²)")
        print("2. Visualizar Gráficos Estatísticos (Leitura do CSV)")
        print("0. Voltar ao Menu Anterior")
        print("="*55)
        
        op = input("Escolha uma opção: ").strip()
        
        if op == "0":
            break
            
        elif op == "1":
            print("\n--- Regressão e Correlação (Lendo do CSV) ---")
            try:
                x, y = inferencia.ler_par_csv(caminho_csv, "cache_l2", "ipc")
                r = regressao.correlacao_pearson(x, y)
                a, b, r2 = regressao.regressao_linear(x, y)
                previsao_8mb = regressao.prever(8.0, a, b)
                
                print(f"Pares analisados (n):            {len(x)}")
                print(f"Correlação de Pearson (r):       {r:.4f}")
                print(f"Coeficiente de Determinação (R²): {r2:.4f}")
                print(f"Equação Ajustada da Reta:        y = {a:.4f} + ({b:.4f}) * x")
                print(f"IPC previsto para Cache de 8MB:  {previsao_8mb:.4f}")
            except Exception as e:
                print(f"Erro ao ler/processar dados: {e}")
            input("\nPressione ENTER para continuar...")
                
        elif op == "2":
            print("\n--- Carregando Gráficos (Lendo do CSV) ---")
            try:
                x, y = inferencia.ler_par_csv(caminho_csv, "cache_l2", "ipc")
                a, b, _ = regressao.regressao_linear(x, y)
                
                print("Exibindo gráficos de dispersão e reta ajustada...")
                regressao.gerar_e_salvar_graficos(x, y, a, b, "graficos")
                print("-> Gráficos exibidos e salvos na pasta 'graficos/'")
            except Exception as e:
                print(f"Erro ao gerar gráficos: {e}")
            input("\nPressione ENTER para continuar...")


# ---------------- MENU PRINCIPAL ----------------
def main() -> None:
    semente = obter_semente()
    
    # Geração inicial padrão dos arquivos CSV na pasta 'dados/'
    print("\nGerando base de dados nos arquivos CSV...")
    gerador = GeradorDeDados(seed=semente)
    gerador.gerar_e_salvar_todos(pasta_destino="dados")
    print("-> Arquivos de dados padrão preparados com sucesso.")
    
    while True:
        print("\n" + "="*55)
        print(" MENU PRINCIPAL: ESTATÍSTICA DE DESEMPENHO DE SISTEMAS")
        print("="*55)
        print("1. Cenário A - API REST")
        print("2. Cenário B - Compilador")
        print("3. Cenário C - Cache vs IPC")
        print("0. Sair do Programa")
        print("="*55)
        
        opcao = input("Escolha um Cenário: ").strip()
        
        if opcao == "0":
            print("\nFinalizando o programa. Até logo!")
            break
        elif opcao == "1":
            gerenciar_cenario_a(gerador)
        elif opcao == "2":
            gerenciar_cenario_b(gerador)
        elif opcao == "3":
            gerenciar_cenario_c()
        else:
            print("\n[Erro] Opção inválida! Selecione uma opção válida.")


if __name__ == "__main__":
    main()