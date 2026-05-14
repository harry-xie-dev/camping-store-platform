# Camping Store Data Platform

## Project Overview

Camping Store Data Platform is a portfolio project that models an end-to-end data platform for a simulated small outdoor camping tableware store. The project is designed to demonstrate practical data engineering, backend, frontend, and analytics planning around product tracking, customer records, order activity, and future marketing analysis.

This repository is not connected to a real company, real customers, or a production system. All future data, workflows, and analysis should be treated as simulated project material.

## Business Problem

A small camping tableware store needs a better way to organize operational data across products, customers, orders, and marketing activity. Without a structured data platform, it is difficult to answer basic business questions such as:

- Which products are available and how are they categorized?
- Who has placed orders?
- What items are included in each order?
- Which marketing campaigns are associated with customer or order activity?
- What data should be collected now to support future analytics?

## Core Features

Planned platform capabilities include:

- Product catalog tracking for camping tableware items.
- Customer data management for simulated customer profiles.
- Order and order item tracking.
- Initial marketing campaign data structure.
- Backend API planning for future data access.
- Frontend planning for future operational views.
- Analytics planning for future reporting and business questions.

## Planned Tech Stack

The planned stack may evolve as the project develops:

- Backend: Python, FastAPI
- Database: PostgreSQL
- Frontend: React or Next.js
- Analytics: SQL, Python, notebooks, dashboard tooling
- Development tools: Git, Docker, environment-based configuration

## Project Structure

```text
camping-store-platform/
|-- analytics/      # Future analytics notebooks, SQL queries, and reports
|-- backend/        # Future API, service logic, and database integration
|-- data/           # Sample CSV data and local SQLite database
|-- docs/           # Project planning and design documentation
|-- frontend/       # Future user interface for store operations
|-- reports/        # Generated CSV business reports
|-- scripts/        # Data generation, database loading, validation, analytics, and reporting scripts
`-- README.md       # Main project documentation
```

## Current Feature

- Generate synthetic sample data for products, customers, orders, order items, and marketing campaigns.
- Load CSV data into a local SQLite database.
- Inspect SQLite database tables, columns, and sample rows for debugging.
- Validate database integrity, including row counts, foreign key consistency, line item totals, and order totals.
- Run basic sales analytics queries from SQLite.
    - Revenue by product category
    - Top products by revevnue
    - Top customers by spending
    - Monthly revenue trend

## How to Run

- Generate sample data: python scripts/generate_sample_data.py
- Load CSV files into SQLite: python scripts/load_csv_to_sqlite.py
- Validate the database: python scripts/validate_database.py
- Run basic analytics: python scripts/run_basic_analytics.py
- Generate CSV reports: python scripts/generate_reports.py
- Generated reports are saved in the reports/ directory.

## Current Status

Current phase: local data platform prototype.

The project currently includes simulated CSV data, a local SQLite database, database validation scripts, basic sales analytics queries, automated CSV report generation, and database inspection tooling. Backend, frontend, dashboard, and production database components are planned for later phases.
