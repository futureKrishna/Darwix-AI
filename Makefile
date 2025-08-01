.PHONY: help install install-dev test test-watch lint format type-check security clean docker-build docker-run docker-test ci-local dev-up

# Default target
help:
	@echo "Available commands:"
	@echo "  install       Install production dependencies"
	@echo "  install-dev   Install development dependencies"
	@echo "  dev-up        Complete development setup and start server"
	@echo "  test          Run tests with coverage"
	@echo "  test-watch    Run tests in watch mode"
	@echo "  lint          Run all linting checks"
	@echo "  format        Format code with black and isort"
	@echo "  type-check    Run mypy type checking"
	@echo "  security      Run security checks"
	@echo "  clean         Clean cache and build files"
	@echo "  docker-build  Build Docker image"
	@echo "  docker-run    Run Docker container"
	@echo "  docker-test   Test Docker image"
	@echo "  ci-local      Run full CI pipeline locally"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

# Complete development setup
dev-up: install
	@echo "🚀 Setting up development environment..."
	alembic upgrade head || echo "Database already up to date"
	@echo "✅ Database initialized"
	@echo "🌐 Starting development server..."
	python fast_run.py

# Testing
test:
	pytest test_final_clean.py --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=90 -v

test-watch:
	pytest-watch -- test_final_clean.py --cov=app --cov-report=term-missing -v

# Code quality
lint:
	flake8 app/
	pylint app/ --disable=C0103,C0111,R0903,W0613 --max-line-length=88
	bandit -r app/

format:
	black app/
	isort app/

type-check:
	mypy app/ --ignore-missing-imports --disallow-untyped-defs --strict-optional

security:
	bandit -r app/ -f json -o bandit-report.json
	safety check

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -f coverage.xml
	rm -f bandit-report.json
	rm -f safety-report.json

# Docker
docker-build:
	docker build -t darwix-ai:latest .

docker-run:
	docker run -d --name darwix-ai -p 8000:8000 darwix-ai:latest

docker-test:
	docker build -t darwix-ai:test .
	docker run --rm -d --name test-container -p 8001:8000 darwix-ai:test
	sleep 10
	curl -f http://localhost:8001/health || (docker stop test-container && exit 1)
	docker stop test-container

# Local CI simulation
ci-local: clean format lint type-check security test
	@echo "✅ All CI checks passed locally!"

# Database operations
db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-reset:
	alembic downgrade base
	alembic upgrade head

# Development server
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
prod:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
