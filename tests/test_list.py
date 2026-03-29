import pytest

from cartbot.model import ShoppingList


@pytest.fixture()
def sl() -> ShoppingList:
    return ShoppingList(db_path=":memory:")


def test_add_and_get(sl: ShoppingList) -> None:
    sl.add("milk")
    sl.add("bread")
    assert [item.name for item in sl.get_all()] == ["milk", "bread"]


def test_empty_list(sl: ShoppingList) -> None:
    assert sl.get_all() == []


def test_add_strips_whitespace(sl: ShoppingList) -> None:
    sl.add("  eggs  ")
    assert sl.get_all()[0].name == "eggs"


def test_get_all_preserves_insertion_order(sl: ShoppingList) -> None:
    for item in ["apple", "banana", "cherry"]:
        sl.add(item)
    assert [item.name for item in sl.get_all()] == ["apple", "banana", "cherry"]


def test_remove_deletes_item(sl: ShoppingList) -> None:
    sl.add("milk")
    sl.add("bread")
    sl.remove(sl.get_all()[0].id)
    assert [item.name for item in sl.get_all()] == ["bread"]


def test_remove_only_target(sl: ShoppingList) -> None:
    sl.add("milk")
    sl.add("bread")
    sl.add("eggs")
    sl.remove(sl.get_all()[1].id)
    assert [item.name for item in sl.get_all()] == ["milk", "eggs"]
