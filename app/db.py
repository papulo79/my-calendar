import sqlite3
from pathlib import Path

from fasthtml.common import database

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "calendar.db"
LEGACY_DB_PATH = BASE_DIR / "calendar.db"

# Preserve datos antiguos si el archivo previo existe en la raiz
if LEGACY_DB_PATH.exists() and not DB_PATH.exists():
    DB_PATH.write_bytes(LEGACY_DB_PATH.read_bytes())

db = database(str(DB_PATH))
categories = db.t.categories
events = db.t.events

# Ensure schema (transform=True applies column additions on existing tables)
categories.create(id=int, name=str, icon=str, color=str, owner=str, pk="id", transform=True)
events.create(
    id=int,
    category_id=int,
    date=str,
    note=str,
    owner=str,
    pk="id",
    foreign_keys=[("category_id", "categories")],
    transform=True,
)

# Backfill owner for legacy rows so they remain visible for the default user
def backfill_owner(default_owner: str = "Pablo"):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE categories SET owner=? WHERE owner IS NULL OR owner=''", (default_owner,))
        conn.execute("UPDATE events SET owner=? WHERE owner IS NULL OR owner=''", (default_owner,))
        conn.commit()

backfill_owner()

Category = categories.dataclass()
Event = events.dataclass()

__all__ = [
    "db",
    "categories",
    "events",
    "Category",
    "Event",
    "DATA_DIR",
    "DB_PATH",
]
