"""
Q4 Workload: Relational Join Query (High Complexity)
Join customer and orders tables/collections filtered by market segment.
"""

import time

def run_q4_postgres(conn, mktsegment: str = "BUILDING"):
    """PostgreSQL Q4 Relational Join."""
    cursor = conn.cursor()
    start = time.perf_counter()
    cursor.execute(
        "SELECT c.c_custkey, c.c_name, o.o_orderkey, o.o_totalprice, o.o_orderdate "
        "FROM customer c JOIN orders o ON c.c_custkey = o.o_custkey "
        "WHERE c.c_mktsegment = %s;",
        (mktsegment,)
    )
    rows = cursor.fetchall()
    end = time.perf_counter()
    cursor.close()
    return (end - start) * 1000.0, len(rows)

def run_q4_mongodb(db, mktsegment: str = "BUILDING"):
    """MongoDB Q4 $lookup Join."""
    start = time.perf_counter()
    pipeline = [
        {"$match": {"c_mktsegment": mktsegment}},
        {
            "$lookup": {
                "from": "orders",
                "localField": "c_custkey",
                "foreignField": "o_custkey",
                "as": "customer_orders"
            }
        },
        {"$unwind": "$customer_orders"}
    ]
    docs = list(db.customer.aggregate(pipeline))
    end = time.perf_counter()
    return (end - start) * 1000.0, len(docs)
