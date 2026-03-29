from unittest.mock import AsyncMock, MagicMock

import pytest

from cartbot.model import ShoppingList


@pytest.fixture()
def sl() -> ShoppingList:
    return ShoppingList(db_path=":memory:")


def make_interaction() -> MagicMock:
    interaction = MagicMock()
    interaction.response.send_message = AsyncMock()
    interaction.response.edit_message = AsyncMock()
    return interaction


def capture_commands(sl: ShoppingList) -> dict:
    from cartbot.commands import register

    handlers: dict = {}

    def fake_command(**kwargs):
        def decorator(f):
            handlers[kwargs["name"]] = f
            return f
        return decorator

    tree = MagicMock()
    tree.command = fake_command
    register(tree, sl)
    return handlers


async def test_add_sends_confirmation(sl: ShoppingList) -> None:
    handlers = capture_commands(sl)
    await handlers["add"](make_interaction(), item="tomato")
    assert sl.get_all()[0].name == "tomato"


async def test_add_replies_with_item_name(sl: ShoppingList) -> None:
    handlers = capture_commands(sl)
    interaction = make_interaction()
    await handlers["add"](interaction, item="tomato")
    assert "tomato" in interaction.response.send_message.call_args.args[0]


async def test_list_empty_message(sl: ShoppingList) -> None:
    handlers = capture_commands(sl)
    interaction = make_interaction()
    await handlers["list"](interaction)
    assert "empty" in interaction.response.send_message.call_args.args[0].lower()


async def test_list_sends_embed(sl: ShoppingList) -> None:
    sl.add("milk")
    handlers = capture_commands(sl)
    interaction = make_interaction()
    await handlers["list"](interaction)
    assert interaction.response.send_message.call_args.kwargs.get("embed") is not None


async def test_help_shows_commands(sl: ShoppingList) -> None:
    handlers = capture_commands(sl)
    interaction = make_interaction()
    await handlers["help"](interaction)
    msg = interaction.response.send_message.call_args.args[0]
    assert "/add" in msg
    assert "/list" in msg
