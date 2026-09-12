"""
MongoDB Schema and Index Management
"""
from pymongo import MongoClient, ASCENDING, DESCENDING

COLLECTIONS = [
    "region", "nation", "customer", "supplier",
    "part", "partsupp", "orders", "lineitem"
]

def init_mongodb_collections(db):
    """Ensure standard TPC-H collections exist and are clean."""
    existing = db.list_collection_names()
    for col in COLLECTIONS:
        if col not in existing:
            db.create_collection(col)

def apply_mongodb_indexes(db):
    """Apply workload-specific secondary indexes for Condition B (Indexed)."""
    # Q1: Customer lookup on c_custkey
    db.customer.create_index([("c_custkey", ASCENDING)], name="idx_c_custkey")
    
    # Q2: Range query on o_totalprice
    db.orders.create_index([("o_totalprice", ASCENDING)], name="idx_o_totalprice")
    
    # Q3: Compound multi-condition filter on orders
    db.orders.create_index([
        ("o_orderstatus", ASCENDING),
        ("o_orderdate", ASCENDING),
        ("o_totalprice", ASCENDING)
    ], name="idx_orders_multi")
    
    # Q4: Join keys
    db.customer.create_index([("c_mktsegment", ASCENDING)], name="idx_c_mktsegment")
    db.orders.create_index([("o_custkey", ASCENDING)], name="idx_o_custkey")
    
    # Q5: Analytical join and aggregation keys
    db.lineitem.create_index([("l_orderkey", ASCENDING)], name="idx_l_orderkey")
    db.lineitem.create_index([("l_shipdate", ASCENDING)], name="idx_l_shipdate")

def drop_mongodb_indexes(db):
    """Drop secondary indexes for Condition A (Baseline / No workload index)."""
    for col_name in COLLECTIONS:
        col = db[col_name]
        for index_info in col.list_indexes():
            if index_info["name"] != "_id_":
                col.drop_index(index_info["name"])
