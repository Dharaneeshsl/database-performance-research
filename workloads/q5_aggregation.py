"""
Q5 Workload: Complex Analytical Aggregation Query (Very High Complexity)
Orders ⋈ Lineitem + Filter on shipdate + GROUP BY orderpriority + SUM revenue + SORT.
"""

import time

def run_q5_postgres(conn, min_shipdate: str = "1994-01-01", max_shipdate: str = "1995-01-01"):
    """PostgreSQL Q5 Complex Aggregation."""
    cursor = conn.cursor()
    start = time.perf_counter()
    cursor.execute(
        "SELECT o.o_orderpriority, COUNT(*) as order_count, SUM(l.l_extendedprice * (1 - l.l_discount)) as total_revenue "
        "FROM orders o JOIN lineitem l ON o.o_orderkey = l.l_orderkey "
        "WHERE l.l_shipdate >= %s AND l.l_shipdate < %s "
        "GROUP BY o.o_orderpriority ORDER BY total_revenue DESC;",
        (min_shipdate, max_shipdate)
    )
    rows = cursor.fetchall()
    end = time.perf_counter()
    cursor.close()
    return (end - start) * 1000.0, len(rows)

def run_q5_mongodb(db, min_shipdate: str = "1994-01-01", max_shipdate: str = "1995-01-01"):
    """MongoDB Q5 Complex Aggregation Pipeline."""
    start = time.perf_counter()
    pipeline = [
        {
            "$lookup": {
                "from": "lineitem",
                "localField": "o_orderkey",
                "foreignField": "l_orderkey",
                "as": "items"
            }
        },
        {"$unwind": "$items"},
        {
            "$match": {
                "items.l_shipdate": {"$gte": min_shipdate, "$lt": max_shipdate}
            }
        },
        {
            "$group": {
                "_id": "$o_orderpriority",
                "order_count": {"$sum": 1},
                "total_revenue": {
                    "$sum": {
                        "$multiply": [
                            "$items.l_extendedprice",
                            {"$subtract": [1, "$items.l_discount"]}
                        ]
                    }
                }
            }
        },
        {"$sort": {"total_revenue": -1}}
    ]
    docs = list(db.orders.aggregate(pipeline))
    end = time.perf_counter()
    return (end - start) * 1000.0, len(docs)
