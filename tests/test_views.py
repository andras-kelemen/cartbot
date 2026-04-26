import discord
import pytest

from cartbot.model import Item, ShoppingList
from cartbot.views import ItemButton, build_embed, build_list_message


@pytest.fixture()
def sl() -> ShoppingList:
    return ShoppingList(db_path=":memory:")


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


def test_item_button_unchecked_style() -> None:
    item = Item(id=1, name="milk", checked=False)
    sl = ShoppingList(db_path=":memory:")
    btn = ItemButton(item, page=0, shopping_list=sl, row=0)
    assert btn.style == discord.ButtonStyle.secondary
    assert str(btn.emoji) == "🛒"


def test_item_button_checked_style() -> None:
    item = Item(id=1, name="milk", checked=True)
    sl = ShoppingList(db_path=":memory:")
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
