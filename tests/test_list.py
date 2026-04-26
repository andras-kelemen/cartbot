import sqlite3
import tempfile

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


def test_check_marks_item_checked(sl: ShoppingList) -> None:
    sl.add("milk")
    sl.add("bread")
    item_id = sl.get_all()[0].id
    sl.check(item_id)
    items = sl.get_all()
    assert items[0].checked is True
    assert items[1].checked is False


def test_check_does_not_delete_item(sl: ShoppingList) -> None:
    sl.add("milk")
    item_id = sl.get_all()[0].id
    sl.check(item_id)
    assert len(sl.get_all()) == 1


def test_remove_checked_deletes_only_checked(sl: ShoppingList) -> None:
    sl.add("milk")
    sl.add("bread")
    sl.add("eggs")
    sl.check(sl.get_all()[1].id)
    sl.remove_checked()
    assert [item.name for item in sl.get_all()] == ["milk", "eggs"]


def test_remove_checked_on_empty_list_is_safe(sl: ShoppingList) -> None:
    sl.remove_checked()
    assert sl.get_all() == []


def test_toggle_checked_unchecked_to_checked(sl: ShoppingList) -> None:
    sl.add("milk")
    item_id = sl.get_all()[0].id
    sl.toggle_checked(item_id)
    assert sl.get_all()[0].checked is True


def test_toggle_checked_checked_to_unchecked(sl: ShoppingList) -> None:
    sl.add("milk")
    item_id = sl.get_all()[0].id
    sl.check(item_id)
    sl.toggle_checked(item_id)
    assert sl.get_all()[0].checked is False


def test_migration_existing_db() -> None:
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)")
    conn.execute("INSERT INTO items (name) VALUES ('milk')")
    conn.commit()
    conn.close()

    sl = ShoppingList(db_path=db_path)
    items = sl.get_all()
    assert len(items) == 1
    assert items[0].name == "milk"
    assert items[0].checked is False
