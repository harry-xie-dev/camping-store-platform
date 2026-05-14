from pathlib import Path
import csv

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = BASE_DIR / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"


def read_csv(filename):
    path = REPORTS_DIR / filename
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def save_bar_chart(labels, values, title, xlabel, ylabel, output_filename):
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    output_path = CHARTS_DIR / output_filename
    plt.savefig(output_path)
    plt.close()

    print(f"Generated: {output_path}")


def save_line_chart(labels, values, title, xlabel, ylabel, output_filename):
    plt.figure(figsize=(10, 6))
    plt.plot(labels, values, marker="o")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    output_path = CHARTS_DIR / output_filename
    plt.savefig(output_path)
    plt.close()

    print(f"Generated: {output_path}")


def generate_revenue_by_category_chart():
    rows = read_csv("revenue_by_category.csv")

    labels = [row["category"] for row in rows]
    values = [float(row["total_revenue"]) for row in rows]

    save_bar_chart(
        labels,
        values,
        "Revenue by Product Category",
        "Category",
        "Revenue",
        "revenue_by_category.png",
    )


def generate_top_products_chart():
    rows = read_csv("top_products_by_revenue.csv")

    labels = [row["product_name"] for row in rows]
    values = [float(row["total_revenue"]) for row in rows]

    save_bar_chart(
        labels,
        values,
        "Top Products by Revenue",
        "Product",
        "Revenue",
        "top_products_by_revenue.png",
    )


def generate_top_customers_chart():
    rows = read_csv("top_customers_by_spend.csv")

    labels = [row["customer_name"] for row in rows]
    values = [float(row["total_spend"]) for row in rows]

    save_bar_chart(
        labels,
        values,
        "Top Customers by Spend",
        "Customer",
        "Total Spend",
        "top_customers_by_spend.png",
    )


def generate_monthly_revenue_chart():
    rows = read_csv("monthly_revenue_trend.csv")

    labels = [row["order_month"] for row in rows]
    values = [float(row["total_revenue"]) for row in rows]

    save_line_chart(
        labels,
        values,
        "Monthly Revenue Trend",
        "Month",
        "Revenue",
        "monthly_revenue_trend.png",
    )


def main():
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    generate_revenue_by_category_chart()
    generate_top_products_chart()
    generate_top_customers_chart()
    generate_monthly_revenue_chart()

    print("All charts generated successfully.")


if __name__ == "__main__":
    main()