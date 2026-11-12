import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import src.buscaTabu as bt
import src.buscaTabu2 as bt2
import src.simulateAnilling as sa
import src.simulateAnilling2 as sa2
import random
import numpy as np
import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

def ler_json(caminho_json: str) -> list[dict]:
    """
    Lê o arquivo JSON de resultados e retorna uma lista de dicts, cada um com:
      - nome_arquivo : string formatada para usar no nome do arquivo salvo
      - titulo       : título legível para o gráfico
      - algoritmo    : "Busca Tabu" ou "Simulated Annealing"
      - funcao       : 1 ou 2
      - dominio      : "A" ou "B"
      - media        : float
      - minimo       : float
      - maximo       : float
      - desvio_padrao: float
      - valores      : list[float] — os 30 resultados para plotar
    """
    with open(caminho_json, "r", encoding="utf-8") as fh:
        dados = json.load(fh)

    blocos = []
    for exp in dados["experimentos"]:
        algo_curto = "BT" if exp["algoritmo"] == "Busca Tabu" else "SA"
        nome_arquivo = f"{algo_curto}_Func{exp['funcao']}_Dom{exp['dominio']}"
        titulo = (
            f"{exp['algoritmo']} | "
            f"Função {exp['funcao']} | "
            f"Domínio {exp['dominio']}"
        )

        blocos.append({
            "nome_arquivo":  nome_arquivo,
            "titulo":        titulo,
            "algoritmo":     exp["algoritmo"],
            "funcao":        exp["funcao"],
            "dominio":       exp["dominio"],
            "media":         exp["media"],
            "minimo":        exp["minimo"],
            "maximo":        exp["maximo"],
            "desvio_padrao": exp["desvio_padrao"],
            "valores":       exp["resultados_30"],
        })

    return blocos

def plotar_boxplot(bloco: dict, pasta_saida: str = "data/boxplots") -> None:
    """
    Recebe um bloco retornado por ler_json(), plota o boxplot e salva o arquivo.
    """
    os.makedirs(pasta_saida, exist_ok=True)

    valores = bloco["valores"]
    media   = bloco["media"]
    minimo  = bloco["minimo"]
    maximo  = bloco["maximo"]
    desvio  = bloco["desvio_padrao"]

    fig, ax = plt.subplots(figsize=(7, 6))
    fig.suptitle(bloco["titulo"], fontsize=13, fontweight="bold")

    # Boxplot
    bp = ax.boxplot(
        valores,
        vert        = True,
        patch_artist= True,
        widths      = 0.5,
        medianprops = dict(color="#1D9E75", linewidth=2.5),
        boxprops    = dict(facecolor="#AFA9EC", color="#534AB7", linewidth=1.5),
        whiskerprops= dict(color="#534AB7", linewidth=1.5),
        capprops    = dict(color="#534AB7", linewidth=2),
        flierprops  = dict(marker="o", color="#D85A30", markersize=6,
                           markerfacecolor="#D85A30", alpha=0.7),
    )

    # Pontos individuais (jitter) para mostrar distribuição real
    jitter = np.random.uniform(-0.08, 0.08, size=len(valores))
    ax.scatter(1 + jitter, valores, color="#534AB7", alpha=0.4, s=25, zorder=5)

    # Linha da média
    ax.axhline(media, color="#E11D48", linestyle="--", linewidth=1.5,
               label=f"Média: {media:.6f}", zorder=4)

    # Anotação com estatísticas
    stats_txt = (
        f"Média:   {media:.6f}\n"
        f"Mínimo:  {minimo:.6f}\n"
        f"Máximo:  {maximo:.6f}\n"
        f"Desvio:  {desvio:.6f}\n"
        f"N:       {len(valores)}"
    )
    ax.text(
        0.97, 0.97, stats_txt,
        transform=ax.transAxes, va="top", ha="right", fontsize=9,
        fontfamily="monospace",
        bbox=dict(boxstyle="round,pad=0.45", fc="white", ec="#CCCCCC", alpha=0.92)
    )

    ax.set_ylabel("f(x) — valor da função objetivo", fontsize=11)
    ax.set_xticks([1])
    ax.set_xticklabels([bloco["algoritmo"]], fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(True, axis="y", linestyle=":", alpha=0.5)

    caminho = os.path.join(pasta_saida, f"{bloco['nome_arquivo']}.png")
    plt.tight_layout()
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Boxplot salvo em: {caminho}")

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

    # ── Gera boxplots ──────────────────────────────────────────────────────────────
    blocos = ler_json("data/resultados.json")
    for bloco in blocos:
        plotar_boxplot(bloco, pasta_saida="data/boxplots")

