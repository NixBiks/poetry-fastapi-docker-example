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

dev:
	poetry run uvicorn playground.main:app --reload

start:
	poetry run gunicorn playground.main:app -w 4 -k uvicorn.workers.UvicornWorker

build-image:
	docker build -t playground --file image/Dockerfile .

pre-commit:
	poetry run pytest tests --cov
	poetry run pyright
	poetry run black --check .
	poetry run isort --check-only .
	poetry run ruff .