import csv
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "camping_store.db"
REPORTS_DIR = PROJECT_ROOT / "reports"


REPORT_QUERIES = {
    "revenue_by_category.csv": """
        SELECT
            p.category,
            ROUND(SUM(oi.line_total), 2) AS total_revenue,
            COUNT(DISTINCT o.order_id) AS order_count,
            SUM(oi.quantity) AS units_sold
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.status = 'completed'
        GROUP BY p.category
        ORDER BY total_revenue DESC;
    """,

    "top_products_by_revenue.csv": """
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            ROUND(SUM(oi.line_total), 2) AS total_revenue,
            SUM(oi.quantity) AS units_sold
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.status = 'completed'
        GROUP BY p.product_id, p.product_name, p.category
        ORDER BY total_revenue DESC
        LIMIT 10;
    """,

    "top_customers_by_spend.csv": """
        SELECT
            c.customer_id,
            c.first_name || ' ' || c.last_name AS customer_name,
            c.email,
            c.city,
            c.state,
            COUNT(DISTINCT o.order_id) AS completed_orders,
            ROUND(SUM(o.total), 2) AS total_spend
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.status = 'completed'
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city, c.state
        ORDER BY total_spend DESC
        LIMIT 10;
    """,

    "monthly_revenue_trend.csv": """
        SELECT
            SUBSTR(o.order_date, 1, 7) AS order_month,
            COUNT(DISTINCT o.order_id) AS completed_orders,
            ROUND(SUM(o.total), 2) AS total_revenue
        FROM orders o
        WHERE o.status = 'completed'
        GROUP BY order_month
        ORDER BY order_month;
    """,
}


def export_query_to_csv(connection: sqlite3.Connection, query: str, output_path: Path) -> None:
    cursor = connection.execute(query)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        writer.writerows(rows)


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    REPORTS_DIR.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        for filename, query in REPORT_QUERIES.items():
            output_path = REPORTS_DIR / filename
            export_query_to_csv(connection, query, output_path)
            print(f"Generated report: {output_path}")

    print("All reports generated successfully.")


if __name__ == "__main__":
    main()