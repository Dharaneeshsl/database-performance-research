"""
TPC-H Pure-Python Data Generator
Generates reproducible synthetic TPC-H datasets matching standard TPC-H schema and cardinalities.
Cardinality formulas:
- Region: 5 fixed rows
- Nation: 25 fixed rows
- Supplier: 10,000 * SF rows
- Customer: 150,000 * SF rows
- Part: 200,000 * SF rows
- PartSupp: 800,000 * SF rows
- Orders: 1,500,000 * SF rows
- Lineitem: ~6,000,000 * SF rows (~4 lineitems per order)
"""

import os
import csv
import random
from datetime import datetime, timedelta

REGIONS = ["AFRICA", "AMERICA", "ASIA", "EUROPE", "MIDDLE EAST"]
NATIONS = [
    (0, "ALGERIA", 0), (1, "ARGENTINA", 1), (2, "BRAZIL", 1), (3, "CANADA", 1),
    (4, "EGYPT", 4), (5, "ETHIOPIA", 0), (6, "FRANCE", 3), (7, "GERMANY", 3),
    (8, "INDIA", 2), (9, "INDONESIA", 2), (10, "IRAN", 4), (11, "IRAQ", 4),
    (12, "ITALY", 3), (13, "JAPAN", 2), (14, "JORDAN", 4), (15, "KENYA", 0),
    (16, "MOROCCO", 0), (17, "MOZAMBIQUE", 0), (18, "PERU", 1), (19, "CHINA", 2),
    (20, "ROMANIA", 3), (21, "SAUDI ARABIA", 4), (22, "VIETNAM", 2),
    (23, "RUSSIA", 3), (24, "UNITED STATES", 1)
]
MKTSEGMENTS = ["AUTOMOBILE", "BUILDING", "FURNITURE", "MACHINERY", "HOUSEHOLD"]
ORDER_PRIORITIES = ["1-URGENT", "2-HIGH", "3-MEDIUM", "4-NOT SPECIFIED", "5-LOW"]
ORDER_STATUSES = ["F", "O", "P"]
SHIP_INSTRUCTS = ["DELIVER IN PERSON", "COLLECT COD", "NONE", "TAKE BACK RETURN"]
SHIP_MODES = ["REG AIR", "AIR", "RAIL", "SHIP", "TRUCK", "MAIL", "FOB"]

def generate_tpch_data(scale_factor: float, output_dir: str):
    """Generates TPC-H CSV datasets for a given scale factor."""
    random.seed(42 + int(scale_factor * 100))
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating TPC-H datasets for Scale Factor {scale_factor} into '{output_dir}'...")

    # 1. Region
    region_file = os.path.join(output_dir, "region.csv")
    with open(region_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for i, name in enumerate(REGIONS):
            writer.writerow([i, name, f"Comment for region {name}"])

    # 2. Nation
    nation_file = os.path.join(output_dir, "nation.csv")
    with open(nation_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for nid, name, rid in NATIONS:
            writer.writerow([nid, name, rid, f"Comment for nation {name}"])

    # 3. Supplier (10,000 * SF)
    n_suppliers = max(5, int(10000 * scale_factor))
    supplier_file = os.path.join(output_dir, "supplier.csv")
    with open(supplier_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for i in range(1, n_suppliers + 1):
            writer.writerow([
                i, f"Supplier#{i:09d}", f"Addr#{i}", random.randint(0, 24),
                f"15-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
                round(random.uniform(-999.99, 9999.99), 2), f"Comment supplier {i}"
            ])

    # 4. Customer (150,000 * SF)
    n_customers = max(10, int(150000 * scale_factor))
    customer_file = os.path.join(output_dir, "customer.csv")
    with open(customer_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for i in range(1, n_customers + 1):
            writer.writerow([
                i, f"Customer#{i:09d}", f"Address#{i}", random.randint(0, 24),
                f"13-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
                round(random.uniform(-999.99, 9999.99), 2), random.choice(MKTSEGMENTS), f"Comment cust {i}"
            ])

    # 5. Part (200,000 * SF)
    n_parts = max(10, int(200000 * scale_factor))
    part_file = os.path.join(output_dir, "part.csv")
    with open(part_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for i in range(1, n_parts + 1):
            writer.writerow([
                i, f"Part #{i}", f"Manufacturer#{random.randint(1,5)}", f"Brand#{random.randint(1,5)}",
                "STANDARD POLISHED", random.randint(1, 50), "JUMBO PKG",
                round(random.uniform(1.00, 2000.00), 2), f"Part comment {i}"
            ])

    # 6. PartSupp (4 suppliers per part)
    partsupp_file = os.path.join(output_dir, "partsupp.csv")
    with open(partsupp_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for pkey in range(1, n_parts + 1):
            supps = random.sample(range(1, n_suppliers + 1), min(4, n_suppliers))
            for skey in supps:
                writer.writerow([
                    pkey, skey, random.randint(1, 9999),
                    round(random.uniform(1.00, 1000.00), 2), f"Comment partsupp {pkey}-{skey}"
                ])

    # 7 & 8. Orders (1,500,000 * SF) & Lineitem (~4 items per order)
    n_orders = max(15, int(1500000 * scale_factor))
    orders_file = os.path.join(output_dir, "orders.csv")
    lineitem_file = os.path.join(output_dir, "lineitem.csv")

    base_date = datetime(1992, 1, 1)
    with open(orders_file, "w", newline="", encoding="utf-8") as f_ord, \
         open(lineitem_file, "w", newline="", encoding="utf-8") as f_item:
        writer_ord = csv.writer(f_ord)
        writer_item = csv.writer(f_item)

        for okey in range(1, n_orders + 1):
            custkey = random.randint(1, n_customers)
            ord_date = base_date + timedelta(days=random.randint(0, 2400))
            ord_date_str = ord_date.strftime("%Y-%m-%d")
            total_price = 0.0
            
            n_lineitems = random.randint(1, 7)
            lineitems_data = []

            for lnum in range(1, n_lineitems + 1):
                partkey = random.randint(1, n_parts)
                suppkey = random.randint(1, n_suppliers)
                qty = float(random.randint(1, 50))
                price = round(qty * random.uniform(10.0, 100.0), 2)
                disc = round(random.uniform(0.00, 0.10), 2)
                tax = round(random.uniform(0.00, 0.08), 2)
                ship_date = ord_date + timedelta(days=random.randint(1, 120))
                commit_date = ord_date + timedelta(days=random.randint(30, 90))
                receipt_date = ship_date + timedelta(days=random.randint(1, 30))
                
                total_price += price * (1 - disc) * (1 + tax)
                
                lineitems_data.append([
                    okey, partkey, suppkey, lnum, qty, price, disc, tax,
                    random.choice(["R", "A", "N"]), random.choice(["O", "F"]),
                    ship_date.strftime("%Y-%m-%d"), commit_date.strftime("%Y-%m-%d"),
                    receipt_date.strftime("%Y-%m-%d"), random.choice(SHIP_INSTRUCTS),
                    random.choice(SHIP_MODES), f"Lineitem comment {okey}-{lnum}"
                ])

            writer_ord.writerow([
                okey, custkey, random.choice(ORDER_STATUSES), round(total_price, 2),
                ord_date_str, random.choice(ORDER_PRIORITIES), f"Clerk#{random.randint(1,1000):09d}",
                0, f"Comment order {okey}"
            ])

            for item in lineitems_data:
                writer_item.writerow(item)

    print(f"Data generation complete for SF {scale_factor}. Files saved to {output_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TPC-H Pure Python Generator")
    parser.add_argument("--scale-factor", type=float, default=0.1, help="TPC-H Scale Factor")
    parser.add_argument("--output-dir", type=str, default="data/raw/sf_0.1", help="Output directory")
    args = parser.parse_args()
    generate_tpch_data(args.scale_factor, args.output_dir)
