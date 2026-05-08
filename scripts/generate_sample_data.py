from pathlib import Path
import csv
import random
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"

random.seed(42)


def money(value):
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def write_csv(filename, fieldnames, rows):
    DATA_DIR.mkdir(exist_ok=True)

    with open(DATA_DIR / filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    products = [
        {
            "product_id": "P001",
            "sku": "CG-UTL-001",
            "product_name": "Stainless Steel Camping Utensil Set",
            "category": "camping utensils",
            "brand": "TrailMate",
            "unit_price": "18.99",
            "cost": "7.50",
            "stock_quantity": 120,
            "supplier": "Outdoor Supply Co",
            "active": "true",
        },
        {
            "product_id": "P002",
            "sku": "CG-UTL-002",
            "product_name": "Titanium Folding Spork",
            "category": "camping utensils",
            "brand": "SummitLite",
            "unit_price": "12.49",
            "cost": "4.20",
            "stock_quantity": 90,
            "supplier": "Summit Wholesale",
            "active": "true",
        },
        {
            "product_id": "P003",
            "sku": "CG-COOK-001",
            "product_name": "Compact Camping Cookware Kit",
            "category": "camping cookware",
            "brand": "CampForge",
            "unit_price": "39.99",
            "cost": "18.75",
            "stock_quantity": 64,
            "supplier": "Outdoor Supply Co",
            "active": "true",
        },
        {
            "product_id": "P004",
            "sku": "CG-COOK-002",
            "product_name": "Nonstick Portable Fry Pan",
            "category": "camping cookware",
            "brand": "CampForge",
            "unit_price": "24.99",
            "cost": "10.60",
            "stock_quantity": 75,
            "supplier": "Camp Essentials Ltd",
            "active": "true",
        },
        {
            "product_id": "P005",
            "sku": "CG-BOWL-001",
            "product_name": "Collapsible Silicone Camping Bowl",
            "category": "camping dinnerware",
            "brand": "TrailMate",
            "unit_price": "9.99",
            "cost": "3.10",
            "stock_quantity": 150,
            "supplier": "Camp Essentials Ltd",
            "active": "true",
        },
        {
            "product_id": "P006",
            "sku": "CG-MUG-001",
            "product_name": "Insulated Stainless Camping Mug",
            "category": "camping drinkware",
            "brand": "NorthPeak",
            "unit_price": "16.99",
            "cost": "6.25",
            "stock_quantity": 110,
            "supplier": "NorthPeak Distribution",
            "active": "true",
        },
        {
            "product_id": "P007",
            "sku": "CG-BTL-001",
            "product_name": "BPA-Free Trail Water Bottle",
            "category": "camping drinkware",
            "brand": "HydroTrail",
            "unit_price": "21.99",
            "cost": "8.40",
            "stock_quantity": 95,
            "supplier": "HydroTrail Partners",
            "active": "true",
        },
        {
            "product_id": "P008",
            "sku": "CG-CASE-001",
            "product_name": "Hard Shell Camping Utensil Case",
            "category": "storage",
            "brand": "TrailMate",
            "unit_price": "14.99",
            "cost": "5.10",
            "stock_quantity": 85,
            "supplier": "Outdoor Supply Co",
            "active": "true",
        },
        {
            "product_id": "P009",
            "sku": "CG-KIT-001",
            "product_name": "Family Camping Dinnerware Bundle",
            "category": "camping dinnerware",
            "brand": "BaseCamp Goods",
            "unit_price": "54.99",
            "cost": "25.50",
            "stock_quantity": 40,
            "supplier": "BaseCamp Wholesale",
            "active": "true",
        },
        {
            "product_id": "P010",
            "sku": "CG-ACC-001",
            "product_name": "Reusable Camp Cleaning Cloth Set",
            "category": "camping accessories",
            "brand": "EcoTrail",
            "unit_price": "8.99",
            "cost": "2.40",
            "stock_quantity": 180,
            "supplier": "EcoTrail Supply",
            "active": "true",
        },
        {
            "product_id": "P011",
            "sku": "CG-COOK-003",
            "product_name": "Portable Camping Kettle",
            "category": "camping cookware",
            "brand": "NorthPeak",
            "unit_price": "29.99",
            "cost": "13.20",
            "stock_quantity": 58,
            "supplier": "NorthPeak Distribution",
            "active": "true",
        },
        {
            "product_id": "P012",
            "sku": "CG-UTL-003",
            "product_name": "Lightweight Outdoor Knife and Fork Set",
            "category": "camping utensils",
            "brand": "SummitLite",
            "unit_price": "15.99",
            "cost": "5.95",
            "stock_quantity": 102,
            "supplier": "Summit Wholesale",
            "active": "true",
        },
    ]

    customers = [
        ["C001", "Emily", "Chen", "emily.chen@example.com", "Los Angeles", "CA", "2026-01-08", "Google Ads"],
        ["C002", "Daniel", "Kim", "daniel.kim@example.com", "San Jose", "CA", "2026-01-12", "Organic Search"],
        ["C003", "Sophia", "Martinez", "sophia.martinez@example.com", "San Diego", "CA", "2026-01-19", "Instagram"],
        ["C004", "Kevin", "Nguyen", "kevin.nguyen@example.com", "Seattle", "WA", "2026-01-23", "Referral"],
        ["C005", "Rachel", "Wong", "rachel.wong@example.com", "Irvine", "CA", "2026-01-30", "Email Campaign"],
        ["C006", "Jason", "Lee", "jason.lee@example.com", "Berkeley", "CA", "2026-02-04", "Organic Search"],
        ["C007", "Mia", "Johnson", "mia.johnson@example.com", "Portland", "OR", "2026-02-10", "Instagram"],
        ["C008", "Brian", "Patel", "brian.patel@example.com", "Fremont", "CA", "2026-02-16", "Google Ads"],
        ["C009", "Olivia", "Garcia", "olivia.garcia@example.com", "Phoenix", "AZ", "2026-02-22", "Referral"],
        ["C010", "Ethan", "Brown", "ethan.brown@example.com", "Sacramento", "CA", "2026-03-01", "Email Campaign"],
        ["C011", "Grace", "Liu", "grace.liu@example.com", "Austin", "TX", "2026-03-05", "Organic Search"],
        ["C012", "Andrew", "Wilson", "andrew.wilson@example.com", "Denver", "CO", "2026-03-09", "Google Ads"],
        ["C013", "Natalie", "Davis", "natalie.davis@example.com", "San Francisco", "CA", "2026-03-15", "Instagram"],
        ["C014", "Ryan", "Taylor", "ryan.taylor@example.com", "Las Vegas", "NV", "2026-03-21", "Referral"],
        ["C015", "Chloe", "Anderson", "chloe.anderson@example.com", "Pasadena", "CA", "2026-03-27", "Email Campaign"],
        ["C016", "Justin", "Moore", "justin.moore@example.com", "Oakland", "CA", "2026-04-02", "Organic Search"],
        ["C017", "Hannah", "Thomas", "hannah.thomas@example.com", "Tucson", "AZ", "2026-04-06", "Instagram"],
        ["C018", "Eric", "White", "eric.white@example.com", "Long Beach", "CA", "2026-04-12", "Google Ads"],
    ]

    customer_rows = [
        {
            "customer_id": customer[0],
            "first_name": customer[1],
            "last_name": customer[2],
            "email": customer[3],
            "city": customer[4],
            "state": customer[5],
            "signup_date": customer[6],
            "acquisition_channel": customer[7],
        }
        for customer in customers
    ]

    product_lookup = {product["product_id"]: product for product in products}
    product_ids = list(product_lookup.keys())
    customer_ids = [customer["customer_id"] for customer in customer_rows]

    orders = []
    order_items = []

    start_date = date(2026, 1, 15)
    status_options = ["completed", "completed", "completed", "completed", "pending", "cancelled", "refunded"]
    payment_methods = ["credit_card", "debit_card", "paypal", "apple_pay"]

    order_item_counter = 1

    for order_number in range(1, 33):
        order_id = f"O{order_number:04d}"
        customer_id = random.choice(customer_ids)
        order_date = start_date + timedelta(days=random.randint(0, 105))
        status = random.choice(status_options)

        selected_products = random.sample(product_ids, random.randint(1, 4))
        subtotal = Decimal("0.00")

        for product_id in selected_products:
            product = product_lookup[product_id]
            quantity = random.randint(1, 3)
            unit_price = money(product["unit_price"])
            line_total = money(unit_price * quantity)
            subtotal += line_total

            order_items.append(
                {
                    "order_item_id": f"OI{order_item_counter:05d}",
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": f"{unit_price:.2f}",
                    "line_total": f"{line_total:.2f}",
                }
            )

            order_item_counter += 1

        subtotal = money(subtotal)
        shipping_fee = Decimal("0.00") if subtotal >= Decimal("75.00") else Decimal("5.99")
        tax = money(subtotal * Decimal("0.095"))
        total = money(subtotal + shipping_fee + tax)

        orders.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "order_date": order_date.isoformat(),
                "status": status,
                "subtotal": f"{subtotal:.2f}",
                "shipping_fee": f"{shipping_fee:.2f}",
                "tax": f"{tax:.2f}",
                "total": f"{total:.2f}",
                "payment_method": random.choice(payment_methods),
            }
        )

    campaigns = [
        {
            "campaign_id": "M001",
            "campaign_name": "Summer Camping Starter Kit",
            "channel": "Google Ads",
            "start_date": "2026-03-01",
            "end_date": "2026-03-21",
            "budget": "1200.00",
            "target_category": "camping utensils",
            "clicks": 1840,
            "conversions": 96,
            "revenue_attributed": "2840.75",
        },
        {
            "campaign_id": "M002",
            "campaign_name": "Backpack Essentials Promo",
            "channel": "Instagram",
            "start_date": "2026-03-10",
            "end_date": "2026-03-31",
            "budget": "900.00",
            "target_category": "camping accessories",
            "clicks": 1425,
            "conversions": 63,
            "revenue_attributed": "1365.20",
        },
        {
            "campaign_id": "M003",
            "campaign_name": "Family Camping Weekend",
            "channel": "Email Campaign",
            "start_date": "2026-04-01",
            "end_date": "2026-04-14",
            "budget": "450.00",
            "target_category": "camping dinnerware",
            "clicks": 760,
            "conversions": 51,
            "revenue_attributed": "2385.50",
        },
        {
            "campaign_id": "M004",
            "campaign_name": "Ultralight Cookware Launch",
            "channel": "Google Ads",
            "start_date": "2026-04-05",
            "end_date": "2026-04-25",
            "budget": "1500.00",
            "target_category": "camping cookware",
            "clicks": 2110,
            "conversions": 88,
            "revenue_attributed": "3520.40",
        },
        {
            "campaign_id": "M005",
            "campaign_name": "Trail Drinkware Refresh",
            "channel": "Organic Search",
            "start_date": "2026-04-12",
            "end_date": "2026-04-30",
            "budget": "300.00",
            "target_category": "camping drinkware",
            "clicks": 980,
            "conversions": 44,
            "revenue_attributed": "1220.65",
        },
        {
            "campaign_id": "M006",
            "campaign_name": "Spring Outdoor Gear Sale",
            "channel": "Instagram",
            "start_date": "2026-04-18",
            "end_date": "2026-05-02",
            "budget": "850.00",
            "target_category": "camping cookware",
            "clicks": 1310,
            "conversions": 57,
            "revenue_attributed": "1988.35",
        },
    ]

    write_csv(
        "sample_products.csv",
        [
            "product_id",
            "sku",
            "product_name",
            "category",
            "brand",
            "unit_price",
            "cost",
            "stock_quantity",
            "supplier",
            "active",
        ],
        products,
    )

    write_csv(
        "sample_customers.csv",
        [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "city",
            "state",
            "signup_date",
            "acquisition_channel",
        ],
        customer_rows,
    )

    write_csv(
        "sample_orders.csv",
        [
            "order_id",
            "customer_id",
            "order_date",
            "status",
            "subtotal",
            "shipping_fee",
            "tax",
            "total",
            "payment_method",
        ],
        orders,
    )

    write_csv(
        "sample_order_items.csv",
        [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
            "line_total",
        ],
        order_items,
    )

    write_csv(
        "sample_marketing_campaigns.csv",
        [
            "campaign_id",
            "campaign_name",
            "channel",
            "start_date",
            "end_date",
            "budget",
            "target_category",
            "clicks",
            "conversions",
            "revenue_attributed",
        ],
        campaigns,
    )

    print("Sample data generated successfully.")
    print(f"Products: {len(products)}")
    print(f"Customers: {len(customer_rows)}")
    print(f"Orders: {len(orders)}")
    print(f"Order items: {len(order_items)}")
    print(f"Marketing campaigns: {len(campaigns)}")
    print(f"Output directory: {DATA_DIR}")


if __name__ == "__main__":
    main()