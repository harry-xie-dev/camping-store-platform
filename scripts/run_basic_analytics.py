import sqlite3
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "data" / "camping_store.db"


def print_rows(title: str, rows: list[sqlite3.Row]) -> None:
    print(f"\n{title}")
    print("-" * len(title))

    for row in rows:
        print(dict(row))


def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        revenue_by_category = conn.execute(
            """
            SELECT
                p.category,
                ROUND(SUM(oi.line_total), 2) AS revenue,
                SUM(oi.quantity) AS units_sold
            FROM order_items oi
            JOIN products p
                ON oi.product_id = p.product_id
            JOIN orders o
                ON oi.order_id = o.order_id
            WHERE o.status = 'completed'
            GROUP BY p.category
            ORDER BY revenue DESC;
            """
        ).fetchall()

        top_products = conn.execute(
            """
            SELECT
                p.product_name,
                p.category,
                SUM(oi.quantity) AS units_sold,
                ROUND(SUM(oi.line_total), 2) AS revenue
            FROM order_items oi
            JOIN products p
                ON oi.product_id = p.product_id
            JOIN orders o
                ON oi.order_id = o.order_id
            WHERE o.status = 'completed'
            GROUP BY p.product_id, p.product_name, p.category
            ORDER BY revenue DESC
            LIMIT 5;
            """
        ).fetchall()

        customer_order_summary = conn.execute(
            """
            SELECT
                c.customer_id,
                c.first_name || ' ' || c.last_name AS customer_name,
                COUNT(o.order_id) AS completed_orders,
                ROUND(SUM(o.total), 2) AS total_spent
            FROM customers c
            JOIN orders o
                ON c.customer_id = o.customer_id
            WHERE o.status = 'completed'
            GROUP BY c.customer_id, customer_name
            ORDER BY total_spent DESC
            LIMIT 5;
            """
        ).fetchall()

        print_rows("Revenue by category", revenue_by_category)
        print_rows("Top 5 products by revenue", top_products)
        print_rows("Top 5 customers by completed order spending", customer_order_summary)


if __name__ == "__main__":
    main()