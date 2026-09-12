"""
Q3 Workload: Multi-Condition Query (Medium Complexity)
Filter orders on o_orderstatus, o_orderdate, and o_totalprice.
"""

import time

def run_q3_postgres(conn, status: str = "O", min_date: str = "1995-01-01", min_price: float = 50000.0):
    """PostgreSQL Q3 Multi-Condition Filter."""
    cursor = conn.cursor()
    start = time.perf_counter()
    cursor.execute(
        "SELECT * FROM orders WHERE o_orderstatus = %s AND o_orderdate >= %s AND o_totalprice > %s;",
        (status, min_date, min_price)
    )
    rows = cursor.fetchall()
    end = time.perf_counter()
    cursor.close()
    return (end - start) * 1000.0, len(rows)

def run_q3_mongodb(db, status: str = "O", min_date: str = "1995-01-01", min_price: float = 50000.0):
    """MongoDB Q3 Multi-Condition Filter."""
    start = time.perf_counter()
    docs = list(db.orders.find({
        "o_orderstatus": status,
        "o_orderdate": {"$gte": min_date},
        "o_totalprice": {"$gt": min_price}
    }))
    end = time.perf_counter()
    return (end - start) * 1000.0, len(docs)
