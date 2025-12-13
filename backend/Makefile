.PHONY: help install sync run dev test test-verbose clean lint format

help:
	@echo "Lumberjack Legends Backend - Available Commands:"
	@echo ""
	@echo "  make install       - Install all dependencies"
	@echo "  make sync          - Sync dependencies from lockfile"
	@echo "  make run           - Run the server"
	@echo "  make dev           - Run the server with auto-reload (development)"
	@echo "  make test          - Run all tests"
	@echo "  make test-verbose  - Run tests with verbose output"
	@echo "  make clean         - Remove cache and build artifacts"
	@echo ""

install:
	uv sync

sync:
	uv sync

run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest

test-verbose:
	uv run pytest -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/
