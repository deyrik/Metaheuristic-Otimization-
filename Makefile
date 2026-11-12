.PHONY: help setup tp1 tp2 tp3 clean

help:
	@echo "=========================================================="
	@echo " Metaheuristic Optimization - Central de Execução"
	@echo "=========================================================="
	@echo "Comandos gerais:"
	@echo "  make setup - Prepara ambientes e instala dependências de todos os TPs"
	@echo "  make tp1   - Executa os experimentos do Trabalho Prático 1"
	@echo "  make tp2   - Executa os experimentos do Trabalho Prático 2"
	@echo "  make tp3   - Executa os experimentos do Trabalho Prático 3"
	@echo "  make clean - Limpa diretórios de cache e arquivos temporários"
	@echo ""
	@echo "Dica: Você também pode entrar diretamente na pasta de cada TP"
	@echo "e utilizar 'make help' para comandos específicos de cada trabalho."

setup:
	@echo "Configurando TP1..."
	@cd TP1 && $(MAKE) setup
	@echo "Configurando TP2..."
	@cd TP2 && $(MAKE) setup
	@echo "Configurando TP3..."
	@cd TP3 && $(MAKE) setup
	@echo "Todos os ambientes configurados com sucesso!"

tp1:
	@cd TP1 && $(MAKE) run

tp2:
	@cd TP2 && $(MAKE) run

tp3:
	@cd TP3 && $(MAKE) run

clean:
	@cd TP1 && $(MAKE) clean 2>/dev/null || true
	@cd TP2 && $(MAKE) clean 2>/dev/null || true
	@cd TP3 && $(MAKE) clean 2>/dev/null || true
	@rm -rf __pycache__
	@echo "Limpeza concluída!"
