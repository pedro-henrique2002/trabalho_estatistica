import os
import inferencia
import regressao
from gerador import GeradorDeDados
from scipy import stats  # Importado para recalcular os valores teóricos dinamicamente caso o 'n' mude
import numpy as np


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
            print("\n" + "-"*65)
            print(" COMPARATIVO DE RESULTADOS: CENÁRIO A - API REST")
            print("-"*65)
            try:
                dados = inferencia.ler_coluna_csv(caminho_csv, "tempo_resposta")
                n_lido = len(dados)
                
                # Valores Calculados Amostrais (com aleatoriedade real do CSV)
                lim_inf_c, lim_sup_c, media_c, desvio_c = inferencia.intervalo_confianca(dados, alpha=0.05)
                n_min_c = inferencia.tamanho_amostra(desvio_c, amplitude=20.0, alpha=0.05)
                
                # Valores Teóricos Dinâmicos (Calculados dinamicamente para o 'n' ativo para evitar bugs)
                df_t = n_atual - 1
                if df_t > 0:
                    t_crit_teorico = stats.t.ppf(0.975, df_t)
                    se_t = desvio_atual / (n_atual ** 0.5)
                    me_t = t_crit_teorico * se_t
                    lim_inf_t = media_atual - me_t
                    lim_sup_t = media_atual + me_t
                    n_min_t = inferencia.tamanho_amostra(desvio_atual, amplitude=20.0, alpha=0.05)
                else:
                    lim_inf_t, lim_sup_t, n_min_t = 0.0, 0.0, 0
                
                # Exibição tabulada comparativa
                print(f"{'Métrica Estatística':<28} | {'Valor Calculado (CSV)':<21} | {'Valor Teórico (Prova)':<21}")
                print("-" * 76)
                print(f"{'Tamanho da Amostra (n)':<28} | {n_lido:<21} | {n_atual:<21}")
                print(f"{'Média Amostral (x_bar)':<28} | {media_c:<18.4f} ms | {media_atual:<18.4f} ms")
                print(f"{'Desvio Padrão Amostral (s)':<28} | {desvio_c:<18.4f} ms | {desvio_atual:<18.4f} ms")
                print(f"{'Intervalo de Confiança':<28} | [{lim_inf_c:.2f}; {lim_sup_c:.2f}] ms | [{lim_inf_t:.2f}; {lim_sup_t:.2f}] ms")
                print(f"{'Amostra Mínima (Amp. 20ms)':<28} | {n_min_c:<21} | {n_min_t:<21}")
                print("-" * 76)
                
                print("\nAnálise de SLA (Limite: 350 ms):")
                print(f"-> Amostra Real:  " + ("Em conformidade." if lim_sup_c < 350.0 else "Fora de conformidade."))
                print(f"-> Teórico Prova: " + ("Em conformidade." if lim_sup_t < 350.0 else "Fora de conformidade."))
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
            print("\n" + "-"*65)
            print(" COMPARATIVO DE RESULTADOS: CENÁRIO B - TESTE DE HIPÓTESES")
            print("-"*65)
            try:
                dados = inferencia.ler_coluna_csv(caminho_csv, "tempo_execucao")
                n_lido = len(dados)
                
                # Valores Calculados Amostrais (do CSV)
                t_calc_c, t_crit_c, rejeita_c, _ = inferencia.teste_t_unilateral(dados, mu0=50.0, alpha=0.05)
                media_c = float(np.mean(dados))
                desvio_c = float(np.std(dados, ddof=1))
                
                # Valores Teóricos Dinâmicos (Calculados para o 'n' ativo para evitar bugs)
                df_t = n_atual - 1
                if df_t > 0:
                    t_crit_t = stats.t.ppf(0.05, df_t)
                    t_calc_t = (media_atual - 50.0) / (desvio_atual / (n_atual ** 0.5))
                    rejeita_t = t_calc_t < t_crit_t
                else:
                    t_calc_t, t_crit_t, rejeita_t = 0.0, 0.0, False
                
                print(f"{'Métrica Estatística':<28} | {'Valor Calculado (CSV)':<21} | {'Valor Teórico (Prova)':<21}")
                print("-" * 76)
                print(f"{'Tamanho da Amostra (n)':<28} | {n_lido:<21} | {n_atual:<21}")
                print(f"{'Média Amostral (x_bar)':<28} | {media_c:<18.4f} s  | {media_atual:<18.4f} s")
                print(f"{'Desvio Padrão Amostral (s)':<28} | {desvio_c:<18.4f} s  | {desvio_atual:<18.4f} s")
                print(f"{'Estatística t calculada':<28} | {t_calc_c:<21.4f} | {t_calc_t:<21.4f}")
                print(f"{'Valor Crítico de t':<28} | {t_crit_c:<21.4f} | {t_crit_t:<21.4f}")
                print(f"{'Rejeita H0? (Signif. 5%)':<28} | {str(rejeita_c):<21} | {str(rejeita_t):<21}")
                print("-" * 76)
                
                print("\nConclusão Prática:")
                print(f"-> Amostra Real:  " + ("Novo compilador é eficaz (Rejeita H0)." if rejeita_c else "Sem evidências para rejeitar H0."))
                print(f"-> Teórico Prova: " + ("Novo compilador é eficaz (Rejeita H0)." if rejeita_t else "Sem evidências para rejeitar H0."))
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
            print("\n" + "-"*65)
            print(" COMPARATIVO DE RESULTADOS: CENÁRIO C - REGRESSÃO LINEAR")
            print("-"*65)
            try:
                x, y = inferencia.ler_par_csv(caminho_csv, "cache_l2", "ipc")
                
                # Valores Calculados Amostrais (do CSV)
                r_c = regressao.correlacao_pearson(x, y)
                a_c, b_c, r2_c = regressao.regressao_linear(x, y)
                previsao_8_c = regressao.prever(8.0, a_c, b_c)
                
                # Valores Teóricos Fixos (da Prova)
                r_t = 0.9037
                a_t = -0.5000
                b_t = 0.7000
                r2_t = 0.8167
                previsao_8_t = a_t + b_t * 8.0
                
                print(f"{'Métrica Estatística':<28} | {'Valor Calculado (CSV)':<21} | {'Valor Teórico (Prova)':<21}")
                print("-" * 76)
                print(f"{'Pares Analisados (n)':<28} | {len(x):<21} | {15:<21}")
                print(f"{'Correlação de Pearson (r)':<28} | {r_c:<18.4f} | {r_t:<18.4f}")
                print(f"{'Coeficiente R²':<28} | {r2_c:<18.4f} | {r2_t:<18.4f}")
                print(f"{'Equação Reta de Regressão':<28} | y = {a_c:.2f} + ({b_c:.2f})*x | y = {a_t:.2f} + ({b_t:.2f})*x")
                print(f"{'Previsão IPC (Cache 8MB)':<28} | {previsao_8_c:<18.4f} | {previsao_8_t:<18.4f}")
                print("-" * 76)
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