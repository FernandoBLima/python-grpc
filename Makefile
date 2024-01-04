# Makefile
SHELL = /bin/bash

.PHONY: help
help:
	@echo "Commands:"
	@echo "venv    : creates a virtual environment."
	@echo "style   : executes style formatting."
	@echo "clean   : cleans all unnecessary files."
	@echo "pre-commit : executes pre-commit tasks."
	@echo "serve-dev   : serves the application in development mode."
	@echo "docker-build: builds the docker image."
	@echo "compose     : runs the docker-compose file."

# Styling
.PHONY: style
style:
	black .
	flake8
	python -m isort .
	pydocstyle .
	isort .

# Environment
.ONESHELL:
venv:
	python -m venv venv
	source venv/bin/activate && \
	python -m pip install --upgrade pip setuptools wheel && \
	python -m pip install -e ".[dev]" && \
	pre-commit install && \
	pre-commit autoupdate

# Cleaning
.PHONY: clean
clean: style
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	find . | grep -E ".trash" | xargs rm -rf
	rm -f .coverage
	rm -rf htmlcov

# Run pre-commit tasks
.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

# Serve non-production
.PHONY: serve-client
serve-dev:
	python client/app.py

.PHONY: serve-server
serve-dev:
	python server/app.py

# Docker
.PHONY: docker-build
docker-build:
	docker build -t grpc-python .

# Docker Compose
.PHONY: compose
compose:
	docker-compose up --build