import sqlite3
from dataclasses import dataclass


@dataclass
class Item:
    id: int
    name: str


class ShoppingList:
    def __init__(self, db_path: str = "cartbot.db") -> None:
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS items "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)"
        )
        self._conn.commit()

    def add(self, item: str) -> None:
        self._conn.execute("INSERT INTO items (name) VALUES (?)", (item.strip(),))
        self._conn.commit()

    def get_all(self) -> list[Item]:
        rows = self._conn.execute("SELECT id, name FROM items ORDER BY id").fetchall()
        return [Item(id=row[0], name=row[1]) for row in rows]

    def remove(self, item_id: int) -> None:
        self._conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()
