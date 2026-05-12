from pathlib import Path
import csv
import sqlite3


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "camping_store.db"


def read_csv(filename: str) -> list[dict[str, str]]:
    path = DATA_DIR / filename
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def to_bool(value: str) -> int:
    return 1 if value.strip().lower() == "true" else 0


def create_tables(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON;")

    conn.executescript(
        """
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS marketing_campaigns;
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS products;

        CREATE TABLE products (
            product_id TEXT PRIMARY KEY,
            sku TEXT NOT NULL UNIQUE,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            brand TEXT NOT NULL,
            unit_price REAL NOT NULL,
            cost REAL NOT NULL,
            stock_quantity INTEGER NOT NULL,
            supplier TEXT NOT NULL,
            active INTEGER NOT NULL
        );

        CREATE TABLE customers (
            customer_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            signup_date TEXT NOT NULL,
            acquisition_channel TEXT NOT NULL
        );

        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            subtotal REAL NOT NULL,
            shipping_fee REAL NOT NULL,
            tax REAL NOT NULL,
            total REAL NOT NULL,
            payment_method TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE order_items (
            order_item_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            line_total REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );

        CREATE TABLE marketing_campaigns (
            campaign_id TEXT PRIMARY KEY,
            campaign_name TEXT NOT NULL,
            channel TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            budget REAL NOT NULL,
            target_category TEXT NOT NULL,
            clicks INTEGER NOT NULL,
            conversions INTEGER NOT NULL,
            revenue_attributed REAL NOT NULL
        );
        """
    )


def load_products(conn: sqlite3.Connection) -> None:
    rows = read_csv("sample_products.csv")
    cleaned_rows = [
        (
            row["product_id"],
            row["sku"],
            row["product_name"],
            row["category"],
            row["brand"],
            float(row["unit_price"]),
            float(row["cost"]),
            int(row["stock_quantity"]),
            row["supplier"],
            to_bool(row["active"]),
        )
        for row in rows
    ]

    conn.executemany(
        """
        INSERT INTO products (
            product_id, sku, product_name, category, brand,
            unit_price, cost, stock_quantity, supplier, active
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        cleaned_rows,
    )


def load_customers(conn: sqlite3.Connection) -> None:
    rows = read_csv("sample_customers.csv")
    cleaned_rows = [
        (
            row["customer_id"],
            row["first_name"],
            row["last_name"],
            row["email"],
            row["city"],
            row["state"],
            row["signup_date"],
            row["acquisition_channel"],
        )
        for row in rows
    ]

    conn.executemany(
        """
        INSERT INTO customers (
            customer_id, first_name, last_name, email,
            city, state, signup_date, acquisition_channel
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """,
        cleaned_rows,
    )


def load_orders(conn: sqlite3.Connection) -> None:
    rows = read_csv("sample_orders.csv")
    cleaned_rows = [
        (
            row["order_id"],
            row["customer_id"],
            row["order_date"],
            row["status"],
            float(row["subtotal"]),
            float(row["shipping_fee"]),
            float(row["tax"]),
            float(row["total"]),
            row["payment_method"],
        )
        for row in rows
    ]

    conn.executemany(
        """
        INSERT INTO orders (
            order_id, customer_id, order_date, status,
            subtotal, shipping_fee, tax, total, payment_method
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        cleaned_rows,
    )


def load_order_items(conn: sqlite3.Connection) -> None:
    rows = read_csv("sample_order_items.csv")
    cleaned_rows = [
        (
            row["order_item_id"],
            row["order_id"],
            row["product_id"],
            int(row["quantity"]),
            float(row["unit_price"]),
            float(row["line_total"]),
        )
        for row in rows
    ]

    conn.executemany(
        """
        INSERT INTO order_items (
            order_item_id, order_id, product_id,
            quantity, unit_price, line_total
        )
        VALUES (?, ?, ?, ?, ?, ?);
        """,
        cleaned_rows,
    )


def load_marketing_campaigns(conn: sqlite3.Connection) -> None:
    rows = read_csv("sample_marketing_campaigns.csv")
    cleaned_rows = [
        (
            row["campaign_id"],
            row["campaign_name"],
            row["channel"],
            row["start_date"],
            row["end_date"],
            float(row["budget"]),
            row["target_category"],
            int(row["clicks"]),
            int(row["conversions"]),
            float(row["revenue_attributed"]),
        )
        for row in rows
    ]

    conn.executemany(
        """
        INSERT INTO marketing_campaigns (
            campaign_id, campaign_name, channel,
            start_date, end_date, budget, target_category,
            clicks, conversions, revenue_attributed
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        cleaned_rows,
    )


def print_table_counts(conn: sqlite3.Connection) -> None:
    tables = [
        "products",
        "customers",
        "orders",
        "order_items",
        "marketing_campaigns",
    ]

    print(f"Database created at: {DB_PATH}")

    for table in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
        print(f"{table}: {count} rows")


def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        create_tables(conn)

        load_products(conn)
        load_customers(conn)
        load_orders(conn)
        load_order_items(conn)
        load_marketing_campaigns(conn)

        conn.commit()
        print_table_counts(conn)


if __name__ == "__main__":
    main()