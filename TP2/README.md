# INFOS

## Algoritmo Implementados:
    
- **Programação Evolutiva com Penalidade Estatica** 

- **Programação Evolutica com Stochastic Ranking**

## Instalação e Gerenciamento

### Criar a pasta venv

Para criar um ambiente virtual, execute o comando:

```bash
python3 -m venv .venv
```

Isso irá criar uma pasta `.venv` no diretório atual com todos os arquivos necessários para o ambiente virtual.

### Ativar o venv

Para ativar o ambiente virtual, execute:

```bash
source .venv/bin/activate
```

Após ativar, você verá `(.venv)` no início da sua linha de comando, indicando que o ambiente virtual está ativo.

### Desativar o venv

Para desativar o ambiente virtual, execute:

```bash
deactivate
```

Após desativar, o prefixo `(.venv)` desaparecerá da sua linha de comando, retornando ao ambiente Python padrão.

## Configuração Automática no VSCode

Para ativar/desativar o `.venv` automaticamente no VSCode:

1. Pressione `Ctrl + ,` para abrir as configurações
2. Na barra de busca, digite: `python terminal activat`
3. Ative a caixa: **Python › Terminal: Activate Environment**

## Dependências Instaladas

Pacotes instalados no ambiente virtual:

```bash
pip install numpy
pip install matplotlib
pip install seaborn

```

Ou em uma única linha:

```bash
pip install numpy matplotlib seaborn 
```

## Estrutura do Projeto

### Descrição dos Arquivos

- **PE_ER_Problem01.py**: Implementação do Problema 1 utilizando **Programação Evolutiva - Estática Restrição (ER)**. Resolve um problema de otimização com 4 variáveis (x1, x2, u1, u2), incluindo restrições de desigualdade e igualdade. Usa penalidades fixas (multas estáticas) para lidar com violações de restrições. Gera estatísticas e resultados em formato JSON.

- **PE_ER_Problem02.py**: Implementação do Problema 2 (Redutor de Velocidade) utilizando **Programação Evolutiva - Estática Restrição (ER)**. Resolve um problema de engenharia com 7 variáveis e 11 restrições de desigualdade. Usa penalidades estáticas para garantir a viabilidade das soluções. Salva resultados das execuções em arquivos JSON.

- **PE_SR_Problem01.py**: Implementação do Problema 1 utilizando **Stochastic Ranking (SR)**. Implementa a mesma formulação do PE_ER_Problem01.py, mas utiliza classificação estocástica para ordenar soluções, oferecendo uma abordagem alternativa ao tratamento de restrições. Gera estatísticas das execuções.

- **PE_SR_Problem02.py**: Implementação do Problema 2 (Redutor de Velocidade) utilizando **Stochastic Ranking (SR)**. Resolve o mesmo problema que PE_ER_Problem02.py, mas emprega o método de classificação estocástica para avaliar soluções viáveis. Armazena resultados em formato JSON.

- **geradorGraficos.py**: Utilitário responsável por gerar visualizações dos resultados das execuções. Carrega dados JSON das estatísticas, cria boxplots para análise de convergência e gera gráficos de barras comparando métricas (mínimo, mediana, máximo e desvio padrão) entre os diferentes algoritmos e problemas.

### Pasta data/

Armazena os resultados das execuções dos algoritmos:

- **Datas/Boxplots**: Pasta contendo os boxplots referentes a cada conjunto (de 30 iterações) dos algoritmos.

- **Datas/Estatisticas**: Pasta contendo Estatiticas especificas de cada iteração e cada algoritmo. Dados em .Json

- **Datas/ViewEstatiticas**: Pasta contendo os graficos das estatisticas para melhor visualização 



## Como Executar

### Executar o programa principal

OBS: lembre-se de executar dentro do ambiente virtual (.venv).

Para executar de maneira completa os algortimos:

```bash
python PE_ER_Problem01.py && \
python PE_ER_Problem02.py && \
python PE_SR_Problem01.py && \
python PE_SR_Problem02.py 
```

### Executar arquivos individuais

Também é possivel testar ou executar um algoritmo específico isoladamente, gerando resultados apenas de tal:

```bash
python PE_ER_Problem01.py
```
```bash
python PE_ER_Problem02.py
```
```bash
python PE_SR_Problem01.py
```
```bash
python PE_SR_Problem02.py 
```









