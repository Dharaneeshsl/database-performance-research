"""
Database Metrics Collector
Measures exact data size, index size, and total storage footprint for PostgreSQL and MongoDB.
"""

import psycopg2
from pymongo import MongoClient

def get_postgres_storage(conn):
    """Retrieves PostgreSQL table size, index size, and total database size in MB."""
    cursor = conn.cursor()
    cursor.execute("SELECT pg_database_size(current_database());")
    total_db_bytes = cursor.fetchone()[0]

    cursor.execute("""
        SELECT 
            sum(pg_relation_size(c.oid)) as data_bytes,
            sum(pg_indexes_size(c.oid)) as index_bytes
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'public' AND c.relkind = 'r';
    """)
    res = cursor.fetchone()
    data_bytes = res[0] or 0
    index_bytes = res[1] or 0
    cursor.close()

    return {
        "data_size_mb": round(data_bytes / (1024 * 1024), 2),
        "index_size_mb": round(index_bytes / (1024 * 1024), 2),
        "total_storage_mb": round(total_db_bytes / (1024 * 1024), 2)
    }

def get_mongodb_storage(db):
    """Retrieves MongoDB data size, index size, and total storage footprint in MB."""
    stats = db.command("dbStats")
    data_bytes = stats.get("dataSize", 0)
    index_bytes = stats.get("indexSize", 0)
    total_bytes = stats.get("storageSize", 0) + index_bytes

    return {
        "data_size_mb": round(data_bytes / (1024 * 1024), 2),
        "index_size_mb": round(index_bytes / (1024 * 1024), 2),
        "total_storage_mb": round(total_bytes / (1024 * 1024), 2)
    }
