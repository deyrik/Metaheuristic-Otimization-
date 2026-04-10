import random
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ─── Função de Michalewicz ─────────────────────────────────────────────────────
D = 2
M = 10


def maxEmin(numero):
    if numero == 1:
        X_MIN, X_MAX = 0.0, math.pi
        return X_MIN, X_MAX

    elif numero == 2:
        X_MIN, X_MAX = 1.0, 2.5
        return X_MIN, X_MAX

def f(x: list) -> float:
    total = 0.0
    for i in range(1, D + 1):
        xi = x[i - 1]
        total += math.sin(xi) * (math.sin(i * xi**2 / math.pi)) ** (2 * M)
    return -total

def clamp(x: list, X_MIN: float, X_MAX: float) -> list:
    return [max(X_MIN, min(X_MAX, xi)) for xi in x]

def simulated_annealing(
    T_inicial      = 10.0,
    T_final        = 1e-5,
    alpha          = 0.995,   # fator de resfriamento (geométrico)
    iter_por_T     = 50,      # iterações por temperatura
    passo          = 0.5,     # amplitude da perturbação
    verbose        = True,
    dominio        = 1
):
    
    X_MIN, X_MAX = maxEmin(dominio)
    # Solução inicial aleatória
    x = [random.uniform(X_MIN, X_MAX) for _ in range(D)]
    custo_atual = f(x)

    melhor_x = x[:]
    melhor_custo = custo_atual

    T = T_inicial
    historico_custo   = [custo_atual]
    historico_melhor  = [melhor_custo]
    historico_temp    = [T]
    historico_pontos  = [x[:]]
    total_iter = 0
    aceitos_piores = 0
    rejeitados = 0
    n_epocas = 0

    if verbose:
        print(f"{'Época':>6}  {'Temp':>10}  {'x1':>10}  {'x2':>10}  {'f(x)':>12}  {'Melhor':>12}")
        print("─" * 70)

    while T > T_final:
        n_epocas += 1
        for _ in range(iter_por_T):
            # Perturbação gaussiana
            delta = [random.gauss(0, passo) for _ in range(D)]
            nx = clamp([x[i] + delta[i] for i in range(D)], X_MIN, X_MAX)
            nc = f(nx)

            delta_custo = nc - custo_atual

            # Aceita se melhora, ou com probabilidade e^(-Δ/T) se piora
            if delta_custo < 0:
                x = nx[:]
                custo_atual = nc
            else:
                prob = math.exp(-delta_custo / T)
                if random.random() < prob:
                    x = nx[:]
                    custo_atual = nc
                    aceitos_piores += 1
                else:
                    rejeitados += 1

            if custo_atual < melhor_custo:
                melhor_custo = custo_atual
                melhor_x = x[:]

            total_iter += 1
            historico_custo.append(custo_atual)
            historico_melhor.append(melhor_custo)
            historico_temp.append(T)
            historico_pontos.append(x[:])

        # Resfriamento geométrico
        T *= alpha

        if verbose and (n_epocas % 100 == 0 or n_epocas == 1):
            print(f"{n_epocas:>6}  {T:>10.6f}  {x[0]:>10.6f}  {x[1]:>10.6f}  "
                  f"{custo_atual:>12.8f}  {melhor_custo:>12.8f}")

    if verbose:
        print("─" * 70)
        print(f"\nMelhor solução  :  x1 = {melhor_x[0]:.8f},  x2 = {melhor_x[1]:.8f}")
        print(f"Melhor f(x)     :  {melhor_custo:.10f}")
        print(f"Ótimo global    :  f ≈ -1.8013 (d=2, m=10)")
        print(f"Gap             :  {abs(melhor_custo - (-1.8013)):.2e}")
        print(f"Total iterações :  {total_iter}")
        print(f"Épocas          :  {n_epocas}")
        print(f"Aceitos piores  :  {aceitos_piores}")
        print(f"Rejeitados      :  {rejeitados}")

    return {
        "melhor_x": melhor_x,
        "melhor_custo": melhor_custo,
        "historico_custo": historico_custo,
        "historico_melhor": historico_melhor,
        "historico_temp": historico_temp,
        "historico_pontos": historico_pontos,
        "total_iter": total_iter,
        "aceitos_piores": aceitos_piores,
        "n_epocas": n_epocas,
    }

def visualizar(resultado, dominio=1):
    
    X_MIN, X_MAX = maxEmin(dominio)

    fig = plt.figure(figsize=(20, 6))
    fig.suptitle(
        r"Simulated Annealing — Função de Michalewicz"
        "\n"
        r"$f(\mathbf{x}) = -\sum_{i=1}^{d}\sin(x_i)\,\sin^{2m}\!\left(\frac{i\,x_i^2}{\pi}\right)$"
        r"$\quad d=2,\; m=10,\; " + f"{X_MIN} \leq x_1, x_2 \leq {X_MAX}$",
        fontsize=12, fontweight="bold"
    )

    res = 300
    x1g = np.linspace(X_MIN, X_MAX, res)
    x2g = np.linspace(X_MIN, X_MAX, res)
    X1G, X2G = np.meshgrid(x1g, x2g)
    ZG = np.vectorize(lambda a, b: f([a, b]))(X1G, X2G)

    pts = resultado["historico_pontos"]
    px  = [p[0] for p in pts]
    py  = [p[1] for p in pts]
    n   = len(pts)
    iters = list(range(n))

    # ── Painel 1: Mapa de calor + trajetória ──────────────────────────────────
    ax1 = fig.add_subplot(1, 4, 1)
    ax1.set_title("Superfície e trajetória", fontsize=11)
    cf = ax1.contourf(X1G, X2G, ZG, levels=50, cmap="plasma", alpha=0.9)
    ax1.contour(X1G, X2G, ZG, levels=20, colors="white", linewidths=0.3, alpha=0.3)
    plt.colorbar(cf, ax=ax1, fraction=0.046, pad=0.04)

    # Colorir trajetória pela temperatura (quente=início, frio=fim)
    cores = plt.cm.cool(np.linspace(0.0, 1.0, n))
    step = max(1, n // 3000)  # evita plotar milhões de segmentos
    for i in range(0, n - step, step):
        ax1.plot([px[i], px[i+step]], [py[i], py[i+step]],
                 color=cores[i], lw=0.5, alpha=0.6)

    ax1.scatter(px[0], py[0], s=120, color="#FFD700", zorder=6,
                edgecolors="white", lw=1.5, label="Início")
    ax1.scatter(resultado["melhor_x"][0], resultado["melhor_x"][1],
                s=250, color="white", marker="*", zorder=7, lw=1,
                label=f"Melhor encontrado")
    ax1.scatter([2.2029], [1.5708], s=150, color="#FF4444", marker="x",
                linewidths=2, zorder=8, label="Ótimo global")
    ax1.set_xlabel("$x_1$"); ax1.set_ylabel("$x_2$")
    ax1.set_xlim(X_MIN, X_MAX); ax1.set_ylim(X_MIN, X_MAX)
    ax1.legend(fontsize=8, loc="upper left")

    # ── Painel 2: Superfície 3D ───────────────────────────────────────────────
    ax2 = fig.add_subplot(1, 4, 2, projection="3d")
    ax2.set_title("Superfície 3D", fontsize=11)
    x1s = np.linspace(X_MIN, X_MAX, 100)
    x2s = np.linspace(X_MIN, X_MAX, 100)
    X1S, X2S = np.meshgrid(x1s, x2s)
    ZS = np.vectorize(lambda a, b: f([a, b]))(X1S, X2S)
    ax2.plot_surface(X1S, X2S, ZS, cmap="plasma", alpha=0.88,
                     linewidth=0, antialiased=True)
    ax2.scatter([resultado["melhor_x"][0]], [resultado["melhor_x"][1]],
                [resultado["melhor_custo"]], s=120, color="white",
                zorder=10, edgecolors="black", lw=1.5)
    ax2.set_xlabel("$x_1$"); ax2.set_ylabel("$x_2$"); ax2.set_zlabel("$f(x)$")
    ax2.view_init(elev=35, azim=-130)

    # ── Painel 3: Convergência do custo ──────────────────────────────────────
    ax3 = fig.add_subplot(1, 4, 3)
    ax3.set_title("Convergência do custo", fontsize=11)
    ax3.plot(iters, resultado["historico_custo"],
             color="#C084FC", lw=0.4, alpha=0.5, label="Custo atual")
    ax3.plot(iters, resultado["historico_melhor"],
             color="#7C3AED", lw=2, label="Melhor global")
    ax3.axhline(-1.8013, color="#22C55E", linestyle="--", lw=1.3,
                label="Ótimo global (−1.8013)")
    ax3.axhline(resultado["melhor_custo"], color="#F59E0B", linestyle=":",
                lw=1.2, label=f"Encontrado ({resultado['melhor_custo']:.5f})")
    ax3.fill_between(iters, resultado["historico_custo"],
                     resultado["historico_melhor"], alpha=0.08, color="#7C3AED")
    ax3.set_xlabel("Iteração"); ax3.set_ylabel("f(x)")
    ax3.legend(fontsize=8)
    ax3.grid(True, linestyle=":", alpha=0.4)

    gap = abs(resultado["melhor_custo"] - (-1.8013))
    ax3.annotate(
        f"x1* = {resultado['melhor_x'][0]:.5f}\n"
        f"x2* = {resultado['melhor_x'][1]:.5f}\n"
        f"f*  = {resultado['melhor_custo']:.6f}\n"
        f"Gap = {gap:.2e}\n"
        f"Iterações: {resultado['total_iter']}",
        xy=(0.03, 0.97), xycoords="axes fraction", va="top", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.45", fc="white", ec="#CCCCCC", alpha=0.92)
    )

    # ── Painel 4: Curva de temperatura (schedule) ─────────────────────────────
    ax4 = fig.add_subplot(1, 4, 4)
    ax4.set_title("Curva de resfriamento (schedule)", fontsize=11)

    temps = resultado["historico_temp"]
    ax4.plot(iters, temps, color="#EF4444", lw=1.5, label="Temperatura T")
    ax4.set_xlabel("Iteração"); ax4.set_ylabel("T", color="#EF4444")
    ax4.tick_params(axis="y", labelcolor="#EF4444")
    ax4.set_yscale("log")
    ax4.grid(True, linestyle=":", alpha=0.4)

    # Eixo secundário: probabilidade de aceitar solução 10% pior
    ax4b = ax4.twinx()
    delta_ref = 0.10   # Δf = 0.10 como referência
    prob_vals = [math.exp(-delta_ref / max(t, 1e-10)) for t in temps]
    ax4b.plot(iters, prob_vals, color="#3B82F6", lw=1.2, linestyle="--",
              alpha=0.8, label="P(aceitar Δf=0.1)")
    ax4b.set_ylabel("Probabilidade de aceitar piora", color="#3B82F6")
    ax4b.tick_params(axis="y", labelcolor="#3B82F6")
    ax4b.set_ylim(0, 1)

    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4b.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc="center right")

    plt.tight_layout()
    plt.savefig("data/simulated_annealing_michalewiczDDD.png", dpi=150, bbox_inches="tight")
    print("Gráfico salvo: simulated_annealing_michalewiczDDD.png")

# ─── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    random.seed(42)
    dominio = 1  
    resultado = simulated_annealing(
        T_inicial   = 10.0,
        T_final     = 1e-5,
        alpha       = 0.995,
        iter_por_T  = 50,
        passo       = 0.5,
        verbose     = True,
        dominio     = dominio
    )
    visualizar(resultado, dominio=dominio)