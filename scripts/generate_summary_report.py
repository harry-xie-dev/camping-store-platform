from pathlib import Path
import sqlite3
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "camping_store.db"
REPORTS_DIR = BASE_DIR / "reports"
OUTPUT_PATH = REPORTS_DIR / "report_summary.md"


def fetch_one(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchone()


def fetch_all(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def format_currency(value):
    return f"${value:,.2f}"


def generate_summary_report():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    total_orders = fetch_one(
        conn,
        """
        SELECT COUNT(*)
        FROM orders;
        """,
    )[0]

    completed_order_count, total_revenue, avg_order_value = fetch_one(
        conn,
        """
        SELECT 
            COUNT(*) AS completed_orders,
            COALESCE(SUM(total), 0) AS total_revenue,
            COALESCE(AVG(total), 0) AS avg_order_value
        FROM orders
        WHERE status = 'completed';
        """,
    )

    status_counts = fetch_all(
        conn,
        """
        SELECT status, COUNT(*)
        FROM orders
        GROUP BY status
        ORDER BY COUNT(*) DESC;
        """,
    )

    top_category = fetch_one(
        conn,
        """
        SELECT 
            p.category,
            COALESCE(SUM(oi.line_total), 0) AS revenue
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.status = 'completed'
        GROUP BY p.category
        ORDER BY revenue DESC
        LIMIT 1;
        """,
    )

    top_product = fetch_one(
        conn,
        """
        SELECT 
            p.product_name,
            COALESCE(SUM(oi.line_total), 0) AS revenue
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.status = 'completed'
        GROUP BY p.product_name
        ORDER BY revenue DESC
        LIMIT 1;
        """,
    )

    top_customer = fetch_one(
        conn,
        """
        SELECT 
            c.first_name || ' ' || c.last_name AS customer_name,
            COALESCE(SUM(o.total), 0) AS spending
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.status = 'completed'
        GROUP BY c.customer_id, c.first_name, c.last_name
        ORDER BY spending DESC
        LIMIT 1;
        """,
    )

    monthly_revenue = fetch_all(
        conn,
        """
        SELECT 
            substr(order_date, 1, 7) AS month,
            COALESCE(SUM(total), 0) AS revenue
        FROM orders
        WHERE status = 'completed'
        GROUP BY month
        ORDER BY month;
        """,
    )

    conn.close()

    top_category_name = top_category[0] if top_category else "N/A"
    top_category_revenue = top_category[1] if top_category else 0

    top_product_name = top_product[0] if top_product else "N/A"
    top_product_revenue = top_product[1] if top_product else 0

    top_customer_name = top_customer[0] if top_customer else "N/A"
    top_customer_spending = top_customer[1] if top_customer else 0

    status_lines = "\n".join(
        [f"- {status}: {count}" for status, count in status_counts]
    )

    monthly_lines = "\n".join(
        [f"- {month}: {format_currency(revenue)}" for month, revenue in monthly_revenue]
    )

    if len(monthly_revenue) >= 2:
        first_month, first_revenue = monthly_revenue[0]
        last_month, last_revenue = monthly_revenue[-1]
        revenue_change = last_revenue - first_revenue

        if revenue_change > 0:
            trend_summary = (
                f"Revenue increased from {format_currency(first_revenue)} in "
                f"{first_month} to {format_currency(last_revenue)} in {last_month}."
            )
        elif revenue_change < 0:
            trend_summary = (
                f"Revenue decreased from {format_currency(first_revenue)} in "
                f"{first_month} to {format_currency(last_revenue)} in {last_month}."
            )
        else:
            trend_summary = (
                f"Revenue stayed flat between {first_month} and {last_month}."
            )
    else:
        trend_summary = "Not enough monthly data to determine a revenue trend."

    report = f"""# Camping Store Business Summary Report

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 1. Executive Summary

This report summarizes the sales performance of the camping store sample dataset. It includes key business metrics, top-performing categories, products, customers, and monthly revenue trends.

## 2. Key Metrics

| Metric | Value |
|---|---:|
| Total Orders | {total_orders} |
| Completed Orders | {completed_order_count} |
| Total Revenue | {format_currency(total_revenue)} |
| Average Order Value | {format_currency(avg_order_value)} |

## 3. Order Status Breakdown

{status_lines}

## 4. Top Performers

| Area | Result | Revenue / Spending |
|---|---|---:|
| Top Category | {top_category_name} | {format_currency(top_category_revenue)} |
| Top Product | {top_product_name} | {format_currency(top_product_revenue)} |
| Top Customer | {top_customer_name} | {format_currency(top_customer_spending)} |

## 5. Monthly Revenue Trend

{monthly_lines}

## 6. Business Observations

- The highest-performing category is **{top_category_name}**, generating {format_currency(top_category_revenue)} in completed-order revenue.
- The top product is **{top_product_name}**, generating {format_currency(top_product_revenue)}.
- The top customer is **{top_customer_name}**, with total completed-order spending of {format_currency(top_customer_spending)}.
- {trend_summary}

## 7. Notes

This report is generated automatically from the SQLite database. Only completed orders are counted as revenue to avoid overstating sales performance from canceled or incomplete orders.
"""

    OUTPUT_PATH.write_text(report, encoding="utf-8")
    print(f"Generated summary report: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_summary_report()