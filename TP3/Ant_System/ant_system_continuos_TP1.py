import numpy as np

# 1. Definição da Função Objetivo (Minimização)
def objective_function(x):
    x1, x2 = x[0], x[1]
    
    # Penalização explícita caso saia dos limites do domínio
    if not (-15 <= x1 <= -5) or not (-3 <= x2 <= 3):
        return float('inf')
        
    term1 = 100 * np.sqrt(np.abs(x2 - 0.01 * (x1**2)))
    term2 = 0.01 * np.abs(x1 + 10)
    return term1 + term2

# 2. Função principal que encapsula a execução de UMA rodada do ACO_R
def rodar_aco_r(K=50, M=20, N_ITER=100, Q=0.1, XI=0.85, verbose=False):
    DIM = 2
    LB = np.array([-15.0, -3.0])
    UB = np.array([-5.0, 3.0])

    # Inicialização do Arquivo de Soluções
    archive_X = np.random.uniform(LB, UB, (K, DIM))
    archive_F = np.array([objective_function(sol) for sol in archive_X])

    # Ordenar
    idx_sort = np.argsort(archive_F)
    archive_X = archive_X[idx_sort]
    archive_F = archive_F[idx_sort]

    # Loop Principal
    for iteration in range(N_ITER):
        rankings = np.arange(1, K + 1)
        weights = (1.0 / (Q * K * np.sqrt(2 * np.pi))) * np.exp(-((rankings - 1) ** 2) / (2 * (Q * K) ** 2))
        probabilities = weights / np.sum(weights)
        
        new_solutions = []
        
        for _ in range(M):
            guide_idx = np.random.choice(K, p=probabilities)
            guide_sol = archive_X[guide_idx]
            
            new_sol = np.zeros(DIM)
            
            for d in range(DIM):
                distance_sum = np.sum(np.abs(archive_X[:, d] - guide_sol[d]))
                sigma = XI * (distance_sum / (K - 1)) + 1e-6
                
                val = np.random.normal(guide_sol[d], sigma)
                val = np.clip(val, LB[d], UB[d])
                new_sol[d] = val
                
            new_solutions.append(new_sol)
            
        new_solutions = np.array(new_solutions)
        new_F = np.array([objective_function(sol) for sol in new_solutions])
        
        combined_X = np.vstack((archive_X, new_solutions))
        combined_F = np.concatenate((archive_F, new_F))
        
        idx_sort = np.argsort(combined_F)
        archive_X = combined_X[idx_sort[:K]]
        archive_F = combined_F[idx_sort[:K]]
        
        if verbose and ((iteration + 1) % 10 == 0 or iteration == 0):
            print(f"Iteração {iteration+1:03d} -> Melhor F(x): {archive_F[0]:.6f} | x1: {archive_X[0,0]:.4f}, x2: {archive_X[0,1]:.4f}")



    # Retorna o melhor valor de f(x) e as coordenadas [x1, x2]
    return archive_F[0], archive_X[0]