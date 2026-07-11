import matplotlib.pyplot as plt
import numpy as np
import os

def gerar_grafico_comparativo(titulo, algoritmos, minimos, maximos, medias, desvios, nome_arquivo):
    """
    Função genérica para plotar o comparativo das meta-heurísticas.
    """
    x = np.arange(len(algoritmos))  # Localização no eixo X para cada algoritmo
    width = 0.25  # Largura das barras

    fig, ax = plt.subplots(figsize=(10, 6))

    # Criando as barras para Mínimo, Média e Máximo
    # Adicionamos yerr (error bar) na Média para representar o Desvio-Padrão
    rects1 = ax.bar(x - width, minimos, width, label='Mínimo', color='#4C72B0', edgecolor='black')
    rects2 = ax.bar(x, medias, width, label='Média (com Desvio-Padrão)', color='#55A868', 
                    yerr=desvios, capsize=5, edgecolor='black', error_kw=dict(lw=1.5, capthick=1.5))
    rects3 = ax.bar(x + width, maximos, width, label='Máximo', color='#C44E52', edgecolor='black')

    # Configurações de texto e eixos
    ax.set_ylabel('Valor da Função Objetivo f(x)', fontsize=12)
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(algoritmos, fontsize=11)
    ax.legend()
    
    # Adiciona uma grade de fundo para facilitar a leitura dos valores
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Adiciona uma linha no zero caso os valores sejam negativos (útil para o TP2)
    ax.axhline(0, color='black', linewidth=0.8)

    plt.tight_layout()
    
    # Salvar na pasta Data
    caminho_arquivo = os.path.join('Data', nome_arquivo)
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"[+] Gráfico gerado com sucesso: '{caminho_arquivo}'")

if __name__ == "__main__":
    # Garante que a pasta Data exista
    os.makedirs('Data', exist_ok=True)

    # ==========================================
    # DADOS DO TP1 (Função 1A)
    # ==========================================
    algoritmos_tp1 = ['Ant Community', 'Busca Tabu', 'Simulate Anilling']
    
    # Atualizado com os novos valores da imagem
    min_tp1 = [0.26687777, 0.04761600, 0.03011900]
    max_tp1 = [4.21036619, 0.69255900, 0.48550200]
    med_tp1 = [1.70220234, 0.33545200, 0.20486300]
    std_tp1 = [1.04581103, 0.16964500, 0.09252600]

    gerar_grafico_comparativo(
        titulo='Comparação de Meta-Heurísticas - TP1 (Função 1A)',
        algoritmos=algoritmos_tp1,
        minimos=min_tp1,
        maximos=max_tp1,
        medias=med_tp1,
        desvios=std_tp1,
        nome_arquivo='comparacao_metaheuristicas_TP1.png'
    )

    # ==========================================
    # DADOS DO TP2 (Função 1 com Restrições)
    # ==========================================
    algoritmos_tp2 = ['Ant Community', 'Rest. Penalidade Estática', 'Rest. Stochastic Ranking']
    
    # Atualizado com os novos valores da imagem
    min_tp2 = [-3.84173156, -3.88793589, -3.34352677]
    max_tp2 = [-0.00013778, -0.00008640, -0.00006892]
    med_tp2 = [-0.50107793, -2.24277731, -0.61388757]
    std_tp2 = [0.96709178, 1.02822357, 0.84161949]

    gerar_grafico_comparativo(
        titulo='Comparação de Meta-Heurísticas - TP2 (Função 1)',
        algoritmos=algoritmos_tp2,
        minimos=min_tp2,
        maximos=max_tp2,
        medias=med_tp2,
        desvios=std_tp2,
        nome_arquivo='comparacao_metaheuristicas_TP2.png'
    )