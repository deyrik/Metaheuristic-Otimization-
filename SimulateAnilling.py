import random, math, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ─── Função objetivo ───────────────────────────────────────────────────────────
# f(x1, x2) = 100 * sqrt(|x2 - 0.01*x1²|) + 0.01 * |x1 + 10|
# Domínio: -15 <= x1 <= -5,  -3 <= x2 <= 3



def f(x1, x2):
    return 100.0 * math.sqrt(abs(x2 - 0.01 * x1**2)) + 0.01 * abs(x1 + 10)

def maxEmin(numero):
    if numero == 1:
        X1_MIN, X1_MAX = -15.0, -5.0 
        X2_MIN, X2_MAX =  -3.0,  3.0   
        return X1_MIN, X1_MAX, X2_MIN, X2_MAX

    elif numero == 2:
        X1_MIN, X1_MAX = -11.0, -9.0   
        X2_MIN, X2_MAX =   0.0,  2.0 
        return X1_MIN, X1_MAX, X2_MIN, X2_MAX

def clamp(x1, x2, X1_MIN, X1_MAX, X2_MIN, X2_MAX):
    return max(X1_MIN, min(X1_MAX, x1)), max(X2_MIN, min(X2_MAX, x2))

# ─── Simulated Annealing ───────────────────────────────────────────────────────
def simulated_annealing(
    T_inicial   = 50.0,
    T_final     = 1e-6,
    alpha       = 0.995,
    iter_por_T  = 60,
    passo       = 1.5,
    verbose     = True,
    dominio     = 1
):
    
    X1_MIN, X1_MAX, X2_MIN, X2_MAX = maxEmin(dominio)

    x1 = random.uniform(X1_MIN, X1_MAX)
    x2 = random.uniform(X2_MIN, X2_MAX)
    custo_atual = f(x1, x2)

    melhor_x1, melhor_x2 = x1, x2
    melhor_custo = custo_atual

    T = T_inicial
    hist_custo   = [custo_atual]
    hist_melhor  = [melhor_custo]
    hist_temp    = [T]
    hist_pts     = [(x1, x2)]
    total_iter   = 0
    aceitos_piores = 0
    n_epocas = 0

    if verbose:
        print(f"{'Época':>6}  {'Temp':>10}  {'x1':>10}  {'x2':>10}  {'f(x)':>12}  {'Melhor':>12}")
        print("─" * 70)

    while T > T_final:
        n_epocas += 1
        for _ in range(iter_por_T):
            # Perturbação gaussiana independente em cada eixo
            nx1 = x1 + random.gauss(0, passo)
            nx2 = x2 + random.gauss(0, passo * 0.4)   # x2 tem domínio menor
            nx1, nx2 = clamp(nx1, nx2, X1_MIN, X1_MAX, X2_MIN, X2_MAX)
            nc = f(nx1, nx2)

            delta = nc - custo_atual
            if delta < 0 or random.random() < math.exp(-delta / T):
                x1, x2 = nx1, nx2
                custo_atual = nc
                if delta > 0:
                    aceitos_piores += 1

            if custo_atual < melhor_custo:
                melhor_custo = custo_atual
                melhor_x1, melhor_x2 = x1, x2

            total_iter += 1
            hist_custo.append(custo_atual)
            hist_melhor.append(melhor_custo)
            hist_temp.append(T)
            hist_pts.append((x1, x2))

        T *= alpha

        if verbose and (n_epocas % 200 == 0 or n_epocas == 1):
            print(f"{n_epocas:>6}  {T:>10.6f}  {x1:>10.5f}  {x2:>10.5f}  "
                  f"{custo_atual:>12.6f}  {melhor_custo:>12.6f}")

    if verbose:
        print("─" * 70)
        print(f"\nMelhor solução  :  x1 = {melhor_x1:.8f},  x2 = {melhor_x2:.8f}")
        print(f"Melhor f(x)     :  {melhor_custo:.10f}")
        print(f"Total iterações :  {total_iter}")
        print(f"Épocas          :  {n_epocas}")
        print(f"Aceitos piores  :  {aceitos_piores}")

    return {
        "melhor_x1": melhor_x1, "melhor_x2": melhor_x2,
        "melhor_custo": melhor_custo,
        "custo_inicial": hist_custo[0],
        "hist_custo": hist_custo, "hist_melhor": hist_melhor,
        "hist_temp": hist_temp,  "hist_pts": hist_pts,
        "total_iter": total_iter, "aceitos_piores": aceitos_piores,
        "n_epocas": n_epocas,
    }

# ─── Visualização ──────────────────────────────────────────────────────────────
def visualizar(resultado, dominio=1):
    fig = plt.figure(figsize=(20, 6))
    fig.suptitle(
        r"Simulated Annealing — $f(x_1,x_2)=100\sqrt{|x_2-0.01\,x_1^2|}+0.01\,|x_1+10|$"
        "\n"
        r"$-15\leq x_1\leq -5,\quad -3\leq x_2\leq 3$",
        fontsize=12, fontweight="bold"
    )

    X1_MIN, X1_MAX, X2_MIN, X2_MAX = maxEmin(dominio)
    # Grade da superfície
    x1g = np.linspace(X1_MIN, X1_MAX, 300)
    x2g = np.linspace(X2_MIN, X2_MAX, 300)
    X1G, X2G = np.meshgrid(x1g, x2g)
    ZG = np.vectorize(f)(X1G, X2G)

    pts = resultado["hist_pts"]
    px  = [p[0] for p in pts]
    py  = [p[1] for p in pts]
    n   = len(pts)
    iters = list(range(n))

    # ── Painel 1: Mapa de calor + trajetória ──────────────────────────────────
    ax1 = fig.add_subplot(1, 4, 1)
    ax1.set_title("Superfície de custo e trajetória", fontsize=11)
    cf = ax1.contourf(X1G, X2G, ZG, levels=50, cmap="inferno_r", alpha=0.9)
    ax1.contour(X1G, X2G, ZG, levels=20, colors="white", linewidths=0.3, alpha=0.3)
    plt.colorbar(cf, ax=ax1, fraction=0.046, pad=0.04)

    step = max(1, n // 4000)
    cores = plt.cm.cool(np.linspace(0.0, 1.0, n))
    for i in range(0, n - step, step):
        ax1.plot([px[i], px[i+step]], [py[i], py[i+step]],
                 color=cores[i], lw=0.5, alpha=0.55)

    ax1.scatter(px[0], py[0], s=130, color="#FFD700", zorder=6,
                edgecolors="white", lw=1.5, label="Início")
    ax1.scatter(resultado["melhor_x1"], resultado["melhor_x2"],
                s=250, color="white", marker="*", zorder=7,
                label=f"Melhor  f={resultado['melhor_custo']:.4f}")

    ax1.set_xlabel("$x_1$"); ax1.set_ylabel("$x_2$")
    ax1.set_xlim(X1_MIN, X1_MAX); ax1.set_ylim(X2_MIN, X2_MAX)
    ax1.legend(fontsize=8, loc="upper left")

    # ── Painel 2: Superfície 3D ───────────────────────────────────────────────
    ax2 = fig.add_subplot(1, 4, 2, projection="3d")
    ax2.set_title("Superfície 3D", fontsize=11)
    x1s = np.linspace(X1_MIN, X1_MAX, 80)
    x2s = np.linspace(X2_MIN, X2_MAX, 80)
    X1S, X2S = np.meshgrid(x1s, x2s)
    ZS = np.vectorize(f)(X1S, X2S)
    ax2.plot_surface(X1S, X2S, ZS, cmap="inferno_r", alpha=0.88,
                     linewidth=0, antialiased=True)
    ax2.scatter([resultado["melhor_x1"]], [resultado["melhor_x2"]],
                [resultado["melhor_custo"]], s=120, color="white",
                zorder=10, edgecolors="black", lw=1.5)
    ax2.set_xlabel("$x_1$"); ax2.set_ylabel("$x_2$"); ax2.set_zlabel("$f(x)$")
    ax2.view_init(elev=30, azim=-60)

    # ── Painel 3: Convergência do custo ──────────────────────────────────────
    ax3 = fig.add_subplot(1, 4, 3)
    ax3.set_title("Convergência do custo", fontsize=11)
    ax3.plot(iters, resultado["hist_custo"],
             color="#FDA4AF", lw=0.4, alpha=0.5, label="Custo atual")
    ax3.plot(iters, resultado["hist_melhor"],
             color="#E11D48", lw=2, label="Melhor global")
    ax3.axhline(resultado["melhor_custo"], color="#22C55E", linestyle="--",
                lw=1.3, label=f"Melhor ({resultado['melhor_custo']:.5f})")
    ax3.fill_between(iters, resultado["hist_custo"], resultado["hist_melhor"],
                     alpha=0.08, color="#E11D48")
    ax3.set_xlabel("Iteração"); ax3.set_ylabel("f(x)")
    ax3.legend(fontsize=8)
    ax3.grid(True, linestyle=":", alpha=0.4)

    melhora = (1 - resultado["melhor_custo"] / resultado["custo_inicial"]) * 100
    ax3.annotate(
        f"x1* = {resultado['melhor_x1']:.5f}\n"
        f"x2* = {resultado['melhor_x2']:.5f}\n"
        f"f*  = {resultado['melhor_custo']:.6f}\n"
        f"Melhora: {melhora:.1f}%\n"
        f"Aceitos piores: {resultado['aceitos_piores']}",
        xy=(0.97, 0.97), xycoords="axes fraction", va="top", ha="right",
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.45", fc="white", ec="#CCCCCC", alpha=0.92)
    )

    # ── Painel 4: Schedule de temperatura + prob. de aceitar piora ────────────
    ax4 = fig.add_subplot(1, 4, 4)
    ax4.set_title("Schedule de temperatura", fontsize=11)
    temps = resultado["hist_temp"]
    ax4.plot(iters, temps, color="#EF4444", lw=1.5, label="Temperatura T")
    ax4.set_xlabel("Iteração"); ax4.set_ylabel("T", color="#EF4444")
    ax4.tick_params(axis="y", labelcolor="#EF4444")
    ax4.set_yscale("log")
    ax4.grid(True, linestyle=":", alpha=0.4)

    ax4b = ax4.twinx()
    delta_ref = 5.0   # referência de piora (escala da função é maior aqui)
    prob_vals = [math.exp(-delta_ref / max(t, 1e-12)) for t in temps]
    ax4b.plot(iters, prob_vals, color="#3B82F6", lw=1.2, linestyle="--",
              alpha=0.8, label="P(aceitar Δf=5)")
    ax4b.set_ylabel("P(aceitar piora)", color="#3B82F6")
    ax4b.tick_params(axis="y", labelcolor="#3B82F6")
    ax4b.set_ylim(0, 1)

    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4b.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc="center right")

    plt.tight_layout()
    plt.savefig("data/simulated_annealing_michalewiczA.png", dpi=150, bbox_inches="tight")
    print("Gráfico salvo: simulated_annealing_michalewiczA.png")


# ─── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    random.seed(7)
    resultado = simulated_annealing(
        T_inicial  = 50.0,
        T_final    = 1e-6,
        alpha      = 0.995,
        iter_por_T = 60,
        passo      = 1.5,
        verbose    = True,
        dominio    = 1
    )
    visualizar(resultado, dominio=1)