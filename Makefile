.PHONY: help install dev-install test test-cov lint format run clean

help:
	@echo "PROYECTO COLMENA - Available commands:"
	@echo ""
	@echo "  make install       Install production dependencies"
	@echo "  make dev-install   Install development dependencies"
	@echo "  make test          Run tests"
	@echo "  make test-cov      Run tests with coverage report"
	@echo "  make lint          Run linting (flake8, mypy)"
	@echo "  make format        Format code (black, isort)"
	@echo "  make run           Run investigation CLI"
	@echo "  make clean         Clean generated files"

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt

test:
	pytest

test-cov:
	pytest --cov=agents --cov=shared --cov=core --cov-report=html --cov-report=term
	@echo "\n📊 Coverage report generated: htmlcov/index.html"

lint:
	flake8 agents shared core integrations scripts tests
	mypy agents shared core --ignore-missing-imports

format:
	black agents shared core integrations scripts tests

run:
	python scripts/run_investigation.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache .coverage htmlcov build dist *.egg-info
	rm -f colmena_events.db colmena.db colmena.log
	@echo "✨ Clean complete"
