"""
PostgreSQL Data Loader
Loads generated TPC-H CSV datasets into PostgreSQL using COPY.
"""

import os
import psycopg2
import yaml

TABLE_FILES = [
    ("region", "region.csv"),
    ("nation", "nation.csv"),
    ("supplier", "supplier.csv"),
    ("customer", "customer.csv"),
    ("part", "part.csv"),
    ("partsupp", "partsupp.csv"),
    ("orders", "orders.csv"),
    ("lineitem", "lineitem.csv")
]

def load_postgres_data(data_dir: str, db_config_path: str = "config/database.yaml", schema_path: str = "schemas/postgresql/schema.sql"):
    """Loads CSV files into PostgreSQL database."""
    with open(db_config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)["postgresql"]

    conn = psycopg2.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        dbname=cfg["dbname"]
    )
    cursor = conn.cursor()

    # 1. Execute DDL schema
    print("Executing PostgreSQL DDL Schema...")
    with open(schema_path, "r", encoding="utf-8") as f:
        cursor.execute(f.read())
    conn.commit()

    # 2. Bulk copy CSVs
    for table_name, csv_filename in TABLE_FILES:
        file_path = os.path.join(data_dir, csv_filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        print(f"Loading '{table_name}' into PostgreSQL...")
        with open(file_path, "r", encoding="utf-8") as f:
            cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH (FORMAT csv, DELIMITER ',')", f)
        conn.commit()

    cursor.close()
    conn.close()
    print(f"Successfully loaded all TPC-H datasets from '{data_dir}' into PostgreSQL.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="PostgreSQL TPC-H Loader")
    parser.add_argument("--data-dir", type=str, default="data/raw/sf_0.1", help="Data directory containing CSVs")
    args = parser.parse_args()
    load_postgres_data(args.data_dir)
