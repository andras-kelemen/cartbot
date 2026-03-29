# cartbot – development conventions

Discord bot for managing shared shopping lists (discord.py, Python 3.12+).

## Tooling

- **Linter + formatter:** `ruff` – run: `make lint` / `make format`
- **Tests:** `pytest` – run: `make test`
- **Asyncio mode:** `auto` (pytest-asyncio)
- **Docker:** `make build` to build the image, `make run` to start the container

## Code style

- Python 3.12+, type hints everywhere
- Max line length: 120 characters
- Import order: stdlib → third-party → `cartbot` (handled by ruff/isort)
- Ruff rule set: E, W, F, I, N, UP, B, SIM, RUF

## Project structure

```
cartbot/
  model.py     # data layer (ShoppingList, Item)
  views.py     # Discord UI (embed, select menu, pagination)
  commands.py  # slash command handlers
  bot.py       # bot setup and wiring
  __main__.py  # entry point
tests/        # pytest tests
Dockerfile    # containerization
pyproject.toml
```

## Docker

- The bot runs in Docker; all dependencies are pinned in `pyproject.toml`.
- Never hardcode tokens or secrets – read from environment variables.

## Testing

- Use `pytest-asyncio` for async tests (asyncio_mode = auto).
- Mock all Discord API calls – never call the real API from tests.

## General principles

- Clean code: short functions, clear naming, no unnecessary comments.
- Never commit `.env` files or tokens.
