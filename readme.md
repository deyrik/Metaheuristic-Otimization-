# INFOS

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
pip install scipy
pip install pandas

```

Ou em uma única linha:

```bash
pip install numpy matplotlib scipy pandas
```

## Estrutura do Projeto

### Descrição dos Arquivos

- **main.py**: Arquivo principal que coordena a execução dos algoritmos de otimização. Responsável por chamar os diferentes métodos de busca e gerenciar o fluxo geral do programa.

- **buscaTabu.py**: Implementação do algoritmo **Tabu Search (Busca Tabu)** - uma metaheurística que utiliza memória para evitar revisitar soluções já exploradas, impedindo ciclos e melhorando a exploração do espaço de busca.

- **buscaTabu2.py**: Implementação do **Tabu Search** adaptada para resolver um tipo diferente de função ou problema.

- **SimulateAnilling.py**: Implementação do algoritmo **Simulated Annealing (Recozimento Simulado)** - metaheurística inspirada no processo de resfriamento de metais, que permite aceitar soluções piores com probabilidade decrescente para escapar de ótimos locais.

- **SimulateAnilling2.py**: Implementação do **Simulated Annealing** adaptada para resolver um tipo diferente de função ou problema.

- **backup.py**: Arquivo de backup ou utilitários para salvar/restaurar estados ou resultados dos algoritmos.

### Pasta data/

Armazena os resultados das execuções dos algoritmos:

- **resultados.json**: Arquivo JSON contendo os resultados consolidados de todas as execuções. Este é o único arquivo versionado do diretório `data/`.

- **BT_Func1_LimiteA/** e **BT_Func1_LimiteB/**: Resultados do Tabu Search aplicado à Função 1 com limites A e B.

- **BT_Func2_LimiteA/** e **BT_Func2_LimiteB/**: Resultados do Tabu Search aplicado à Função 2 com limites A e B.

- **SA_Func1_LimiteA/** e **SA_Func1_LimiteB/**: Resultados do Simulated Annealing aplicado à Função 1 com limites A e B.

- **SA_Func2_LimiteA/** e **SA_Func2_LimiteB/**: Resultados do Simulated Annealing aplicado à Função 2 com limites A e B.

Note: As subpastas não são versionadas no Git (conforme configurado no `.gitignore`), pois contêm dados de execução local.







