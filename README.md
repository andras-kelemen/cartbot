# cartbot

[![CI](https://github.com/andras-kelemen/cartbot/actions/workflows/ci.yml/badge.svg)](https://github.com/andras-kelemen/cartbot/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/andras-kelemen/cartbot/branch/main/graph/badge.svg)](https://codecov.io/gh/andras-kelemen/cartbot)
![Python](https://img.shields.io/badge/python-3.12+-blue)

Discord bot for managing shared shopping lists.

## Commands

| Command | Description |
|---|---|
| `/add <item(s)>` | Add one or more comma-separated items (e.g. `/add milk, bread, eggs`) |
| `/list` | Show all items as toggle buttons; tap to check off, next `/list` removes them |
| `/help` | Show available commands |

## How it works

`/list` displays an embed with each item as a clickable button. Tapping a button marks it as done (turns green). The next time `/list` is called, checked items are removed and a fresh list is shown. When the list is empty, the embed turns green. Lists with more than 20 items are paginated.

## Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/) or Docker
- A Discord bot token ([Discord Developer Portal](https://discord.com/developers/applications))

### Discord bot configuration

1. Create a new application in the Developer Portal
2. Under **Bot**, enable **Message Content Intent**
3. Under **OAuth2 → URL Generator**, select scope `bot` and invite the bot to your server

### Environment variables

| Variable | Description | Default |
|---|---|---|
| `DISCORD_TOKEN` | Discord bot token | required |
| `DB_PATH` | Path to the SQLite database file | `cartbot.db` |
| `GUILD_ID` | Sync slash commands to a specific server instantly (dev only) | — |

Create a `.env` file:

```
DISCORD_TOKEN=your_token_here
```

## Running

### With uv

```bash
uv run --env-file .env python -m cartbot
```

### With Docker

```bash
make build
make run
```

The SQLite database is stored in a Docker volume (`cartbot_data`) so data persists across restarts.

## Development

```bash
make test      # run tests
make lint      # ruff check
make format    # ruff format
```

### Project structure

```
cartbot/
  model.py     — data layer (ShoppingList, Item)
  views.py     — Discord UI (embed, buttons, pagination)
  commands.py  — slash command handlers
  bot.py       — bot setup and wiring
  __main__.py  — entry point
tests/
  test_list.py      — ShoppingList unit tests
  test_views.py     — embed and view tests
  test_commands.py  — slash command handler tests
```
