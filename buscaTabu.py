import random
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
import os

# ─── Função objetivo ───────────────────────────────────────────────────────────
# f(x1, x2) = 100 * sqrt(|x2 - 0.01*x1²|) + 0.01 * |x1 + 10|
# Domínio A: -15 <= x1 <= -5,  -3 <= x2 <= 3
# Dominio B: -11 <= x1 <= -9, e 0 <= x2 <= 2

def f(x1, x2):
    return 100.0 * math.sqrt(abs(x2 - 0.01 * x1**2)) + 0.01 * abs(x1 + 10)

# Restrições do domínio
#X1_MIN, X1_MAX = -15.0, -5.0
#X2_MIN, X2_MAX = -3.0,   3.0
X1_MIN, X1_MAX = -11.0, -9.0
X2_MIN, X2_MAX = 0.0, 2.0

def clamp(x1, x2):
    return max(X1_MIN, min(X1_MAX, x1)), max(X2_MIN, min(X2_MAX, x2))

# ─── Busca Tabu contínua ───────────────────────────────────────────────────────
def busca_tabu(
    tamanho_tabu   = 10,
    max_iteracoes  = 300,
    n_vizinhos     = 20,
    passo_inicial  = 2.0,
    fator_reducao  = 0.98,
    verbose        = True,
):
    # Solução inicial aleatória
    x1 = random.uniform(X1_MIN, X1_MAX)
    x2 = random.uniform(X2_MIN, X2_MAX)
    custo_atual = f(x1, x2)

    melhor_x1, melhor_x2 = x1, x2
    melhor_custo = custo_atual

    lista_tabu = []          # lista de soluções proibidas (x1, x2)
    historico_custo  = [custo_atual]
    historico_melhor = [melhor_custo]
    historico_pontos = [(x1, x2)]
    passo = passo_inicial
    aspiracoes = 0

    if verbose:
        print(f"{'Iter':>5}  {'x1':>8}  {'x2':>8}  {'f(x)':>12}  {'Melhor':>12}  {'Passo':>8}")
        print("─" * 60)

    for it in range(1, max_iteracoes + 1):
        melhor_viz_custo = math.inf
        melhor_viz_x1 = melhor_viz_x2 = None
        eh_aspiracao = False

        # Gera n_vizinhos candidatos por perturbação aleatória
        for _ in range(n_vizinhos):
            ang = random.uniform(0, 2 * math.pi)
            r   = random.uniform(0.1, 1.0) * passo
            nx1 = x1 + r * math.cos(ang)
            nx2 = x2 + r * math.sin(ang)
            nx1, nx2 = clamp(nx1, nx2)
            nc = f(nx1, nx2)

            # Verifica se está na lista tabu (por proximidade)
            tabu = any(math.hypot(nx1 - tx1, nx2 - tx2) < 0.05
                       for tx1, tx2 in lista_tabu)

            # Critério de aspiração: aceita tabu se supera o melhor global
            if tabu and nc < melhor_custo:
                melhor_viz_custo = nc
                melhor_viz_x1, melhor_viz_x2 = nx1, nx2
                eh_aspiracao = True
            elif not tabu and nc < melhor_viz_custo:
                melhor_viz_custo = nc
                melhor_viz_x1, melhor_viz_x2 = nx1, nx2
                eh_aspiracao = False

        if melhor_viz_x1 is None:
            # Todos tabu — relaxa e tenta novamente
            passo *= 1.2
            continue

        x1, x2 = melhor_viz_x1, melhor_viz_x2
        custo_atual = melhor_viz_custo

        # Atualiza lista tabu
        if not eh_aspiracao:
            lista_tabu.append((x1, x2))
            if len(lista_tabu) > tamanho_tabu:
                lista_tabu.pop(0)

        if custo_atual < melhor_custo:
            melhor_custo = custo_atual
            melhor_x1, melhor_x2 = x1, x2

        if eh_aspiracao:
            aspiracoes += 1

        # Reduz passo gradualmente (intensificação)
        passo *= fator_reducao
        passo = max(passo, 0.01)

        historico_custo.append(custo_atual)
        historico_melhor.append(melhor_custo)
        historico_pontos.append((x1, x2))

        if verbose and (it % 50 == 0 or it == 1):
            print(f"{it:>5}  {x1:>8.4f}  {x2:>8.4f}  {custo_atual:>12.6f}  {melhor_custo:>12.6f}  {passo:>8.4f}")

    if verbose:
        print("─" * 60)
        print(f"\nMelhor solução:  x1 = {melhor_x1:.6f}, x2 = {melhor_x2:.6f}")
        print(f"Melhor f(x):     {melhor_custo:.8f}")
        print(f"Aspirações:      {aspiracoes}")

    return {
        "melhor_x1": melhor_x1,
        "melhor_x2": melhor_x2,
        "melhor_custo": melhor_custo,
        "historico_custo": historico_custo,
        "historico_melhor": historico_melhor,
        "historico_pontos": historico_pontos,
        "aspiracoes": aspiracoes,
    }

# ─── Visualização ──────────────────────────────────────────────────────────────
def visualizar(resultado):
    fig = plt.figure(figsize=(16, 6))
    fig.suptitle(
        r"Busca Tabu — $f(x_1, x_2) = 100\sqrt{|x_2 - 0.01\,x_1^2|} + 0.01\,|x_1 + 10|$",
        fontsize=13, fontweight="bold"
    )

    # ── Grade para superfície ──
    x1g = np.linspace(X1_MIN, X1_MAX, 300)
    x2g = np.linspace(X2_MIN, X2_MAX, 300)
    X1G, X2G = np.meshgrid(x1g, x2g)
    ZG = np.vectorize(f)(X1G, X2G)

    # ── Painel 1: Contorno + trajetória ──
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.set_title("Superfície de custo e trajetória", fontsize=11)
    cf = ax1.contourf(X1G, X2G, ZG, levels=40, cmap="viridis_r", alpha=0.85)
    ax1.contour(X1G, X2G, ZG, levels=15, colors="white", linewidths=0.4, alpha=0.4)
    plt.colorbar(cf, ax=ax1, fraction=0.046, pad=0.04)

    pts = resultado["historico_pontos"]
    px = [p[0] for p in pts]
    py = [p[1] for p in pts]
    n  = len(pts)
    cores = plt.cm.plasma(np.linspace(0.15, 0.95, n))
    for i in range(n - 1):
        ax1.plot([px[i], px[i+1]], [py[i], py[i+1]], color=cores[i], lw=0.8, alpha=0.7)

    ax1.scatter(px[0], py[0], s=120, color="#FFD700", zorder=6, edgecolors="white", lw=1.5, label="Início")
    ax1.scatter(resultado["melhor_x1"], resultado["melhor_x2"],
                s=200, color="#FF3333", marker="*", zorder=7, edgecolors="white", lw=1, label="Melhor")

    ax1.set_xlabel("$x_1$"); ax1.set_ylabel("$x_2$")
    ax1.legend(fontsize=9, loc="upper right")

    # ── Painel 2: Superfície 3D ──
    ax2 = fig.add_subplot(1, 3, 2, projection="3d")
    ax2.set_title("Superfície 3D", fontsize=11)
    x1s = np.linspace(X1_MIN, X1_MAX, 80)
    x2s = np.linspace(X2_MIN, X2_MAX, 80)
    X1S, X2S = np.meshgrid(x1s, x2s)
    ZS = np.vectorize(f)(X1S, X2S)
    ax2.plot_surface(X1S, X2S, ZS, cmap="viridis_r", alpha=0.85, linewidth=0, antialiased=True)
    ax2.scatter([resultado["melhor_x1"]], [resultado["melhor_x2"]], [resultado["melhor_custo"]],
                s=100, color="#FF3333", zorder=10)
    ax2.set_xlabel("$x_1$"); ax2.set_ylabel("$x_2$"); ax2.set_zlabel("$f(x)$")
    ax2.view_init(elev=30, azim=-120)

    # ── Painel 3: Evolução do custo ──
    ax3 = fig.add_subplot(1, 3, 3)
    ax3.set_title("Evolução do custo", fontsize=11)
    iters = list(range(len(resultado["historico_custo"])))
    ax3.plot(iters, resultado["historico_custo"], color="#AFA9EC", lw=1, alpha=0.7, label="Custo atual")
    ax3.plot(iters, resultado["historico_melhor"], color="#534AB7", lw=2.5, label="Melhor global")
    ax3.axhline(resultado["melhor_custo"], color="#1D9E75", linestyle="--", lw=1.2,
                label=f"Ótimo: {resultado['melhor_custo']:.4f}")
    ax3.fill_between(iters, resultado["historico_custo"], resultado["historico_melhor"],
                     alpha=0.1, color="#534AB7")
    ax3.set_xlabel("Iteração"); ax3.set_ylabel("f(x)")
    ax3.legend(fontsize=9)
    ax3.grid(True, linestyle=":", alpha=0.4)

    ax3.annotate(
        f"x1* = {resultado['melhor_x1']:.4f}\nx2* = {resultado['melhor_x2']:.4f}\nf*  = {resultado['melhor_custo']:.6f}",
        xy=(0.03, 0.97), xycoords="axes fraction", va="top", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#CCCCCC", alpha=0.9)
    )

    # 1. Garante que a pasta 'data' existe para evitar erros
    if not os.path.exists("data"):
        os.makedirs("data")

    # 2. Salva usando o caminho relativo
    plt.tight_layout()
    plt.savefig("data/busca_tabu_func.png", dpi=150, bbox_inches="tight")
    print("\nGráfico salvo em: data/busca_tabu_func.png")

# ─── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    random.seed(99)
    resultado = busca_tabu(
        tamanho_tabu  = 12,
        max_iteracoes = 300,
        n_vizinhos    = 30,
        passo_inicial = 2.5,
        fator_reducao = 0.97,
        verbose       = True,
    )
    visualizar(resultado)