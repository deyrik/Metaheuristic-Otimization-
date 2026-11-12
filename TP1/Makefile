.PHONY: help setup run clean

PYTHON = $(shell if [ -f .venv/bin/python ]; then echo .venv/bin/python; else echo python3; fi)

help:
	@echo "Comandos disponíveis no TP1:"
	@echo "  make setup   - Cria ambiente virtual e instala dependências"
	@echo "  make run     - Executa o experimento completo (30 execuções por algoritmo/função)"
	@echo "  make clean   - Remove caches Python"

setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

run:
	$(PYTHON) src/main.py

clean:
	rm -rf __pycache__ src/__pycache__ .pytest_cache
