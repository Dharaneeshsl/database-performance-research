"""
Q1 Workload: Equality Lookup (Low Complexity)
Find customer by c_custkey.
"""

import time

def run_q1_postgres(conn, custkey: int = 100):
    """PostgreSQL Q1 Equality Lookup."""
    cursor = conn.cursor()
    start = time.perf_counter()
    cursor.execute("SELECT * FROM customer WHERE c_custkey = %s;", (custkey,))
    rows = cursor.fetchall()
    end = time.perf_counter()
    cursor.close()
    return (end - start) * 1000.0, len(rows)

def run_q1_mongodb(db, custkey: int = 100):
    """MongoDB Q1 Equality Lookup."""
    start = time.perf_counter()
    docs = list(db.customer.find({"c_custkey": custkey}))
    end = time.perf_counter()
    return (end - start) * 1000.0, len(docs)
