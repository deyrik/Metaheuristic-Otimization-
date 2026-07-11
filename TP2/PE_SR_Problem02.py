import numpy as np
import json
import os
import numpy as np
from datetime import datetime

# Limites de Caixa (Box Constraints) do Redutor de Velocidade
lim_inf = np.array([2.6, 0.7, 17.0, 7.3, 7.3, 2.9, 5.0])
lim_sup = np.array([3.6, 0.8, 28.0, 8.3, 8.3, 3.9, 5.5])

def f(x):
    """Função Objetivo Principal (Custo)"""
    x1, x2, x3, x4, x5, x6, x7 = x
    t1 = 0.7854 * x1 * (x2**2) * (3.3333 * (x3**2) + 14.9334 * x3 - 43.0934)
    t2 = -1.508 * x1 * ((x6**2) + (x7**2))
    t3 = 7.477 * ((x6**3) + (x7**3))
    t4 = 0.7854 * (x4 * (x6**2) + x5 * (x7**2))
    return t1 + t2 + t3 + t4

def calcular_violacao(x):
    """Retorna APENAS a soma das violações (v). Se for 0, é factível."""
    x1, x2, x3, x4, x5, x6, x7 = x
    
    A1 = np.sqrt( (745 * x4 / (x2 * x3))**2 + 16.9e6 )
    B1 = 0.1 * (x6**3)
    A2 = np.sqrt( (745 * x5 / (x2 * x3))**2 + 157.5e6 )
    B2 = 0.1 * (x7**3)
    
    restricoes = [
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
    
    soma_violacoes = sum(max(0, g) for g in restricoes)
    return soma_violacoes

def programacao_evolutiva_sr(mu=400, geracoes=2000, q_torneio=5, Pf_inicial=0.45, Pf_final=0.02):
    populacao = np.random.uniform(lim_inf, lim_sup, (mu, 7))
    
    sigma = (lim_sup - lim_inf) * 0.30
    
    for gen in range(geracoes):
        sigma_atual = sigma * (1.0 - (gen / geracoes))
        if np.all(sigma_atual < 1e-6): sigma_atual = 1e-6
        
        Pf_atual = Pf_inicial - ((Pf_inicial - Pf_final) * (gen / geracoes))
        
        ruido = np.random.normal(0, sigma_atual, populacao.shape)
        filhos = np.clip(populacao + ruido, lim_inf, lim_sup)
        
        pool_total = np.vstack((populacao, filhos))
        
        custos = np.array([f(ind) for ind in pool_total])
        violacoes = np.array([calcular_violacao(ind) for ind in pool_total])
        
        vitorias = np.zeros(2 * mu)
        
        for i in range(2 * mu):
            oponentes = np.random.choice(2 * mu, q_torneio, replace=False)
            
            for op in oponentes:
                c_i, v_i = custos[i], violacoes[i]
                c_op, v_op = custos[op], violacoes[op]
                
                # Regra 1: Ambos Factíveis (v = 0)
                if v_i == 0 and v_op == 0:
                    if c_i < c_op: vitorias[i] += 1
                        
                # Regra 2: Ambos Infactíveis (v > 0)
                elif v_i > 0 and v_op > 0:
                    if v_i < v_op: vitorias[i] += 1
                        
                # Regra 3: Um factível e um infactível
                else:
                    if np.random.rand() < Pf_atual: # Usa o Pf dinâmico
                        if c_i < c_op: vitorias[i] += 1
                    else:
                        if v_i == 0: vitorias[i] += 1
                        
        indices_sobreviventes = np.argsort(vitorias)[::-1][:mu]
        populacao = pool_total[indices_sobreviventes]
        
    # FILTRAGEM FINAL (Com tolerância de Engenharia 1e-4)
    pop_factivel = [ind for ind in populacao if calcular_violacao(ind) <= 1e-4]
    
    if len(pop_factivel) > 0:
        melhor_idx = np.argmin([f(ind) for ind in pop_factivel])
        melhor_x = pop_factivel[melhor_idx]
        eh_factivel = True
    else:
        melhor_idx = np.argmin([calcular_violacao(ind) for ind in populacao])
        melhor_x = populacao[melhor_idx]
        eh_factivel = False

    custo = f(melhor_x)
    violacao = calcular_violacao(melhor_x)
    return melhor_x, eh_factivel, custo, violacao

os.makedirs("Datas/Estatisticas", exist_ok=True)
def executar_experimento(nome_experimento, funcao_algoritmo, num_execucoes=30):
    print(f"Iniciando {num_execucoes} execuções para: {nome_experimento}...")
    
    resultados_custo = []
    detalhes_execucoes = []
    
    for i in range(num_execucoes):
        # IMPORTANTE: Garanta que não há np.random.seed() fixo no seu algoritmo!
        
        # Chama a função do seu algoritmo (Ex: programacao_evolutiva_sr())
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

    # Calculando as estatísticas finais
    estatisticas = {
        "minimo": float(np.min(resultados_custo)),
        "maximo": float(np.max(resultados_custo)),
        "media": float(np.mean(resultados_custo)),
        "desvio_padrao": float(np.std(resultados_custo))
    }

    # Montando o pacote JSON
    dados_finais = {
        "experimento": nome_experimento,
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estatisticas": estatisticas,
        "execucoes": detalhes_execucoes
    }

    # Salvando no arquivo
    caminho_arquivo = f"Datas/Estatisticas/{nome_experimento.replace(' ', '_')}.json"
    with open(caminho_arquivo, 'w') as f:
        json.dump(dados_finais, f, indent=4)
        
    print(f"-> Dados salvos com sucesso em: {caminho_arquivo}\n")



if __name__ == "__main__":
    print("valor tem que ser menor que:  ")
    executar_experimento("Problema 2 - Stochastic Ranking", programacao_evolutiva_sr)