import numpy as np
import json
import os
from datetime import datetime



R = 1000000.0  # Multa estática pesada

# O vetor x representa [x1, x2, x3, x4, x5, x6, x7]
# Limites
lim_inf = np.array([2.6, 0.7, 17.0, 7.3, 7.3, 2.9, 5.0])
lim_sup = np.array([3.6, 0.8, 28.0, 8.3, 8.3, 3.9, 5.5])

def f(x):
    """Função Objetivo Principal"""
    x1, x2, x3, x4, x5, x6, x7 = x
    
    termo1 = 0.7854 * x1 * (x2**2) * (3.3333 * (x3**2) + 14.9334 * x3 - 43.0934)
    termo2 = -1.508 * x1 * ((x6**2) + (x7**2))
    termo3 = 7.477 * ((x6**3) + (x7**3))
    termo4 = 0.7854 * (x4 * (x6**2) + x5 * (x7**2))
    
    return termo1 + termo2 + termo3 + termo4

def g(x):
    """11 Restrições de Desigualdade (Convertidas para g(x) <= 0)"""
    x1, x2, x3, x4, x5, x6, x7 = x
    
    A1 = np.sqrt( (745 * x4 / (x2 * x3))**2 + 16.9e6 )
    B1 = 0.1 * (x6**3)
    
    A2 = np.sqrt( (745 * x5 / (x2 * x3))**2 + 157.5e6 )
    B2 = 0.1 * (x7**3)
    
    return [
        27.0 - (x1 * (x2**2) * x3),                 
        397.5 - (x1 * (x2**2) * (x3**2)),           
        1.93 - (x2 * (x6**4) * x3 / (x4**3)),       
        1.93 - (x2 * (x7**4) * x3 / (x5**3)),      
        (A1 / B1) - 1100.0,                         
        (A2 / B2) - 850.0,                          
        (x2 * x3) - 40.0,                           
        5.0 - (x1 / x2),                            
        (x1 / x2) - 12.0,                           
        1.5 * x6 - x4 + 1.9,                        
        1.5 * x7 - x5 + 1.9                         
    ]

def avaliar_fitness_penalizado(x):
    custo_objetivo = f(x)
    penalidade_total = 0.0
    
    for gi in g(x):
        if gi > 0:
            penalidade_total += gi**2
            
    return custo_objetivo + (R * penalidade_total)

def programacao_evolutiva(mu=300, geracoes=1000, q_torneio=3):
    populacao = np.random.uniform(lim_inf, lim_sup, (mu, 7))
    sigma = (lim_sup - lim_inf) * 0.10
    
    for gen in range(geracoes):
        sigma_atual = sigma * (1.0 - (gen / geracoes))
        if np.all(sigma_atual < 1e-6): sigma_atual = 1e-6
        
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
    
    violacao = sum(max(0, gi) for gi in g(melhor_x))
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
    print("valor tem que ser menor que:  ")
    executar_experimento("Problema 2 - Penalidade Estatica", programacao_evolutiva)
