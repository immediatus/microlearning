# MicroLearning Platform Makefile
.PHONY: help setup install dev test lint format clean docker build deploy

# Default target
help:
	@echo "MicroLearning Platform Development Commands"
	@echo "==========================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  setup          - Set up development environment (venv + dependencies)"
	@echo "  install        - Install Python dependencies"
	@echo "  install-dev    - Install development dependencies"
	@echo ""
	@echo "Development Commands:"
	@echo "  dev            - Start development server"
	@echo "  dev-mobile     - Start mobile development with Expo"
	@echo "  dev-web        - Start creator dashboard"
	@echo "  dev-worker     - Start Celery worker"
	@echo ""
	@echo "Code Quality Commands:"
	@echo "  test           - Run all tests"
	@echo "  test-unit      - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-coverage  - Run tests with coverage report"
	@echo "  lint           - Run all linters"
	@echo "  format         - Format code (black + isort)"
	@echo "  type-check     - Run type checking with mypy"
	@echo ""
	@echo "Database Commands:"
	@echo "  db-migrate     - Run database migrations"
	@echo "  db-reset       - Reset database (drop and recreate)"
	@echo "  db-seed        - Seed database with sample data"
	@echo ""
	@echo "Docker Commands:"
	@echo "  docker-build   - Build Docker images"
	@echo "  docker-up      - Start all services with Docker Compose"
	@echo "  docker-down    - Stop all services"
	@echo "  docker-logs    - View service logs"
	@echo ""
	@echo "Deployment Commands:"
	@echo "  build          - Build production artifacts"
	@echo "  deploy-staging - Deploy to staging environment"
	@echo "  deploy-prod    - Deploy to production environment"
	@echo ""
	@echo "Utility Commands:"
	@echo "  clean          - Clean temporary files and caches"
	@echo "  security-check - Run security analysis"

# Python Virtual Environment
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Setup development environment
setup: $(VENV)/bin/activate install-dev
	@echo "✅ Development environment set up successfully!"

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip setuptools wheel

# Install dependencies
install: $(VENV)/bin/activate
	$(PIP) install -r requirements.txt

install-dev: install
	$(PIP) install -r requirements-dev.txt
	$(VENV)/bin/pre-commit install

# Development servers
dev:
	$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-mobile:
	cd mobile && npm run start

dev-web:
	cd creator-dashboard && npm run dev

dev-worker:
	$(PYTHON) -m celery -A app.celery worker --loglevel=info

# Testing
test:
	$(PYTHON) -m pytest tests/ -v

test-unit:
	$(PYTHON) -m pytest tests/unit/ -v

test-integration:
	$(PYTHON) -m pytest tests/integration/ -v

test-coverage:
	$(PYTHON) -m pytest --cov=app --cov-report=html --cov-report=term tests/

# Code quality
lint:
	$(PYTHON) -m ruff check app/ tests/
	$(PYTHON) -m black --check app/ tests/
	$(PYTHON) -m isort --check-only app/ tests/

format:
	$(PYTHON) -m black app/ tests/
	$(PYTHON) -m isort app/ tests/
	$(PYTHON) -m ruff check app/ tests/ --fix

type-check:
	$(PYTHON) -m mypy app/

security-check:
	$(PYTHON) -m bandit -r app/ -f json -o bandit-report.json

# Database operations
db-migrate:
	$(PYTHON) -m alembic upgrade head

db-reset:
	$(PYTHON) -c "import asyncio; from app.core.database import drop_tables, create_tables; asyncio.run(drop_tables()); asyncio.run(create_tables())"

db-seed:
	$(PYTHON) scripts/seed_database.py

# Docker operations
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-clean:
	docker-compose down -v
	docker system prune -f

# Build and deployment
build:
	# Build API
	docker build -t microlearning/api:latest -f Dockerfile.api .
	
	# Build Creator Dashboard
	cd creator-dashboard && npm run build
	
	# Build Mobile App
	cd mobile && npx expo build:web

deploy-staging:
	@echo "Deploying to staging..."
	# Add staging deployment commands here

deploy-prod:
	@echo "Deploying to production..."
	# Add production deployment commands here

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name ".expo" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +

# Development workflow shortcuts
start: docker-up
	@echo "🚀 Starting development environment..."
	@echo "📱 Mobile app: http://localhost:19006"
	@echo "🌐 Creator dashboard: http://localhost:3000"
	@echo "🔧 API docs: http://localhost:8000/docs"
	@echo "🗄️  PgAdmin: http://localhost:5050"

stop: docker-down
	@echo "🛑 Stopped development environment"

restart: stop start
	@echo "🔄 Restarted development environment"

# Quick quality check
check: lint type-check test
	@echo "✅ All quality checks passed!"

# Full reset (use with caution)
reset: clean docker-clean
	rm -rf $(VENV)
	@echo "🧹 Environment reset complete. Run 'make setup' to reinitialize."