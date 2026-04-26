import sqlite3
from dataclasses import dataclass


@dataclass
class Item:
    id: int
    name: str
    checked: bool = False
    emoji: str | None = None


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
        for ddl in [
            "ALTER TABLE items ADD COLUMN checked INTEGER NOT NULL DEFAULT 0",
            "ALTER TABLE items ADD COLUMN emoji TEXT",
        ]:
            try:
                self._conn.execute(ddl)
                self._conn.commit()
            except sqlite3.OperationalError:
                pass

    def add(self, item: str, emoji: str | None = None) -> None:
        self._conn.execute("INSERT INTO items (name, emoji) VALUES (?, ?)", (item.strip(), emoji))
        self._conn.commit()

    def get_all(self) -> list[Item]:
        rows = self._conn.execute("SELECT id, name, checked, emoji FROM items ORDER BY id").fetchall()
        return [Item(id=row[0], name=row[1], checked=bool(row[2]), emoji=row[3]) for row in rows]

    def get_emoji_for_name(self, name: str) -> str | None:
        row = self._conn.execute(
            "SELECT emoji FROM items WHERE name = ? AND emoji IS NOT NULL LIMIT 1",
            (name.strip(),),
        ).fetchone()
        return row[0] if row else None

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
