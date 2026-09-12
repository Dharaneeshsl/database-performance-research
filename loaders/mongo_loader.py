"""
MongoDB Data Loader
Converts CSV data into BSON-typed documents and loads into MongoDB.
"""

import os
import csv
import yaml
from pymongo import MongoClient
from schemas.mongodb.schema import init_mongodb_collections

def parse_val(val, target_type):
    """Coerce string CSV value into typed Python value."""
    val = val.strip()
    if target_type == "int":
        return int(val)
    elif target_type == "float":
        return float(val)
    return val

SCHEMA_TYPES = {
    "region": [("r_regionkey", "int"), ("r_name", "str"), ("r_comment", "str")],
    "nation": [("n_nationkey", "int"), ("n_name", "str"), ("n_regionkey", "int"), ("n_comment", "str")],
    "supplier": [("s_suppkey", "int"), ("s_name", "str"), ("s_address", "str"), ("s_nationkey", "int"), ("s_phone", "str"), ("s_acctbal", "float"), ("s_comment", "str")],
    "customer": [("c_custkey", "int"), ("c_name", "str"), ("c_address", "str"), ("c_nationkey", "int"), ("c_phone", "str"), ("c_acctbal", "float"), ("c_mktsegment", "str"), ("c_comment", "str")],
    "part": [("p_partkey", "int"), ("p_name", "str"), ("p_mfgr", "str"), ("p_brand", "str"), ("p_type", "str"), ("p_size", "int"), ("p_container", "str"), ("p_retailprice", "float"), ("p_comment", "str")],
    "partsupp": [("ps_partkey", "int"), ("ps_suppkey", "int"), ("ps_availqty", "int"), ("ps_supplycost", "float"), ("ps_comment", "str")],
    "orders": [("o_orderkey", "int"), ("o_custkey", "int"), ("o_orderstatus", "str"), ("o_totalprice", "float"), ("o_orderdate", "str"), ("o_orderpriority", "str"), ("o_clerk", "str"), ("o_shippriority", "int"), ("o_comment", "str")],
    "lineitem": [("l_orderkey", "int"), ("l_partkey", "int"), ("l_suppkey", "int"), ("l_linenumber", "int"), ("l_quantity", "float"), ("l_extendedprice", "float"), ("l_discount", "float"), ("l_tax", "float"), ("l_returnflag", "str"), ("l_linestatus", "str"), ("l_shipdate", "str"), ("l_commitdate", "str"), ("l_receiptdate", "str"), ("l_shipinstruct", "str"), ("l_shipmode", "str"), ("l_comment", "str")]
}

def load_mongo_data(data_dir: str, db_config_path: str = "config/database.yaml", batch_size: int = 10000):
    """Loads CSV files into MongoDB database."""
    with open(db_config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)["mongodb"]

    client = MongoClient(host=cfg["host"], port=cfg["port"])
    db = client[cfg["dbname"]]

    # Drop existing collections to ensure fresh load
    for col_name in SCHEMA_TYPES.keys():
        db[col_name].drop()
    init_mongodb_collections(db)

    for col_name, fields in SCHEMA_TYPES.items():
        csv_path = os.path.join(data_dir, f"{col_name}.csv")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"File not found: {csv_path}")

        print(f"Loading '{col_name}' into MongoDB...")
        documents = []
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                doc = {}
                for idx, (field_name, field_type) in enumerate(fields):
                    doc[field_name] = parse_val(row[idx], field_type)
                documents.append(doc)

                if len(documents) >= batch_size:
                    db[col_name].insert_many(documents)
                    documents = []

            if documents:
                db[col_name].insert_many(documents)

    client.close()
    print(f"Successfully loaded all TPC-H datasets from '{data_dir}' into MongoDB.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MongoDB TPC-H Loader")
    parser.add_argument("--data-dir", type=str, default="data/raw/sf_0.1", help="Data directory containing CSVs")
    args = parser.parse_args()
    load_mongo_data(args.data_dir)
