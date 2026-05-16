# Camping Store Data Platform

## Project Overview

Camping Store Data Platform is an end-to-end portfolio data project for a simulated small outdoor camping tableware store. The project models how a small business can organize operational data, store it in a database, validate data quality, run business analytics, and generate reports that are easier for non-technical users to understand.

This repository is not connected to a real company, real customers, or a production system. All data is simulated for project and portfolio purposes.

## Business Problem

A small camping tableware store needs a better way to track products, customers, orders, and sales performance. Without a structured data platform, the business owner would have difficulty answering basic operational questions such as:

- Which product categories generate the most revenue?
- Which products are the top sellers?
- Which customers contribute the most completed-order revenue?
- How does revenue change month by month?
- Are the database records consistent and reliable enough for analysis?

This project solves the problem by building a local data pipeline that turns raw CSV data into validated database tables, SQL-based analytics, CSV reports, and PNG charts.

## Current Features

The project currently includes:

- Synthetic sample data generation for products, customers, orders, order items, and marketing campaigns.
- CSV-to-SQLite loading pipeline.
- SQLite database inspection tooling for debugging tables, columns, and sample rows.
- Database validation checks for:
  - Row counts
  - Foreign key relationships
  - Order item line totals
  - Order subtotal consistency
- SQL-based business analytics for:
  - Revenue by product category
  - Top products by revenue
  - Top customers by completed-order spending
  - Monthly revenue trend
- Automated CSV report generation.
- Automated PNG chart generation for visual business reporting.


## Data Pipeline

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
Validation + Analytics SQL
        |
        v
CSV Reports in reports/
        |
        v
PNG Charts in reports/charts/
```


## Project Structure


```text
camping-store-platform/
|-- analytics/              # Future analytics notebooks and deeper analysis
|-- backend/                # Future API and service layer
|-- data/                   # Sample CSV data and local SQLite database
|-- docs/                   # Project planning and database design documentation
|-- frontend/               # Future user interface
|-- reports/                # Generated CSV business reports
|   `-- charts/             # Generated PNG charts
|-- scripts/                # Data generation, loading, validation, analytics, and reporting scripts
`-- README.md               # Main project documentation
```


## Key Reports


```text
reports/
|-- revenue_by_category.csv
|-- top_products_by_revenue.csv
|-- top_customers_by_spend.csv
|-- monthly_revenue_trend.csv
```

The project also generates matching PNG charts under:

```text
|-- reports/charts/
```


## How to Run

From the project root directory, run the scripts in this order:

```text
python scripts/generate_sample_data.py
python scripts/load_csv_to_sqlite.py
python scripts/inspect_db.py
python scripts/validate_database.py
python scripts/run_basic_analytics.py
python scripts/generate_reports.py
python scripts/generate_charts.py
```


## How to Run the Data Pipeline

This project includes a one-command pipeline that regenerates the sample data, loads it into SQLite, validates the database, creates CSV reports, and generates charts.

From the project root, run:

``` text
python scripts/run_pipeline.py
```


Generated CSV reports are saved in:

```text
|-- reports/
```

Generated PNG are saved in:

```text
|-- reports/charts/
```


## Current status:

Current phase: local analytics platform prototype.

The project currently supports a complete local workflow from simulated business data to database storage, validation, analytics, CSV reports, and PNG chart generation.

Planned future improvements include:

FastAPI backend for accessing business data through API endpoints.
PostgreSQL migration for a more production-like database setup.
Dashboard or frontend interface for viewing reports.
More advanced marketing and customer behavior analysis.
Docker-based local development environment.