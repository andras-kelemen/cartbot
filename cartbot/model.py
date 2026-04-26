import sqlite3
from dataclasses import dataclass, field


@dataclass
class Item:
    id: int
    name: str
    checked: bool = field(default=False)


class ShoppingList:
    def __init__(self, db_path: str = "cartbot.db") -> None:
        self._conn = sqlite3.connect(db_path)
        self._migrate()

    def _migrate(self) -> None:
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS items "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, checked INTEGER NOT NULL DEFAULT 0)"
        )
        self._conn.commit()
        try:
            self._conn.execute("ALTER TABLE items ADD COLUMN checked INTEGER NOT NULL DEFAULT 0")
            self._conn.commit()
        except sqlite3.OperationalError:
            pass  # column already exists

    def add(self, item: str) -> None:
        self._conn.execute("INSERT INTO items (name) VALUES (?)", (item.strip(),))
        self._conn.commit()

    def get_all(self) -> list[Item]:
        rows = self._conn.execute("SELECT id, name, checked FROM items ORDER BY id").fetchall()
        return [Item(id=row[0], name=row[1], checked=bool(row[2])) for row in rows]

    def check(self, item_id: int) -> None:
        self._conn.execute("UPDATE items SET checked = 1 WHERE id = ?", (item_id,))
        self._conn.commit()

    def toggle_checked(self, item_id: int) -> None:
        self._conn.execute("UPDATE items SET checked = 1 - checked WHERE id = ?", (item_id,))
        self._conn.commit()

    def remove(self, item_id: int) -> None:
        self._conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        self._conn.commit()

    def remove_checked(self) -> None:
        self._conn.execute("DELETE FROM items WHERE checked = 1")
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()
