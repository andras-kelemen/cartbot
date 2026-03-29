FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir uv && uv sync --no-dev

COPY cartbot/ cartbot/

ENV DB_PATH=/data/cartbot.db

CMD [".venv/bin/python", "-m", "cartbot"]
