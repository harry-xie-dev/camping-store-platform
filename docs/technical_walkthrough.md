# Camping Store Data Platform - Technical Walkthrough

## 1. Project Overview

This project is a small business analytics pipeline for a simulated camping store. I built it to practice the full workflow from raw operational data to business-readable reporting.

The pipeline generates sample CSV data, loads the data into a SQLite database, validates the database, generates analytical CSV reports, creates PNG charts, and produces a Markdown business summary report.

The main idea is not just to create reports, but to make the process repeatable with one command:

```bash
python scripts/run_pipeline.py
```

This makes the project closer to a real analytics workflow where data is prepared, checked, analyzed, visualized, and summarized for business users.

---

## 2. Business Problem

Small businesses often have sales and order data stored across spreadsheets or operational systems. Without a repeatable reporting process, it can be difficult for the owner or operator to answer basic business questions quickly.

This project simulates how a small camping store could organize transaction data and answer questions such as:

- Which product categories generate the most revenue?
- Which products perform best?
- Who are the top customers?
- How does revenue change by month?
- Are canceled, refunded, or pending orders affecting revenue reporting?

The goal is to turn raw transaction data into reliable business insights.

---

## 3. Pipeline Architecture

The project follows an ETL-style workflow:

```text
Sample Data Generation
        |
        v
CSV Files in data/
        |
        v
SQLite Database
        |
        v
Database Validation
        |
        v
CSV Reports
        |
        v
PNG Charts
        |
        v
Markdown Business Summary
```

The full pipeline can be executed with:

```bash
python scripts/run_pipeline.py
```

The pipeline is separated into multiple scripts so each stage has a clear responsibility:

- Generate sample operational data
- Load CSV files into SQLite
- Validate database quality and calculations
- Generate analytical CSV reports
- Generate charts for visual analysis
- Generate a business-readable Markdown summary

This structure makes the workflow easier to debug, test, and extend.

---

## 4. Data Model

The project uses four main tables:

### products

Stores product-level information such as product ID, product name, category, and price.

### customers

Stores customer-level information such as customer ID, first name, last name, and customer-related attributes.

### orders

Stores order-level information such as order ID, customer ID, order date, order status, and total order amount.

### order_items

Stores item-level details inside each order, including product ID, quantity, unit price, and line total.

The reason for separating `orders` and `order_items` is that one order can contain multiple products. The `orders` table represents the transaction as a whole, while `order_items` represents the individual products inside that transaction.

This avoids repeating order-level information across multiple product rows and reduces the risk of double-counting during analysis.

---

## 5. Key Design Decisions

### Why use SQLite instead of only CSV?

CSV files are useful for storing raw data, but this project has relationships between customers, orders, order items, and products. SQLite makes those relationships easier to query and validate.

For example, one order can contain multiple order items, and each order item connects to a product. This relationship is easier to represent and analyze in a relational database than in separate CSV files alone.

### Why separate `orders` and `order_items`?

The `orders` table stores order-level information such as order ID, customer ID, order date, status, and total order amount.

The `order_items` table stores product-level details inside each order, such as product ID, quantity, unit price, and line total.

This separation matters because one order can contain multiple products. If everything were stored in one flat table, order-level information would be repeated across multiple rows and could easily cause double-counting during analysis.

### Why validate the database before reporting?

Reports are only useful if the underlying data is reliable. The validation step checks whether the database was loaded correctly and whether key calculations and relationships are consistent before generating business reports.

The validation logic checks areas such as:

- Row counts
- Foreign key relationships
- Line total calculations
- Order subtotal consistency

This helps prevent incorrect reports from being generated from incomplete or inconsistent data.

### Why count only completed orders as revenue?

Only completed orders represent finalized sales. Pending, canceled, or refunded orders should not be counted as revenue because including them would overstate business performance.

This is an important business rule because the definition of revenue directly affects every downstream report.

### Why generate both CSV reports and a Markdown summary?

CSV reports are structured analytical outputs that can be opened in Excel, used by other scripts, or imported into dashboards.

The Markdown summary is designed for non-technical users who want quick business insights without reading raw data, CSV files, or SQL queries.

---

## 6. Data Quality and Validation Logic

The validation step is designed to check whether the database is reliable before generating reports.

The validation script checks that:

- Expected tables exist
- CSV data has been loaded into SQLite
- Orders reference valid customers
- Order items reference valid orders and products
- Line totals match quantity multiplied by unit price
- Order totals are consistent with the sum of their order items

This step matters because business reporting depends on trust in the underlying data. If the database contains broken relationships or incorrect totals, then revenue reports, customer rankings, and product analysis may be misleading.

---

## 7. Reporting Logic

The project generates several analytical outputs:

- Revenue by category
- Top products by revenue
- Top customers by spending
- Monthly revenue trend
- PNG charts for visual analysis
- Markdown business summary report

The reporting logic focuses on completed orders only when calculating revenue. This prevents canceled, refunded, or pending orders from inflating sales performance.

The final Markdown summary report includes:

- Total orders
- Completed orders
- Total revenue
- Average order value
- Order status breakdown
- Top category
- Top product
- Top customer
- Monthly revenue trend
- Business observations

This creates a bridge between structured analytical data and business-readable insight.

---

## 8. Implementation Notes and Lessons Learned

### Schema consistency

During development, I ran into several schema mismatch issues. For example, one query referenced `p.name`, but the actual products table used `product_name`.

Another query referenced `o.total_amount`, but the actual orders table used `total`.

These issues showed why it is important to inspect the actual database schema instead of assuming column names.

### Customer name construction

When generating the Markdown summary report, the query originally referenced `c.customer_name`, but the customers table stored names as `first_name` and `last_name`.

I fixed this by constructing the full customer name directly in SQL:

```sql
c.first_name || ' ' || c.last_name AS customer_name
```

Then I grouped by the actual schema fields:

```sql
GROUP BY c.customer_id, c.first_name, c.last_name
```

This made the customer aggregation more reliable because the query uses the real table structure.

### Git workflow for generated outputs

I also practiced tracking generated files and source files with Git.

New scripts appeared as untracked files until added with `git add`, while generated reports appeared as modified files if they were already tracked.

This helped clarify the difference between:

- Untracked files
- Modified files
- Staged files
- Committed files

### Timestamp behavior

The Markdown summary report includes a generated timestamp. Because of that, `reports/report_summary.md` becomes modified every time the pipeline runs, even if the business data stays the same.

This is expected behavior, but it is important to keep in mind when reviewing Git diffs.

---

## 9. Business Value

The value of this project is that it turns raw transaction data into decision-ready business insight.

A non-technical business owner does not need to open multiple CSV files or write SQL queries. They can run one command and receive reports, charts, and a summary explaining the store's sales performance.

The project helps answer practical business questions such as:

- Which categories perform best?
- Which products generate the most revenue?
- Which customers spend the most?
- How does revenue change over time?
- Are non-completed orders affecting sales reporting?

This makes the project more than a data-processing script. It simulates a repeatable reporting workflow for a small business.

---

## 10. Limitations and Future Improvements

Current limitations:

- The project uses simulated data instead of real business data.
- The pipeline is batch-based, not real-time.
- The project does not yet include automated unit tests.
- The project does not yet include a web dashboard.
- The current workflow runs locally rather than in a deployed environment.

Possible future improvements:

- Add a Streamlit or Flask dashboard
- Add automated tests with pytest
- Add logging and better error handling
- Support real business CSV uploads
- Add customer segmentation analysis
- Add repeat purchase analysis
- Add inventory risk analysis
- Add configuration files for easier environment setup
- Deploy the project as a small internal reporting tool

---

## 11. How I Would Explain This Project

I built a small business analytics pipeline for a simulated camping store. The project starts with raw CSV data and turns it into validated database tables, analytical reports, charts, and a business-readable Markdown summary.

The pipeline has several stages: sample data generation, CSV-to-SQLite loading, database validation, report generation, chart generation, and summary report generation. I connected these steps into one command through `scripts/run_pipeline.py`, so the whole workflow can be reproduced consistently.

One important design decision was using SQLite instead of only CSV files. Since the data has relationships between customers, orders, order items, and products, a relational database makes it easier to query and validate the data. I also separated `orders` and `order_items` because one order can contain multiple products.

Another important decision was validating the database before reporting. The validation step checks row counts, foreign key relationships, line totals, and order subtotals. This makes the reports more reliable because I am not generating business insights from unchecked data.

For revenue reporting, I only count completed orders. Pending, canceled, and refunded orders are excluded because they do not represent finalized sales. This prevents the reports from overstating business performance.

During development, I fixed several schema mismatch issues. For example, I changed `p.name` to `product_name`, `o.total_amount` to `total`, and built customer names from `first_name` and `last_name` because there was no `customer_name` column. These issues helped me better understand the actual database schema and debug the SQL queries more carefully.

The business value of the project is that a non-technical store owner can run one command and get CSV reports, charts, and an executive-style summary instead of manually checking raw data or writing SQL queries.