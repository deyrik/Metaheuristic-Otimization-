import buscaTabu as bt
import buscaTabu2 as bt2
import simulateAnilling as sa
import simulateAnilling2 as sa2
import random
import numpy as np
import json
import os




def rodar_30(algoritmo_fn, visualizar_fn, seeds, dominio, label_algo, label_func, label_dom, kwargs):
    """
    Roda um algoritmo 30 vezes, coleta os resultados e retorna o bloco de estatísticas.
    """
    resultados_custo = []
    melhor_custo_global = float('inf')
    melhor_resultado = None

    for seed in seeds:
        random.seed(seed)
        resultado = algoritmo_fn(**kwargs)
        visualizar_fn(resultado, dominio=dominio, iteracao=seed)

        custo = resultado.get("melhor_custo")
        resultados_custo.append(custo)

        if custo < melhor_custo_global:
            melhor_custo_global = custo
            melhor_resultado = resultado

    valores = np.array(resultados_custo)

    # Pega as variáveis da melhor solução encontrada (estrutura varia por algoritmo)
    if "melhor_x1" in melhor_resultado:
        best_x1 = melhor_resultado["melhor_x1"]
        best_x2 = melhor_resultado["melhor_x2"]
    else:
        best_x1 = melhor_resultado["melhor_x"][0]
        best_x2 = melhor_resultado["melhor_x"][1]

    bloco = {
        "funcao":        label_func,
        "algoritmo":     label_algo,
        "dominio":       label_dom,
        "media":         round(float(np.mean(valores)),   6),
        "minimo":        round(float(np.min(valores)),    6),
        "maximo":        round(float(np.max(valores)),    6),
        "desvio_padrao": round(float(np.std(valores)),    6),
        "melhor_x1":     round(best_x1, 6),
        "melhor_x2":     round(best_x2, 6),
        "resultados_30": [round(v, 6) for v in resultados_custo],
    }

    print(f"\n{'─'*50}")
    print(f"  {label_algo} | Função {label_func} | Domínio {label_dom}")
    print(f"  Média:   {bloco['media']:.6f}")
    print(f"  Mínimo:  {bloco['minimo']:.6f}")
    print(f"  Máximo:  {bloco['maximo']:.6f}")
    print(f"  Desvio:  {bloco['desvio_padrao']:.6f}")
    print(f"{'─'*50}")

    return bloco

if __name__ == "__main__":

    seeds = list(range(1, 31))
    experimentos = []

    # ── Domínio A (1) e B (2) ──────────────────────────────────────────────────
    for dominio, label_dom in [(1, "A"), (2, "B")]:

        # Busca Tabu — Função 1
        experimentos.append(rodar_30(
            algoritmo_fn  = bt.busca_tabu,
            visualizar_fn = bt.visualizar,
            seeds         = seeds,
            dominio       = dominio,
            label_algo    = "Busca Tabu",
            label_func    = 1,
            label_dom     = label_dom,
            kwargs        = dict(
                tamanho_tabu  = 12,
                max_iteracoes = 300,
                n_vizinhos    = 30,
                passo_inicial = 2.5,
                fator_reducao = 0.97,
                verbose       = False,
                limites       = dominio,
            )
        ))

        # Busca Tabu — Função 2 (Michalewicz)
        experimentos.append(rodar_30(
            algoritmo_fn  = bt2.busca_tabu,
            visualizar_fn = bt2.visualizar,
            seeds         = seeds,
            dominio       = dominio,
            label_algo    = "Busca Tabu",
            label_func    = 2,
            label_dom     = label_dom,
            kwargs        = dict(
                tamanho_tabu  = 12,
                max_iteracoes = 500,
                n_vizinhos    = 40,
                passo_inicial = 1.0,
                fator_reducao = 0.98,
                raio_tabu     = 0.02,
                verbose       = False,
                limites       = dominio,
            )
        ))

        # Simulated Annealing — Função 1
        experimentos.append(rodar_30(
            algoritmo_fn  = sa.simulated_annealing,
            visualizar_fn = sa.visualizar,
            seeds         = seeds,
            dominio       = dominio,
            label_algo    = "Simulated Annealing",
            label_func    = 1,
            label_dom     = label_dom,
            kwargs        = dict(
                T_inicial  = 50.0,
                T_final    = 1e-6,
                alpha      = 0.995,
                iter_por_T = 60,
                passo      = 1.5,
                verbose    = False,
                dominio    = dominio,
            )
        ))

        # Simulated Annealing — Função 2 (Michalewicz)
        experimentos.append(rodar_30(
            algoritmo_fn  = sa2.simulated_annealing,
            visualizar_fn = sa2.visualizar,
            seeds         = seeds,
            dominio       = dominio,
            label_algo    = "Simulated Annealing",
            label_func    = 2,
            label_dom     = label_dom,
            kwargs        = dict(
                T_inicial  = 10.0,
                T_final    = 1e-5,
                alpha      = 0.995,
                iter_por_T = 50,
                passo      = 0.5,
                verbose    = False,
                dominio    = dominio,
            )
        ))

    # ── Salva JSON ─────────────────────────────────────────────────────────────
    os.makedirs("data", exist_ok=True)
    saida = {"experimentos": experimentos}

    with open("data/resultados.json", "w", encoding="utf-8") as fh:
        json.dump(saida, fh, ensure_ascii=False, indent=2)

    print("\nResultados salvos em: data/resultados.json")