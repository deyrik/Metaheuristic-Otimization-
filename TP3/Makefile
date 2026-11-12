.PHONY: help setup run compare clean

PYTHON = $(shell if [ -f .venv/bin/python ]; then echo .venv/bin/python; else echo python3; fi)

help:
	@echo "Comandos disponíveis no TP3:"
	@echo "  make setup    - Cria ambiente virtual e instala dependências"
	@echo "  make run      - Executa o Ant System para variáveis contínuas (ACO-R) nos Problemas 1 e 2"
	@echo "  make compare  - Gera os gráficos comparativos entre ACO-R, Busca Tabu, SA e PE"
	@echo "  make clean    - Remove caches Python"

setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

run:
	$(PYTHON) main.py

compare:
	$(PYTHON) comparacao.py

clean:
	rm -rf __pycache__ Ant_System/__pycache__ .pytest_cache
