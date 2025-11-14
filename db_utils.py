from pathlib import Path
import sqlite3

DB = Path("db/market.db")

def get_conn(db_path: str | None = None):
    p = DB if db_path is None else Path(db_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db(schema_path: str = "sql/schema.sql", db_path: str | None = None):
    conn = get_conn(db_path)
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
