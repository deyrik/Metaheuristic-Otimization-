import numpy as np

# 1. Definição da Função Objetivo com Penalidades
def fitness_function(x):
    x1, x2, u1, u2 = x[0], x[1], x[2], x[3]
    
    # 1.1 Penalização severa se sair dos limites básicos do domínio
    # A restrição x1, x2, u1, u2 >= 0 é rigorosa pois x1**0.6 não aceita negativos
    if x1 < 0 or x2 < 0 or u1 < 0 or u2 < 0 or x1 > 3 or u2 > 1:
        return float('inf')
        
    # 1.2 Cálculo da Função Objetivo Original
    # f(x) = x1^0.6 + x2^0.6 - 6*x1 - 4*u1 + 3*u2
    f_x = (x1**0.6) + (x2**0.6) - 6*x1 - 4*u1 + 3*u2
    
    # 1.3 Avaliação das Restrições (Constraints)
    penalty = 0.0
    
    # Restrição de Igualdade transformada: |x2 - 3x1 - 3u1| - 0.0001 <= 0
    h1 = abs(x2 - 3*x1 - 3*u1) - 0.0001
    if h1 > 0:
        penalty += h1**2  # Elevamos ao quadrado para penalizar erros maiores exponencialmente
        
    # Restrição de Desigualdade 1: x1 + 2u1 <= 4 -> x1 + 2u1 - 4 <= 0
    g1 = x1 + 2*u1 - 4
    if g1 > 0:
        penalty += g1**2
        
    # Restrição de Desigualdade 2: x2 + 2u2 <= 4 -> x2 + 2u2 - 4 <= 0
    g2 = x2 + 2*u2 - 4
    if g2 > 0:
        penalty += g2**2
        
    # 1.4 Retorno com Fator de Penalidade (R)
    # R é um número grande. Se penalty for 0 (solução válida), retorna apenas f_x.
    R = 100000.0 
    return f_x + (R * penalty)

# 2. Função principal que encapsula a execução de UMA rodada do ACO_R
def rodar_aco_r(K=100, M=40, N_ITER=200, Q=0.1, XI=0.85, verbose=False):
    DIM = 4 # Agora temos 4 variáveis: [x1, x2, u1, u2]
    
    # Limites deduzidos do problema para inicializar a colônia
    LB = np.array([0.0, 0.0, 0.0, 0.0])
    UB = np.array([3.0, 4.0, 2.0, 1.0])

    # Inicialização do Arquivo de Soluções
    archive_X = np.random.uniform(LB, UB, (K, DIM))
    archive_F = np.array([fitness_function(sol) for sol in archive_X])

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
                
                # Garantir que a formiga não tente testar variáveis negativas 
                # (evita erro matemático nas potências fracionárias)
                val = max(0.0, val)
                new_sol[d] = val
                
            new_solutions.append(new_sol)
            
        new_solutions = np.array(new_solutions)
        new_F = np.array([fitness_function(sol) for sol in new_solutions])
        
        combined_X = np.vstack((archive_X, new_solutions))
        combined_F = np.concatenate((archive_F, new_F))
        
        idx_sort = np.argsort(combined_F)
        archive_X = combined_X[idx_sort[:K]]
        archive_F = combined_F[idx_sort[:K]]
        
        if verbose and ((iteration + 1) % 10 == 0 or iteration == 0):
            print(f"Iteração {iteration+1:03d} -> Melhor F(x): {archive_F[0]:.6f}")

    # Retorna o melhor valor de f(x) e as coordenadas [x1, x2, u1, u2]
    return archive_F[0], archive_X[0]