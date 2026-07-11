import numpy as np
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("Datas/Boxplots", exist_ok=True)
os.makedirs("Datas/ViewEstatiticas", exist_ok=True)

def carregar_dados(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        return json.load(f)

def gerar_boxplot(dados_json):
    nome_exp = dados_json["experimento"]
    custos = [execucao["custo"] for execucao in dados_json["execucoes"]]
    
    plt.figure(figsize=(8, 6))
    sns.boxplot(y=custos, color="skyblue")
    plt.title(f"Boxplot de Convergência (30 Execuções)\n{nome_exp}")
    plt.ylabel("Custo f(x)")
    
    caminho_salvar = f"Datas/Boxplots/Boxplot_{nome_exp.replace(' ', '_')}.png"
    plt.savefig(caminho_salvar)
    plt.close()
    print(f"Boxplot gerado: {caminho_salvar}")

def gerar_graficos_barras_separados(lista_dados_json):
    """
    Separa os dados por Problema e gera um gráfico de 4 barras (Min, Med, Max, DP) para cada um.
    """
    problemas_agrupados = {}
    
    for d in lista_dados_json:
        nome_completo = d["experimento"]
        prefixo_problema = nome_completo.split("-")[0].strip()
        
        if prefixo_problema not in problemas_agrupados:
            problemas_agrupados[prefixo_problema] = []
        problemas_agrupados[prefixo_problema].append(d)
        
    for problema, dados in problemas_agrupados.items():
        # Extrai apenas o nome do algoritmo para o eixo X (ex: "Penalidade Estatica")
        nomes_algoritmos = [d["experimento"].split("-")[1].strip() for d in dados]
        
        minimos = [d["estatisticas"]["minimo"] for d in dados]
        medias = [d["estatisticas"]["media"] for d in dados]
        maximos = [d["estatisticas"]["maximo"] for d in dados]
        desvios = [d["estatisticas"]["desvio_padrao"] for d in dados]
        
        x = np.arange(len(nomes_algoritmos))
        largura = 0.2  # Reduzido para caberem 4 barras agrupadas
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plota as 4 estatísticas
        ax.bar(x - 1.5*largura, minimos, largura, label='Mínimo (Melhor)', color='lightgreen')
        ax.bar(x - 0.5*largura, medias, largura, label='Média', color='coral')
        ax.bar(x + 0.5*largura, maximos, largura, label='Máximo (Pior)', color='indianred')
        ax.bar(x + 1.5*largura, desvios, largura, label='Desvio Padrão', color='skyblue')
        
        ax.set_ylabel('Custo f(x)')
        ax.set_title(f'Comparação de Algoritmos - {problema}')
        ax.set_xticks(x)
        ax.set_xticklabels(nomes_algoritmos)
        ax.legend()
        
        # Adiciona uma grade horizontal para facilitar a leitura dos valores
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        caminho_salvar = f"Datas/ViewEstatiticas/Barras_{problema.replace(' ', '_')}.png"
        plt.savefig(caminho_salvar)
        plt.close()
        print(f"Gráfico de Barras gerado: {caminho_salvar}")



if __name__ == "__main__":
    pasta = "Datas/Estatisticas/"
    
    if os.path.exists(pasta):
        arquivos = [f for f in os.listdir(pasta) if f.endswith('.json')]
        todos_os_dados = []
        
        for arq in arquivos:
            caminho_completo = os.path.join(pasta, arq)
            dados = carregar_dados(caminho_completo)
            todos_os_dados.append(dados)
            gerar_boxplot(dados)
            
        if todos_os_dados:
            gerar_graficos_barras_separados(todos_os_dados)
    else:
        print(f"A pasta '{pasta}' não foi encontrada. Rode os algoritmos primeiro.")