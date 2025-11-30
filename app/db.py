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

if categories not in db.t:
    categories.create(id=int, name=str, icon=str, color=str, pk="id")

if events not in db.t:
    events.create(
        id=int,
        category_id=int,
        date=str,
        note=str,
        pk="id",
        foreign_keys=[("category_id", "categories")],
    )

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
