import numpy as np
import json
import os
import numpy as np
from datetime import datetime

EPSILON = 0.0001
R = 1000000.0  #Multa pesada para estimular a busca por soluções factíveis


# O vetor x representa [x1, x2, u1, u2]
lim_inf = np.array([0.0, 0.0, 0.0, 0.0])

# LIMITES CORRIGIDOS PELA ÁLGEBRA DAS RESTRIÇÕES
# x1 <= 3.0 (dado no problema)
# x2 <= 4.0 (deduzido de x2 + 2u2 <= 4)
# u1 <= 2.0 (deduzido de x1 + 2u1 <= 4)
# u2 <= 1.0 (dado no problema)
lim_sup = np.array([3.0, 4.0, 2.0, 1.0])

def f(x):
    """Função Objetivo""" 
    x1, x2, u1, u2 = x
    return (x1**0.6) + (x2**0.6) - 6*x1 - 4*u1 + 3*u2

def g(x):
    """Restrições de Desigualdade (Convertidas para g(x) <= 0)"""
    x1, x2, u1, u2 = x
    return [
        x1 + 2*u1 - 4.0,  
        x2 + 2*u2 - 4.0   
    ]

def h(x):
    """Restrições de Igualdade (h(x) = 0)"""
    x1, x2, u1, u2 = x
    return [
        x2 - 3*x1 - 3*u1 
    ]

def avaliar_fitness_penalizado(x):
    custo_objetivo = f(x)
    penalidade_total = 0.0
    
    for gi in g(x):
        if gi > 0:
            penalidade_total += gi**2
            
    for hj in h(x):
        violacao = abs(hj) - EPSILON
        if violacao > 0:
            penalidade_total += violacao**2
            
    return custo_objetivo + (R * penalidade_total)

def programacao_evolutiva(mu=300, geracoes=500, q_torneio=5):
    
    populacao = np.random.uniform(lim_inf, lim_sup, (mu, 4))
    sigma = (lim_sup - lim_inf) * 0.10
    
    for gen in range(geracoes):
        sigma_atual = sigma * (1.0 - (gen / geracoes))
        if np.all(sigma_atual < 1e-5): sigma_atual = 1e-5
        
        #mutação 
        ruido_gaussiano = np.random.normal(0, sigma_atual, populacao.shape)
        filhos = populacao + ruido_gaussiano
        
        filhos = np.clip(filhos, lim_inf, lim_sup)
        
        pool_total = np.vstack((populacao, filhos))
        fitness_pool = np.array([avaliar_fitness_penalizado(ind) for ind in pool_total])
        
        vitorias = np.zeros(2 * mu)
        for i in range(2 * mu):
            oponentes = np.random.choice(2 * mu, q_torneio, replace=False)
            for op in oponentes:
                if fitness_pool[i] < fitness_pool[op]:
                    vitorias[i] += 1
                    
        indices_sobreviventes = np.argsort(vitorias)[::-1][:mu]
        populacao = pool_total[indices_sobreviventes]
        
    melhor_idx = np.argmin([avaliar_fitness_penalizado(ind) for ind in populacao])
    melhor_x = populacao[melhor_idx]
    
    custo = f(melhor_x)
    
    violacao = 0.0
    for gi in g(melhor_x):
        if gi > 0: violacao += gi**2
    for hj in h(melhor_x):
        v_h = abs(hj) - EPSILON
        if v_h > 0: violacao += v_h**2
        
    eh_factivel = bool(violacao <= 1e-6)
    return melhor_x, eh_factivel, custo, violacao


os.makedirs("Datas/Estatisticas", exist_ok=True)
def executar_experimento(nome_experimento, funcao_algoritmo, num_execucoes=30):
    print(f"Iniciando {num_execucoes} execuções para: {nome_experimento}...")
    
    resultados_custo = []
    detalhes_execucoes = []
    
    for i in range(num_execucoes):
        melhor_x, eh_factivel, custo, violacao = funcao_algoritmo() 
        resultados_custo.append(custo)
        detalhes_execucoes.append({
            "iteracao": i + 1,
            "melhor_x": list(melhor_x), # numpy arrays não são serializáveis em JSON
            "custo": float(custo),
            "violacao": float(violacao),
            "valido": bool(eh_factivel)
        })
        print(f"  Execução {i+1}/30 concluída. Custo: {custo:.4f}")

    estatisticas = {
        "minimo": float(np.min(resultados_custo)),
        "maximo": float(np.max(resultados_custo)),
        "media": float(np.mean(resultados_custo)),
        "desvio_padrao": float(np.std(resultados_custo))
    }

    dados_finais = {
        "experimento": nome_experimento,
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estatisticas": estatisticas,
        "execucoes": detalhes_execucoes
    }

    caminho_arquivo = f"Datas/Estatisticas/{nome_experimento.replace(' ', '_')}.json"
    with open(caminho_arquivo, 'w') as f:
        json.dump(dados_finais, f, indent=4)
        
    print(f"-> Dados salvos com sucesso em: {caminho_arquivo}\n")





if __name__ == "__main__":
    executar_experimento("Problema 1 - Penalidade Estatica", programacao_evolutiva)