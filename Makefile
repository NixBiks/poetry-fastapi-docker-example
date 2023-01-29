install:
	poetry install

test:
	poetry run pytest tests
	poetry run pyright

format:
	poetry run black .
	poetry run isort .

lint:
	poetry run black --check .
	poetry run isort --check-only .
	poetry run ruff .

pre-commit:
	poetry run pytest tests --cov
	poetry run pyright
	poetry run black --check .
	poetry run isort --check-only .
	poetry run ruff .