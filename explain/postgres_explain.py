"""
PostgreSQL EXPLAIN ANALYZE Diagnostic Collector
Parses EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) tree output.
"""

import json

def analyze_postgres_query(conn, sql_query: str, params: tuple = ()):
    """Executes EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) and extracts execution plan statistics."""
    cursor = conn.cursor()
    explain_sql = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {sql_query}"
    cursor.execute(explain_sql, params)
    raw_json = cursor.fetchone()[0]
    cursor.close()

    plan_root = raw_json[0]["Plan"]
    planning_time = raw_json[0].get("Planning Time", 0.0)
    execution_time = raw_json[0].get("Execution Time", 0.0)

    node_type = plan_root.get("Node Type", "Unknown")
    shared_hit = plan_root.get("Shared Hit Blocks", 0)
    shared_read = plan_root.get("Shared Read Blocks", 0)

    return {
        "planningTimeMs": round(planning_time, 4),
        "executionTimeMs": round(execution_time, 4),
        "totalCost": plan_root.get("Total Cost", 0.0),
        "plan_node_type": node_type,
        "shared_hit_blocks": shared_hit,
        "shared_read_blocks": shared_read,
        "actual_rows": plan_root.get("Actual Rows", 0)
    }
