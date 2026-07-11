import numpy as np
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

import Ant_System.ant_system_continuos_TP1 as AS_TP1
import Ant_System.ant_system_continuos_TP2 as AS_TP2

def realizar_experimentos(nome_problema, modulo_otimizacao, num_runs=30):
    """
    Função que executa as rodadas independentes, calcula as estatísticas,
    salva os resultados em JSON e gera o Boxplot para um dado problema.
    """
    print(f"\n{'='*50}")
    print(f" INICIANDO EXPERIMENTOS: {nome_problema}")
    print(f"{'='*50}")
    
    results_f = []
    results_x = []
    
    for i in range(num_runs):
        best_f, best_x = modulo_otimizacao.rodar_aco_r(verbose=False) 
        
        results_f.append(best_f)
        results_x.append(best_x.tolist()) 
        
        print(f"[{nome_problema}] Execução {i+1:02d}/{num_runs:02d} concluída. Melhor F(x): {best_f:.6f}")
        
    results_f_np = np.array(results_f)
    
    # Cálculo das métricas solicitadas
    min_res = float(np.min(results_f_np))
    max_res = float(np.max(results_f_np))
    mean_res = float(np.mean(results_f_np))
    std_res = float(np.std(results_f_np))
    
    best_idx = np.argmin(results_f_np)
    best_overall_x = results_x[best_idx]
    
    # ---------------------------------------------------------
    # ESTRUTURAÇÃO DO ARQUIVO JSON
    # ---------------------------------------------------------
    dados_json = {
        "metadados": {
            "problema": nome_problema,
            "data_execucao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "numero_execucoes": num_runs
        },
        "estatisticas": {
            "minimo_global_fx": min_res,
            "maximo_pior_fx": max_res,
            "media_fx": mean_res,
            "desvio_padrao_fx": std_res,
            "melhores_coordenadas_x": best_overall_x
        },
        "detalhes_por_execucao": [
            {
                "rodada": i + 1,
                "melhor_f": float(results_f[i]),
                "melhor_x": results_x[i]
            } for i in range(num_runs)
        ]
    }
    
    pasta_destino = "Data"
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Define o caminho completo do arquivo dentro da pasta Data
    nome_arquivo_json = os.path.join(pasta_destino, f"resultados_aco_r_{nome_problema}.json")
    
    with open(nome_arquivo_json, 'w', encoding='utf-8') as file:
        json.dump(dados_json, file, indent=4, ensure_ascii=False)
        
    # ---------------------------------------------------------
    # PRINT DOS RESULTADOS NO TERMINAL
    # ---------------------------------------------------------
    # Monta a string de coordenadas independentemente de serem 2 ou 4 variáveis
    str_coords = ", ".join([f"var_{idx+1}={val:.4f}" for idx, val in enumerate(best_overall_x)])
    
    print("\n" + "-"*45)
    print(f" RELATÓRIO ESTATÍSTICO - {nome_problema} (30 RODADAS)")
    print("-"*45)
    print(f"Mínimo (Melhor Fx) : {min_res:.6f}")
    print(f"Máximo (Pior Fx)   : {max_res:.6f}")
    print(f"Média dos Fx       : {mean_res:.6f}")
    print(f"Desvio Padrão      : {std_res:.6f}")
    print(f"Coordenadas do Min : {str_coords}")
    print("-"*45)
    print(f"[!] Dados salvos em: '{nome_arquivo_json}'")

    # ---------------------------------------------------------
    # GERAÇÃO DO BOXPLOT
    # ---------------------------------------------------------
    plt.figure(figsize=(8, 6))
    
    plt.boxplot(results_f, vert=True, patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='darkblue'),
                capprops=dict(color='darkblue', linewidth=1.5),
                whiskerprops=dict(color='darkblue', linewidth=1.5),
                flierprops=dict(marker='o', color='red', alpha=0.5),
                medianprops=dict(color='red', linewidth=2))

    plt.title(f'Distribuição da Função Objetivo F(x) - {nome_problema}', fontsize=14)
    plt.ylabel('Melhor Valor de F(x) Encontrado', fontsize=12)
    plt.xticks([1], [f'ACO_R ({nome_problema})'], fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)


    nome_imagem = os.path.join(pasta_destino, f'boxplot_resultados_{nome_problema}.png')
    plt.savefig(nome_imagem, dpi=300, bbox_inches='tight')
    
    print(f"[!] Boxplot gerado e salvo como: '{nome_imagem}'\n")
    
    # Fecha a figura da memória para não misturar com o gráfico do próximo problema
    plt.close()


if __name__ == "__main__":
    NUMERO_DE_RODADAS = 30
    
    # 1. Executa para o TP1
    realizar_experimentos(nome_problema="TP1", modulo_otimizacao=AS_TP1, num_runs=NUMERO_DE_RODADAS)
    
    # 2. Executa para o TP2
    realizar_experimentos(nome_problema="TP2", modulo_otimizacao=AS_TP2, num_runs=NUMERO_DE_RODADAS)
    
    print("\n[!] Todos os algoritmos finalizaram suas execuções com sucesso.")