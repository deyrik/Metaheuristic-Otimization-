# venv

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







LINHA 207 (mudar nome do png gerado dependendo dos limites [linhas 19 a 23] )

25% do tp feito 