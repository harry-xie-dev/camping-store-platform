import sqlite3
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "data" / "camping_store.db"


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    print("Tables:")
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table';"
    ).fetchall()

    for table in tables:
        print("-", table["name"])

    print("\nSample products:")
    rows = conn.execute("SELECT * FROM products LIMIT 5;").fetchall()

    for row in rows:
        print(dict(row))

    conn.close()


if __name__ == "__main__":
    main()