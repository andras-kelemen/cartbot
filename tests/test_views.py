import discord
import pytest

from cartbot.model import ShoppingList
from cartbot.views import build_embed, build_list_message


@pytest.fixture()
def sl() -> ShoppingList:
    return ShoppingList(db_path=":memory:")


def test_embed_contains_items(sl: ShoppingList) -> None:
    sl.add("milk")
    embed, _ = build_list_message(sl, page=0)
    assert "milk" in embed.description


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
    assert "Page" not in embed.footer.text  # only 1 page, no footer
