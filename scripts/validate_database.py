import sqlite3
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "data" / "camping_store.db"


def print_check(name: str, passed: bool, detail: str = "") -> None:
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        print(f"       {detail}")


def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        print(f"Validating database: {DB_PATH}\n")

        # 1. Check table counts
        expected_tables = [
            "products",
            "customers",
            "orders",
            "order_items",
            "marketing_campaigns",
        ]

        for table in expected_tables:
            count = conn.execute(f"SELECT COUNT(*) AS count FROM {table};").fetchone()["count"]
            print_check(f"{table} has data", count > 0, f"{count} rows")

        print()

        # 2. Check SQLite foreign key violations
        fk_errors = conn.execute("PRAGMA foreign_key_check;").fetchall()
        print_check(
            "SQLite foreign key check",
            len(fk_errors) == 0,
            f"{len(fk_errors)} violation(s)",
        )

        # 3. Check orders -> customers
        missing_customers = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM orders o
            LEFT JOIN customers c
                ON o.customer_id = c.customer_id
            WHERE c.customer_id IS NULL;
            """
        ).fetchone()["count"]

        print_check(
            "Every order has a valid customer",
            missing_customers == 0,
            f"{missing_customers} missing customer reference(s)",
        )

        # 4. Check order_items -> orders
        missing_orders = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM order_items oi
            LEFT JOIN orders o
                ON oi.order_id = o.order_id
            WHERE o.order_id IS NULL;
            """
        ).fetchone()["count"]

        print_check(
            "Every order item has a valid order",
            missing_orders == 0,
            f"{missing_orders} missing order reference(s)",
        )

        # 5. Check order_items -> products
        missing_products = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM order_items oi
            LEFT JOIN products p
                ON oi.product_id = p.product_id
            WHERE p.product_id IS NULL;
            """
        ).fetchone()["count"]

        print_check(
            "Every order item has a valid product",
            missing_products == 0,
            f"{missing_products} missing product reference(s)",
        )

        # 6. Check line_total = quantity * unit_price
        line_total_errors = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM order_items
            WHERE ABS(line_total - quantity * unit_price) > 0.01;
            """
        ).fetchone()["count"]

        print_check(
            "Order item line totals are correct",
            line_total_errors == 0,
            f"{line_total_errors} line total mismatch(es)",
        )

        # 7. Check order subtotal = sum(order item line_total)
        subtotal_errors = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM orders o
            JOIN (
                SELECT order_id, ROUND(SUM(line_total), 2) AS calculated_subtotal
                FROM order_items
                GROUP BY order_id
            ) item_totals
                ON o.order_id = item_totals.order_id
            WHERE ABS(o.subtotal - item_totals.calculated_subtotal) > 0.01;
            """
        ).fetchone()["count"]

        print_check(
            "Order subtotals match order items",
            subtotal_errors == 0,
            f"{subtotal_errors} subtotal mismatch(es)",
        )

        # 8. Show one joined business-readable example
        print("\nSample joined order:")
        sample = conn.execute(
            """
            SELECT
                o.order_id,
                c.first_name || ' ' || c.last_name AS customer_name,
                p.product_name,
                oi.quantity,
                oi.unit_price,
                oi.line_total,
                o.total
            FROM orders o
            JOIN customers c
                ON o.customer_id = c.customer_id
            JOIN order_items oi
                ON o.order_id = oi.order_id
            JOIN products p
                ON oi.product_id = p.product_id
            LIMIT 5;
            """
        ).fetchall()

        for row in sample:
            print(dict(row))


if __name__ == "__main__":
    main()