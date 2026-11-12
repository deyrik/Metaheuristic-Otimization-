.PHONY: help setup run run-p1 run-p2 plots clean

PYTHON = $(shell if [ -f .venv/bin/python ]; then echo .venv/bin/python; else echo python3; fi)

help:
	@echo "Comandos disponíveis no TP2:"
	@echo "  make setup   - Cria ambiente virtual e instala dependências"
	@echo "  make run     - Executa todos os problemas (ER e SR para Problemas 1 e 2)"
	@echo "  make run-p1  - Executa apenas o Problema 1 (Penalidade Estática e Stochastic Ranking)"
	@echo "  make run-p2  - Executa apenas o Problema 2 (Redutor de Velocidade)"
	@echo "  make plots   - Gera os gráficos comparativos e boxplots a partir dos JSONs"
	@echo "  make clean   - Remove caches Python"

setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

run:
	$(PYTHON) PE_ER_Problem01.py
	$(PYTHON) PE_ER_Problem02.py
	$(PYTHON) PE_SR_Problem01.py
	$(PYTHON) PE_SR_Problem02.py

run-p1:
	$(PYTHON) PE_ER_Problem01.py
	$(PYTHON) PE_SR_Problem01.py

run-p2:
	$(PYTHON) PE_ER_Problem02.py
	$(PYTHON) PE_SR_Problem02.py

plots:
	$(PYTHON) geradorGraficos.py

clean:
	rm -rf __pycache__ .pytest_cache
