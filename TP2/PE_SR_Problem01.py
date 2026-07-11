import numpy as np
import json
import os
import numpy as np
from datetime import datetime


EPSILON = 0.0001

# O vetor x representa [x1, x2, u1, u2]
lim_inf = np.array([0.0, 0.0, 0.0, 0.0])

# LIMITES PELA ÁLGEBRA DAS RESTRIÇÕES
# x1 <= 3.0 (dado no problema)
# x2 <= 4.0 (deduzido de x2 + 2u2 <= 4)
# u1 <= 2.0 (deduzido de x1 + 2u1 <= 4)
# u2 <= 1.0 (dado no problema)
lim_sup = np.array([3.0, 4.0, 2.0, 1.0])

def f(x):
    """Função Objetivo"""
    x1, x2, u1, u2 = x
    return (x1**0.6) + (x2**0.6) - 6*x1 - 4*u1 + 3*u2

def calcular_violacao(x):
    """Calcula a soma de todas as infrações (Desigualdades e Igualdades)"""
    x1, x2, u1, u2 = x
    
    g1 = x1 + 2*u1 - 4.0
    g2 = x2 + 2*u2 - 4.0
    
    h1 = x2 - 3*x1 - 3*u1
    violacao_h1 = abs(h1) - EPSILON
    
    soma_violacoes = max(0, g1) + max(0, g2) + max(0, violacao_h1)
    
    return soma_violacoes


def programacao_evolutiva_sr(mu=300, geracoes=1500, q_torneio=5, Pf_inicial=0.45, Pf_final=0.02):
    populacao = np.random.uniform(lim_inf, lim_sup, (mu, 4))
    
    sigma = (lim_sup - lim_inf) * 0.30
    
    for gen in range(geracoes):
        sigma_atual = sigma * (1.0 - (gen / geracoes))
        if np.all(sigma_atual < 1e-6): sigma_atual = 1e-6
            
        Pf_atual = Pf_inicial - ((Pf_inicial - Pf_final) * (gen / geracoes))
        
        ruido = np.random.normal(0, sigma_atual, populacao.shape)
        filhos = np.clip(populacao + ruido, lim_inf, lim_sup)
        
        # AVALIAÇÃO (Pais + Filhos)
        pool_total = np.vstack((populacao, filhos))
        custos = np.array([f(ind) for ind in pool_total])
        violacoes = np.array([calcular_violacao(ind) for ind in pool_total])
        
        vitorias = np.zeros(2 * mu)
        
        #TORNEIO ESTOCÁSTICO
        for i in range(2 * mu):
            oponentes = np.random.choice(2 * mu, q_torneio, replace=False)
            
            for op in oponentes:
                c_i, v_i = custos[i], violacoes[i]
                c_op, v_op = custos[op], violacoes[op]
                
                # Regra 1: Ambos Factíveis
                if v_i == 0 and v_op == 0:
                    if c_i < c_op: vitorias[i] += 1
                        
                # Regra 2: Ambos Infactíveis
                elif v_i > 0 and v_op > 0:
                    if v_i < v_op: vitorias[i] += 1
                        
                # Regra 3: Misto (Um na lei, outro fora)
                else:
                    if np.random.rand() < Pf_atual:  
                        if c_i < c_op: vitorias[i] += 1
                    else:                      
                        if v_i == 0: vitorias[i] += 1
                        
        # SELEÇÃO DE SOBREVIVENTES
        indices_sobreviventes = np.argsort(vitorias)[::-1][:mu]
        populacao = pool_total[indices_sobreviventes]
        
    # FILTRAGEM FINAL
    pop_factivel = [ind for ind in populacao if calcular_violacao(ind) == 0]
    
    if len(pop_factivel) > 0:
        melhor_idx = np.argmin([f(ind) for ind in pop_factivel])
        melhor_x = pop_factivel[melhor_idx]
        eh_factivel = True
    else:
        melhor_idx = np.argmin([calcular_violacao(ind) for ind in populacao])
        melhor_x = populacao[melhor_idx]
        eh_factivel = False
        
    return melhor_x, eh_factivel, f(melhor_x), calcular_violacao(melhor_x)


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
    executar_experimento("Problema 1 - Penalidade Stochastic Ranking", programacao_evolutiva_sr)


























