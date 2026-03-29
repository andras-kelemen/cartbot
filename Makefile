.PHONY: build run test lint format

build:
	docker build -t cartbot .

run:
	docker run -d --name cartbot --env-file .env -v cartbot_data:/data cartbot

test:
	uv run pytest -v

lint:
	uv run ruff check .

format:
	uv run ruff format .
