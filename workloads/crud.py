"""
CRUD Workload Operations
Create (Insert), Read, Update, Delete benchmark execution routines.
"""

import time
import psycopg2
from pymongo import MongoClient

def run_crud_postgres(conn, operation: str, count: int = 1000):
    """Executes CRUD operations in PostgreSQL."""
    cursor = conn.cursor()
    start_time = time.perf_counter()
    rows_affected = 0

    if operation == "create":
        # Insert 'count' synthetic customers
        for i in range(990000, 990000 + count):
            cursor.execute(
                "INSERT INTO customer (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                (i, f"Customer#{i}", "Test Addr", 1, "13-000-000-0000", 100.00, "BUILDING", "Temp CRUD insert")
            )
        conn.commit()
        rows_affected = count

    elif operation == "read":
        # Point read customer by c_custkey
        for i in range(1, count + 1):
            cursor.execute("SELECT * FROM customer WHERE c_custkey = %s;", (i,))
            cursor.fetchall()
        rows_affected = count

    elif operation == "update":
        # Update 1% / fixed batch of customer account balances
        cursor.execute("UPDATE customer SET c_acctbal = c_acctbal + 10.00 WHERE c_custkey <= %s;", (count,))
        conn.commit()
        rows_affected = cursor.rowcount

    elif operation == "delete":
        # Delete inserted batch
        cursor.execute("DELETE FROM customer WHERE c_custkey >= 990000 AND c_custkey < %s;", (990000 + count,))
        conn.commit()
        rows_affected = cursor.rowcount

    end_time = time.perf_counter()
    cursor.close()
    latency_ms = (end_time - start_time) * 1000.0
    throughput = (rows_affected / (end_time - start_time)) if (end_time - start_time) > 0 else 0
    return latency_ms, throughput, rows_affected

def run_crud_mongodb(db, operation: str, count: int = 1000):
    """Executes CRUD operations in MongoDB."""
    start_time = time.perf_counter()
    rows_affected = 0

    if operation == "create":
        docs = [
            {
                "c_custkey": i,
                "c_name": f"Customer#{i}",
                "c_address": "Test Addr",
                "c_nationkey": 1,
                "c_phone": "13-000-000-0000",
                "c_acctbal": 100.00,
                "c_mktsegment": "BUILDING",
                "c_comment": "Temp CRUD insert"
            }
            for i in range(990000, 990000 + count)
        ]
        res = db.customer.insert_many(docs)
        rows_affected = len(res.inserted_ids)

    elif operation == "read":
        for i in range(1, count + 1):
            list(db.customer.find({"c_custkey": i}))
        rows_affected = count

    elif operation == "update":
        res = db.customer.update_many(
            {"c_custkey": {"$lte": count}},
            {"$inc": {"c_acctbal": 10.00}}
        )
        rows_affected = res.modified_count

    elif operation == "delete":
        res = db.customer.delete_many({"c_custkey": {"$gte": 990000, "$lt": 990000 + count}})
        rows_affected = res.deleted_count

    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000.0
    throughput = (rows_affected / (end_time - start_time)) if (end_time - start_time) > 0 else 0
    return latency_ms, throughput, rows_affected
