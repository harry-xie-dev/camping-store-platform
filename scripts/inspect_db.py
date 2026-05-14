import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "camping_store.db"


def get_table_names(connection: sqlite3.Connection) -> list[str]:
    cursor = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
        """
    )
    return [row[0] for row in cursor.fetchall()]


def get_table_columns(connection: sqlite3.Connection, table_name: str) -> list[str]:
    cursor = connection.execute(f"PRAGMA table_info({table_name});")
    return [row[1] for row in cursor.fetchall()]


def get_sample_rows(
    connection: sqlite3.Connection,
    table_name: str,
    limit: int = 5,
) -> list[dict]:
    connection.row_factory = sqlite3.Row
    cursor = connection.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
    return [dict(row) for row in cursor.fetchall()]


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as connection:
        tables = get_table_names(connection)

        print("Tables:")
        for table in tables:
            print(f"- {table}")

        print("\nDatabase inspection:")
        for table in tables:
            columns = get_table_columns(connection, table)
            rows = get_sample_rows(connection, table)

            print(f"\n=== {table} ===")
            print("Columns:")
            print(", ".join(columns))

            print("\nSample rows:")
            for row in rows:
                print(row)


if __name__ == "__main__":
    main()