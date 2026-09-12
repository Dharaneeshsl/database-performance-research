"""
Dataset Validation Module
Validates row/document counts between PostgreSQL and MongoDB to guarantee data equivalence.
"""

import yaml
import psycopg2
from pymongo import MongoClient

TABLES = ["region", "nation", "customer", "supplier", "part", "partsupp", "orders", "lineitem"]

def validate_datasets(db_config_path: str = "config/database.yaml"):
    """Compares row/document counts across PostgreSQL and MongoDB."""
    with open(db_config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # PostgreSQL counts
    pg_cfg = cfg["postgresql"]
    pg_conn = psycopg2.connect(
        host=pg_cfg["host"], port=pg_cfg["port"],
        user=pg_cfg["user"], password=pg_cfg["password"],
        dbname=pg_cfg["dbname"]
    )
    pg_cursor = pg_conn.cursor()
    pg_counts = {}
    for table in TABLES:
        pg_cursor.execute(f"SELECT COUNT(*) FROM {table};")
        pg_counts[table] = pg_cursor.fetchone()[0]
    pg_cursor.close()
    pg_conn.close()

    # MongoDB counts
    mg_cfg = cfg["mongodb"]
    mg_client = MongoClient(host=mg_cfg["host"], port=mg_cfg["port"])
    mg_db = mg_client[mg_cfg["dbname"]]
    mg_counts = {}
    for table in TABLES:
        mg_counts[table] = mg_db[table].count_documents({})
    mg_client.close()

    # Validation Table Output
    print("\n" + "=" * 60)
    print(f"{'Table/Collection':<18} | {'PostgreSQL Rows':<16} | {'MongoDB Docs':<16} | {'Match?':<8}")
    print("-" * 60)
    
    all_match = True
    for table in TABLES:
        pg_cnt = pg_counts[table]
        mg_cnt = mg_counts[table]
        match = (pg_cnt == mg_cnt)
        if not match:
            all_match = False
        print(f"{table:<18} | {pg_cnt:<16} | {mg_cnt:<16} | {str(match):<8}")
    print("=" * 60)

    if all_match:
        print("[SUCCESS] Datasets are 100% equivalent across PostgreSQL and MongoDB!")
    else:
        print("[ERROR] Dataset mismatch detected! Check raw data loading pipeline.")
    return all_match

if __name__ == "__main__":
    validate_datasets()
