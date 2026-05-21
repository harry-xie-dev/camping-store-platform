# Camping Store Data Platform - Project Design Notes

## 1. Purpose of This Document

This document records the main design decisions, implementation notes, and lessons learned while building the Camping Store Data Platform.

The goal of this document is to explain why the project is structured the way it is, not just what files exist.

This file is different from the technical walkthrough:

- `technical_walkthrough.md` explains the project from a higher-level technical and business perspective.
- `project_design_notes.md` records the design reasoning, implementation decisions, and limitations behind the project.

---

## 2. Core Design Principle

The main design principle of this project is to make the analytics workflow repeatable, explainable, and easy to inspect.

Instead of manually opening CSV files or writing one-off SQL queries, the project organizes the workflow into a pipeline:

```text
raw data -> database -> validation -> reports -> charts -> business summary
```

Each stage has a clear responsibility:

- Raw data is generated as CSV files.
- CSV files are loaded into a SQLite database.
- The database is validated before analysis.
- Analytical reports are generated from validated data.
- Charts are created for visual inspection.
- A Markdown summary translates the results into business-readable insights.

This separation makes the project easier to debug, extend, and explain.

---

## 3. Data Modeling Notes

The project separates data into four main entities:

- `products`
- `customers`
- `orders`
- `order_items`

The most important modeling decision is separating `orders` and `order_items`.

An order represents the transaction as a whole. It includes information such as:

- order ID
- customer ID
- order date
- order status
- total order amount

Order items represent the individual products inside an order. They include information such as:

- order ID
- product ID
- quantity
- unit price
- line total

This separation matters because one order can contain multiple products.

If all information were stored in one flat table, order-level fields would be repeated across multiple rows. That would increase the risk of double-counting order totals during analysis.

By separating order-level data from item-level data, the project better represents the real relationship between transactions and products.

---

## 4. Revenue Logic

Revenue is calculated only from completed orders.

Pending, canceled, and refunded orders are excluded because they do not represent finalized sales.

This rule matters because revenue is not just a technical calculation. It is a business definition.

If canceled or refunded orders were included, the reports would overstate business performance. If pending orders were included, the report would treat unfinished transactions as confirmed sales.

The current revenue rule is:

```text
revenue = sum of completed order totals
```

This rule affects every downstream report, including:

- total revenue
- average order value
- revenue by category
- top products by revenue
- top customers by spending
- monthly revenue trend

---

## 5. Validation Logic

The validation step exists to make sure the reports are built on reliable data.

The validation script checks whether the database was loaded correctly and whether important relationships and calculations are consistent.

The validation logic checks:

- whether expected tables exist
- whether data was loaded into SQLite
- whether orders reference valid customers
- whether order items reference valid orders
- whether order items reference valid products
- whether line totals match quantity multiplied by unit price
- whether order totals match the sum of their order items

This step prevents the pipeline from generating reports from broken or inconsistent data.

For example, if an order item references a product ID that does not exist in the products table, product-level revenue reports would be unreliable.

If line totals or order totals are incorrect, revenue reports could become misleading.

The validation step protects the reporting layer from bad input.

---

## 6. Reporting Notes

The project generates both structured reports and business-readable summaries.

CSV reports are useful because they can be:

- opened in Excel
- reviewed manually
- imported into dashboards
- used by another script
- shared with technical or semi-technical users

The Markdown business summary is useful because it gives a non-technical user a quick explanation of business performance without requiring them to read raw data, CSV files, or SQL queries.

The main generated reports include:

- `revenue_by_category.csv`
- `top_products_by_revenue.csv`
- `top_customers_by_spend.csv`
- `monthly_revenue_trend.csv`
- PNG charts under `reports/charts/`
- `report_summary.md`

The CSV reports provide structured outputs.

The charts provide visual interpretation.

The Markdown report provides business explanation.

Together, these outputs make the project more useful than a script that only prints SQL query results.

---

## 7. Pipeline Design Notes

The project uses a one-command pipeline through:

```bash
python scripts/run_pipeline.py
```

The pipeline runs the major steps in order:

```text
generate sample data
load CSV data into SQLite
validate the database
generate CSV reports
generate charts
generate Markdown summary report
```

This order is intentional.

Data must be generated before it can be loaded.

Data must be loaded before it can be validated.

Data should be validated before reports are generated.

Reports and charts should be generated from validated data.

The final summary report should represent the completed pipeline output.

This makes the workflow reproducible. A user does not need to remember multiple commands or run scripts manually in the correct order.

---

## 8. Implementation Lessons

### Schema consistency

Several implementation issues came from schema mismatches.

For example, some queries assumed column names such as:

- `name`
- `total_amount`
- `customer_name`

But the actual database schema used:

- `product_name`
- `total`
- `first_name`
- `last_name`

The lesson is that reporting logic must be based on the actual database schema, not assumed field names.

When a SQL query fails, one of the first things to check is whether the selected columns actually exist in the table.

### Customer name construction

The customers table stores first and last names separately.

When the summary report needed a full customer name, the query constructed it directly in SQL:

```sql
c.first_name || ' ' || c.last_name AS customer_name
```

The query also grouped by the actual schema fields:

```sql
GROUP BY c.customer_id, c.first_name, c.last_name
```

This is more reliable than grouping only by customer name because different customers could theoretically share the same first and last name.

Using `customer_id` keeps the aggregation tied to the unique customer record.

### Git workflow

The project also reinforced basic Git workflow concepts.

New source files appear as untracked until they are added with:

```bash
git add <file>
```

Tracked files appear as modified when their contents change.

Generated reports may also appear as modified if they are committed to the repository and regenerated later.

This matters because a project with generated outputs needs a clear decision about which generated files should be committed and which should be ignored.

### Timestamp behavior

The Markdown summary report includes a generated timestamp.

Because of that, `reports/report_summary.md` becomes modified every time the pipeline runs, even if the underlying business data stays the same.

This is expected behavior because the timestamp changes on every run.

The tradeoff is:

- keeping the timestamp makes the report look more like a real generated report
- removing the timestamp would make Git diffs cleaner

For now, the timestamp is kept because it shows when the report was generated.

---

## 9. Current Limitations

The current version of the project has several limitations.

### Simulated data

The project currently uses simulated sample data.

This is useful for development and portfolio demonstration, but it does not yet prove that the pipeline can handle messy real business data.

### Local-only workflow

The project currently runs locally.

It is not deployed as a web app, API service, or cloud-based data pipeline.

### Batch-based processing

The pipeline is batch-based.

It runs when the user executes the command, but it does not automatically update in real time.

### Limited error handling

The current scripts can run successfully, but error handling could be improved.

For example, the project could provide clearer error messages when expected files, folders, or tables are missing.

### No automated unit tests yet

The project has validation scripts, but it does not yet have formal unit tests with a framework like `pytest`.

### No dashboard UI yet

The project generates CSV reports, charts, and Markdown summaries, but it does not yet include an interactive dashboard.

### No real CSV upload support yet

The project does not yet allow a business user to upload their own CSV files through a simple interface.

---

## 10. Future Engineering Improvements

Potential future improvements include:

### Add automated tests

Add `pytest` tests for:

- data generation
- database loading
- validation logic
- report generation
- revenue calculations

This would make the project more reliable and easier to change.

### Add structured logging

Replace or supplement basic `print` statements with structured logging.

This would make pipeline runs easier to inspect, especially if the project grows.

### Add better exception handling

Improve error handling for cases such as:

- missing CSV files
- missing database file
- missing tables
- unexpected column names
- invalid data types
- empty reports

### Add configuration support

Move paths and settings into a configuration file.

This would make the project easier to adapt to different environments.

### Support real business CSV uploads

Allow the pipeline to work with real business CSV exports instead of only generated sample data.

This would make the project more realistic and useful.

### Add a dashboard

Add a Streamlit or Flask dashboard so users can view KPIs, charts, and reports from a browser.

### Add customer segmentation

Analyze customers by behavior, spending level, or repeat purchase activity.

### Add repeat purchase analysis

Identify customers who purchase multiple times and calculate repeat customer metrics.

### Add inventory risk analysis

Use sales patterns to identify products that may be overstocked, understocked, or slow-moving.

### Add deployment

Deploy the project as a small internal analytics tool.

Possible deployment directions include:

- Streamlit app
- Flask web app
- scheduled batch job
- cloud-hosted dashboard
- lightweight internal reporting service

---

## 11. Resume and Interview Positioning

This project should be positioned as a data analytics / data engineering portfolio project.

The strongest points to emphasize are:

- ETL-style pipeline design
- relational database modeling
- SQL-based reporting
- data validation before analysis
- automated report generation
- business-readable summaries
- reproducible one-command workflow

This project is stronger for Data Analyst, Business Analyst, junior Data Engineer, or analytics engineering roles than for pure Software Engineer roles.

For Software Engineer positioning, the project would need additional engineering depth, such as:

- API layer
- web dashboard
- automated tests
- deployment
- authentication
- package structure
- better error handling
- CI workflow

---

## 12. Key Takeaways

The main takeaway from this project is that data work is not only about writing SQL queries.

A useful analytics project needs:

- clear data modeling
- reliable data loading
- validation before reporting
- correct business definitions
- reproducible workflows
- outputs that business users can understand

The project turns raw operational data into reports, charts, and a business summary that can support decision-making.

The most important design idea is:

```text
Do not generate business insights from unchecked data.
```

That is why the project separates loading, validation, reporting, visualization, and summary generation into different stages.