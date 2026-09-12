"""
Q2 Workload: Range Query (Low-Medium Complexity)
Find orders with o_totalprice within specified numerical range.
"""

import time

def run_q2_postgres(conn, min_price: float = 100000.0, max_price: float = 150000.0):
    """PostgreSQL Q2 Range Filter."""
    cursor = conn.cursor()
    start = time.perf_counter()
    cursor.execute(
        "SELECT * FROM orders WHERE o_totalprice >= %s AND o_totalprice <= %s;",
        (min_price, max_price)
    )
    rows = cursor.fetchall()
    end = time.perf_counter()
    cursor.close()
    return (end - start) * 1000.0, len(rows)

def run_q2_mongodb(db, min_price: float = 100000.0, max_price: float = 150000.0):
    """MongoDB Q2 Range Filter."""
    start = time.perf_counter()
    docs = list(db.orders.find({
        "o_totalprice": {"$gte": min_price, "$lte": max_price}
    }))
    end = time.perf_counter()
    return (end - start) * 1000.0, len(docs)
