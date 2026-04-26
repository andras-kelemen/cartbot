from unittest.mock import AsyncMock, MagicMock

import discord
import pytest

from cartbot.model import Item, ShoppingList
from cartbot.views import ItemButton, NavButton, build_embed, build_list_message


@pytest.fixture()
def sl():
    shopping_list = ShoppingList(db_path=":memory:")
    yield shopping_list
    shopping_list.close()


def test_view_contains_item_buttons(sl: ShoppingList) -> None:
    sl.add("milk")
    _, view = build_list_message(sl, page=0)
    labels = [child.label for child in view.children if isinstance(child, ItemButton)]
    assert "milk" in labels


def test_embed_shows_remaining_count(sl: ShoppingList) -> None:
    sl.add("eggs")
    sl.add("butter")
    embed = build_embed(sl.get_all(), page=0, total_pages=1)
    assert "2" in embed.footer.text


def test_embed_orange_when_items_present(sl: ShoppingList) -> None:
    sl.add("milk")
    embed = build_embed(sl.get_all(), page=0, total_pages=1)
    assert embed.color == discord.Color.orange()


def test_embed_green_when_list_empty() -> None:
    embed = build_embed([], page=0, total_pages=1)
    assert embed.color == discord.Color.green()


def test_embed_shows_all_done_when_empty() -> None:
    embed = build_embed([], page=0, total_pages=1)
    assert "All done" in embed.description


def test_pagination_footer_shown_on_multiple_pages(sl: ShoppingList) -> None:
    embed = build_embed([], page=1, total_pages=3)
    assert "Page 2/3" in embed.footer.text


def test_pagination_footer_hidden_on_single_page(sl: ShoppingList) -> None:
    embed = build_embed([], page=0, total_pages=1)
    assert "Page" not in embed.footer.text


def test_page_clamped_to_last(sl: ShoppingList) -> None:
    sl.add("milk")
    embed, _ = build_list_message(sl, page=99)
    assert "Page" not in embed.footer.text


def test_item_button_unchecked_style(sl: ShoppingList) -> None:
    item = Item(id=1, name="milk", checked=False)
    btn = ItemButton(item, page=0, shopping_list=sl, row=0)
    assert btn.style == discord.ButtonStyle.secondary
    assert str(btn.emoji) == "🛒"


def test_item_button_checked_style(sl: ShoppingList) -> None:
    item = Item(id=1, name="milk", checked=True)
    btn = ItemButton(item, page=0, shopping_list=sl, row=0)
    assert btn.style == discord.ButtonStyle.success
    assert str(btn.emoji) == "✅"


def test_embed_remaining_count_excludes_checked() -> None:
    items = [Item(id=1, name="milk", checked=False), Item(id=2, name="bread", checked=True)]
    embed = build_embed(items, page=0, total_pages=1)
    assert "1 item(s) remaining" in embed.footer.text


def test_item_buttons_row_assignment(sl: ShoppingList) -> None:
    for i in range(6):
        sl.add(f"item{i}")
    _, view = build_list_message(sl, page=0)
    buttons = [child for child in view.children if isinstance(child, ItemButton)]
    assert buttons[0].row == 0
    assert buttons[4].row == 0
    assert buttons[5].row == 1


async def test_item_button_callback_toggles_item(sl: ShoppingList) -> None:
    sl.add("milk")
    item = sl.get_all()[0]
    btn = ItemButton(item, page=0, shopping_list=sl, row=0)
    interaction = MagicMock()
    interaction.response.edit_message = AsyncMock()
    await btn.callback(interaction)
    assert sl.get_all()[0].checked is True
    interaction.response.edit_message.assert_called_once()


def test_nav_buttons_added_on_multiple_pages(sl: ShoppingList) -> None:
    for i in range(21):
        sl.add(f"item{i}")
    _, view = build_list_message(sl, page=0)
    nav_labels = [c.label for c in view.children if isinstance(c, NavButton)]
    assert "Next ▶" in nav_labels
    assert "◀ Prev" not in nav_labels


def test_prev_nav_button_added_on_later_pages(sl: ShoppingList) -> None:
    for i in range(21):
        sl.add(f"item{i}")
    _, view = build_list_message(sl, page=1)
    nav_labels = [c.label for c in view.children if isinstance(c, NavButton)]
    assert "◀ Prev" in nav_labels
    assert "Next ▶" not in nav_labels


async def test_nav_button_callback_navigates(sl: ShoppingList) -> None:
    for i in range(21):
        sl.add(f"item{i}")
    _, view = build_list_message(sl, page=0)
    next_btn = next(c for c in view.children if isinstance(c, NavButton))
    interaction = MagicMock()
    interaction.response.edit_message = AsyncMock()
    await next_btn.callback(interaction)
    interaction.response.edit_message.assert_called_once()
