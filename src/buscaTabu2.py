import random
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

# ─── Função de Michalewicz ─────────────────────────────────────────────────────
# f(x) = -sum_{i=1}^{d} sin(xi) * sin^(2m)( i*xi² / pi )
# d=2, m=10, domínio: 0 <= x1, x2 <= pi

D = 2
M = 10


def f(x: list) -> float:
    total = 0.0
    for i in range(1, D + 1):
        xi = x[i - 1]
        total += math.sin(xi) * (math.sin(i * xi**2 / math.pi)) ** (2 * M)
    return -total

def maxEmin(numero):
    if numero == 1:
        X_MIN, X_MAX = 0.0, math.pi
        return X_MIN, X_MAX

    elif numero == 2:
        X_MIN, X_MAX = 1.0, 2.5
        return X_MIN, X_MAX

def clamp(x: list, X_MIN: float, X_MAX: float) -> list:
    return [max(X_MIN, min(X_MAX, xi)) for xi in x]

def busca_tabu(
    tamanho_tabu   = 12,
    max_iteracoes  = 500,
    n_vizinhos     = 40,
    passo_inicial  = 1.0,
    fator_reducao  = 0.98,
    raio_tabu      = 0.02,
    verbose        = True,
    limites         = 1
):
    # Pega os limites especificados no tp
    X_MIN, X_MAX = maxEmin(limites)
    print(f"Limites: X_MIN = {X_MIN}, X_MAX = {X_MAX}")

    # Solução inicial aleatória
    x = [random.uniform(X_MIN, X_MAX) for _ in range(D)]
    custo_atual = f(x)

    melhor_x = x[:]
    melhor_custo = custo_atual

    lista_tabu = []
    historico_custo  = [custo_atual]
    historico_melhor = [melhor_custo]
    historico_pontos = [x[:]]
    passo = passo_inicial
    aspiracoes = 0

    if verbose:
        print(f"{'Iter':>5}  {'x1':>10}  {'x2':>10}  {'f(x)':>12}  {'Melhor':>12}  {'Passo':>8}")
        print("─" * 65)

    for it in range(1, max_iteracoes + 1):
        melhor_viz_custo = math.inf
        melhor_viz_x = None
        eh_aspiracao = False

        for _ in range(n_vizinhos):
            # Perturbação polar generalizada para D dimensões
            delta = [random.gauss(0, 1) for _ in range(D)]
            norm  = math.sqrt(sum(d**2 for d in delta)) or 1e-9
            r     = random.uniform(0.1, 1.0) * passo
            nx    = clamp([x[i] + r * delta[i] / norm for i in range(D)], X_MIN, X_MAX)
            nc    = f(nx)

            tabu = any(
                math.sqrt(sum((nx[i] - tx[i])**2 for i in range(D))) < raio_tabu
                for tx in lista_tabu
            )

            if tabu and nc < melhor_custo:
                melhor_viz_custo = nc
                melhor_viz_x = nx[:]
                eh_aspiracao = True
            elif not tabu and nc < melhor_viz_custo:
                melhor_viz_custo = nc
                melhor_viz_x = nx[:]
                eh_aspiracao = False

        if melhor_viz_x is None:
            passo = min(passo * 1.3, passo_inicial)
            continue

        x = melhor_viz_x[:]
        custo_atual = melhor_viz_custo

        if not eh_aspiracao:
            lista_tabu.append(x[:])
            if len(lista_tabu) > tamanho_tabu:
                lista_tabu.pop(0)

        if custo_atual < melhor_custo:
            melhor_custo = custo_atual
            melhor_x = x[:]

        if eh_aspiracao:
            aspiracoes += 1

        passo = max(passo * fator_reducao, 1e-4)
        historico_custo.append(custo_atual)
        historico_melhor.append(melhor_custo)
        historico_pontos.append(x[:])

        if verbose and (it % 100 == 0 or it == 1):
            print(f"{it:>5}  {x[0]:>10.6f}  {x[1]:>10.6f}  {custo_atual:>12.8f}  {melhor_custo:>12.8f}  {passo:>8.5f}")

    if verbose:
        print("─" * 65)
        print(f"\nMelhor solução:  x1 = {melhor_x[0]:.8f}, x2 = {melhor_x[1]:.8f}")
        print(f"Melhor f(x):     {melhor_custo:.10f}")
        print(f"Ótimo global:    f ≈ -1.8013 (conhecido para d=2, m=10)")
        print(f"Aspirações:      {aspiracoes}")

    return {
        "melhor_x": melhor_x,
        "melhor_custo": melhor_custo,
        "historico_custo": historico_custo,
        "historico_melhor": historico_melhor,
        "historico_pontos": historico_pontos,
        "aspiracoes": aspiracoes,
    }

def visualizar(resultado, dominio=1, iteracao=1):

    X_MIN, X_MAX = maxEmin(dominio)

    fig = plt.figure(figsize=(18, 6))
    fig.suptitle(
        r"Busca Tabu — Função de Michalewicz   $f(\mathbf{x}) = -\sum_{i=1}^{d}\sin(x_i)\,\sin^{2m}\!\left(\frac{i\,x_i^2}{\pi}\right)$"
        "\n" + r"$d=2,\; m=10,\; 0 \leq x_1, x_2 \leq \pi$",
        fontsize=12, fontweight="bold"
    )

    # Grade
    res = 300
    x1g = np.linspace(X_MIN, X_MAX, res)
    x2g = np.linspace(X_MIN, X_MAX, res)
    X1G, X2G = np.meshgrid(x1g, x2g)
    ZG = np.vectorize(lambda a, b: f([a, b]))(X1G, X2G)

    pts = resultado["historico_pontos"]
    px  = [p[0] for p in pts]
    py  = [p[1] for p in pts]
    n   = len(pts)

    # ── Painel 1: Mapa de calor + trajetória ──
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.set_title("Superfície de custo e trajetória", fontsize=11)
    cf = ax1.contourf(X1G, X2G, ZG, levels=50, cmap="plasma", alpha=0.9)
    ax1.contour(X1G, X2G, ZG, levels=20, colors="white", linewidths=0.3, alpha=0.35)
    plt.colorbar(cf, ax=ax1, fraction=0.046, pad=0.04)

    cores = plt.cm.cool(np.linspace(0.0, 1.0, n))
    for i in range(n - 1):
        ax1.plot([px[i], px[i+1]], [py[i], py[i+1]], color=cores[i], lw=0.7, alpha=0.75)

    ax1.scatter(px[0], py[0], s=120, color="#FFD700", zorder=6,
                edgecolors="white", lw=1.5, label="Início")
    ax1.scatter(resultado["melhor_x"][0], resultado["melhor_x"][1],
                s=220, color="white", marker="*", zorder=7, lw=1, label="Melhor encontrado")
    # Ótimo global conhecido: aprox (2.20, 1.57)
    ax1.scatter([2.2029], [1.5708], s=150, color="#FF4444", marker="x",
                linewidths=2, zorder=8, label="Ótimo global (≈ -1.8013)")

    ax1.set_xlabel("$x_1$"); ax1.set_ylabel("$x_2$")
    ax1.set_xlim(X_MIN, X_MAX); ax1.set_ylim(X_MIN, X_MAX)
    ax1.legend(fontsize=8, loc="upper left")

    # ── Painel 2: Superfície 3D ──
    ax2 = fig.add_subplot(1, 3, 2, projection="3d")
    ax2.set_title("Superfície 3D", fontsize=11)
    x1s = np.linspace(X_MIN, X_MAX, 100)
    x2s = np.linspace(X_MIN, X_MAX, 100)
    X1S, X2S = np.meshgrid(x1s, x2s)
    ZS = np.vectorize(lambda a, b: f([a, b]))(X1S, X2S)
    ax2.plot_surface(X1S, X2S, ZS, cmap="plasma", alpha=0.88,
                     linewidth=0, antialiased=True)
    ax2.scatter([resultado["melhor_x"][0]], [resultado["melhor_x"][1]],
                [resultado["melhor_custo"]], s=120, color="white",
                zorder=10, edgecolors="black", lw=1)
    ax2.set_xlabel("$x_1$"); ax2.set_ylabel("$x_2$"); ax2.set_zlabel("$f(x)$")
    ax2.view_init(elev=35, azim=-130)

    # ── Painel 3: Convergência ──
    ax3 = fig.add_subplot(1, 3, 3)
    ax3.set_title("Convergência do custo", fontsize=11)
    iters = list(range(len(resultado["historico_custo"])))
    ax3.plot(iters, resultado["historico_custo"],
             color="#C084FC", lw=1, alpha=0.6, label="Custo atual")
    ax3.plot(iters, resultado["historico_melhor"],
             color="#7C3AED", lw=2.5, label="Melhor global")
    ax3.axhline(-1.8013, color="#22C55E", linestyle="--", lw=1.3,
                label=f"Ótimo global (−1.8013)")
    ax3.axhline(resultado["melhor_custo"], color="#F59E0B", linestyle=":",
                lw=1.2, label=f"Encontrado ({resultado['melhor_custo']:.4f})")
    ax3.fill_between(iters, resultado["historico_custo"],
                     resultado["historico_melhor"], alpha=0.1, color="#7C3AED")
    ax3.set_xlabel("Iteração"); ax3.set_ylabel("f(x)")
    ax3.legend(fontsize=8)
    ax3.grid(True, linestyle=":", alpha=0.4)

    gap = abs(resultado["melhor_custo"] - (-1.8013))
    ax3.annotate(
        f"x1* = {resultado['melhor_x'][0]:.5f}\n"
        f"x2* = {resultado['melhor_x'][1]:.5f}\n"
        f"f*  = {resultado['melhor_custo']:.6f}\n"
        f"Gap = {gap:.6f}\n"
        f"Aspirações: {resultado['aspiracoes']}",
        xy=(0.03, 0.97), xycoords="axes fraction", va="top", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.45", fc="white", ec="#CCCCCC", alpha=0.92)
    )

    #Criando pastas e caminhos para salvar os gráficos  
    raiz = "data"
    os.makedirs(raiz, exist_ok=True)

    if dominio == 1:
        pasta = os.path.join(raiz, "BT_Func2_LimiteA")
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, f"{iteracao}_busca_tabu_funcA.png")

    elif dominio == 2:
        pasta = os.path.join(raiz, "BT_Func2_LimiteB")
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, f"{iteracao}_busca_tabu_funcB.png")

    plt.tight_layout()
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\nGráfico salvo em: {caminho}")

# ─── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    #30 seeds diferentes para testar a robustez do algoritmo
    seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 ,
             21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

    dominio = 1 # 1 ou 2

    for seed in seeds:
        random.seed(seed)
        #random.seed(42)
        resultado = busca_tabu(
            tamanho_tabu  = 12,
            max_iteracoes = 500,
            n_vizinhos    = 40,
            passo_inicial = 1.0,
            fator_reducao = 0.98,
            raio_tabu     = 0.02,
            verbose       = True,
            limites       = dominio
        )
        visualizar(resultado, dominio=dominio, iteracao=seed)