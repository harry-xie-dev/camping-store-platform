# Database Design

## Overview

This document proposes an initial relational database design for the simulated Camping Store Data Platform. The design is intentionally simple and focused on the core entities needed for product tracking, customer data, order data, and future marketing analytics.

No production database has been implemented yet.

## Initial Tables

### products

Stores the camping tableware items available in the simulated store.

Suggested fields:

- `product_id`: Primary key.
- `sku`: Unique product stock keeping unit.
- `name`: Product name.
- `category`: Product category, such as plates, bowls, mugs, utensils, or cookware accessories.
- `description`: Optional product description.
- `unit_price`: Current selling price.
- `is_active`: Whether the product is currently active.
- `created_at`: Record creation timestamp.
- `updated_at`: Last update timestamp.

### customers

Stores simulated customer profile information.

Suggested fields:

- `customer_id`: Primary key.
- `first_name`: Customer first name.
- `last_name`: Customer last name.
- `email`: Customer email address.
- `phone`: Optional phone number.
- `city`: Optional city.
- `state`: Optional state or region.
- `created_at`: Record creation timestamp.
- `updated_at`: Last update timestamp.

### orders

Stores order-level information.

Suggested fields:

- `order_id`: Primary key.
- `customer_id`: Foreign key to `customers.customer_id`.
- `order_date`: Date or timestamp when the order was placed.
- `order_status`: Current order status, such as pending, paid, shipped, completed, or cancelled.
- `order_total`: Total order amount.
- `campaign_id`: Optional foreign key to `marketing_campaigns.campaign_id`.
- `created_at`: Record creation timestamp.
- `updated_at`: Last update timestamp.

### order_items

Stores the individual products included in each order.

Suggested fields:

- `order_item_id`: Primary key.
- `order_id`: Foreign key to `orders.order_id`.
- `product_id`: Foreign key to `products.product_id`.
- `quantity`: Number of units ordered.
- `unit_price`: Product price at the time of the order.
- `line_total`: Quantity multiplied by unit price.

### marketing_campaigns

Stores simulated marketing campaign information for future analytics.

Suggested fields:

- `campaign_id`: Primary key.
- `campaign_name`: Campaign name.
- `channel`: Marketing channel, such as email, social, search, or referral.
- `start_date`: Campaign start date.
- `end_date`: Optional campaign end date.
- `budget`: Optional planned campaign budget.
- `created_at`: Record creation timestamp.
- `updated_at`: Last update timestamp.

## Initial Relationships

- One customer can place many orders.
- One order can contain many order items.
- One product can appear in many order items.
- One marketing campaign can be associated with many orders.

## Design Notes

This design is a starting point for portfolio planning. Future iterations may add inventory tracking, product variants, addresses, payments, returns, campaign attribution details, or audit fields as the project scope becomes more specific.
