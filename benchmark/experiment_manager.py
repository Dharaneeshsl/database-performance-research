"""
Master Experiment Manager
Orchestrates full benchmark matrix execution across database engines, scale factors, workloads, and index strategies.
Saves raw result logs to CSV files.
"""

import os
import csv
import yaml
import psycopg2
from pymongo import MongoClient

from schemas.mongodb.schema import apply_mongodb_indexes, drop_mongodb_indexes
from loaders.generator import generate_tpch_data
from loaders.postgres_loader import load_postgres_data
from loaders.mongo_loader import load_mongo_data
from loaders.validate import validate_datasets
from benchmark.runner import run_workload
from benchmark.metrics import get_postgres_storage, get_mongodb_storage
from workloads.q1_simple import run_q1_postgres, run_q1_mongodb
from workloads.q2_range import run_q2_postgres, run_q2_mongodb
from workloads.q3_multi_condition import run_q3_postgres, run_q3_mongodb
from workloads.q4_join import run_q4_postgres, run_q4_mongodb
from workloads.q5_aggregation import run_q5_postgres, run_q5_mongodb
from workloads.crud import run_crud_postgres, run_crud_mongodb

WORKLOAD_MAP = {
    "q1": (run_q1_postgres, run_q1_mongodb),
    "q2": (run_q2_postgres, run_q2_mongodb),
    "q3": (run_q3_postgres, run_q3_mongodb),
    "q4": (run_q4_postgres, run_q4_mongodb),
    "q5": (run_q5_postgres, run_q5_mongodb)
}

def apply_postgres_indexes(conn, apply: bool):
    """Creates or drops workload indexes in PostgreSQL."""
    cursor = conn.cursor()
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_c_custkey ON customer(c_custkey);",
        "CREATE INDEX IF NOT EXISTS idx_o_totalprice ON orders(o_totalprice);",
        "CREATE INDEX IF NOT EXISTS idx_orders_multi ON orders(o_orderstatus, o_orderdate, o_totalprice);",
        "CREATE INDEX IF NOT EXISTS idx_c_mktsegment ON customer(c_mktsegment);",
        "CREATE INDEX IF NOT EXISTS idx_o_custkey ON orders(o_custkey);",
        "CREATE INDEX IF NOT EXISTS idx_l_orderkey ON lineitem(l_orderkey);",
        "CREATE INDEX IF NOT EXISTS idx_l_shipdate ON lineitem(l_shipdate);"
    ]
    drop_statements = [
        "DROP INDEX IF EXISTS idx_c_custkey;",
        "DROP INDEX IF EXISTS idx_o_totalprice;",
        "DROP INDEX IF EXISTS idx_orders_multi;",
        "DROP INDEX IF EXISTS idx_c_mktsegment;",
        "DROP INDEX IF EXISTS idx_o_custkey;",
        "DROP INDEX IF EXISTS idx_l_orderkey;",
        "DROP INDEX IF EXISTS idx_l_shipdate;"
    ]

    statements = indexes if apply else drop_statements
    for stmt in statements:
        cursor.execute(stmt)
    conn.commit()
    cursor.close()

def run_experiment_matrix(config_path: str = "config/experiment.yaml", db_config_path: str = "config/database.yaml"):
    """Runs master benchmark matrix and writes output CSV files."""
    with open(config_path, "r", encoding="utf-8") as f:
        exp_cfg = yaml.safe_load(f)
    with open(db_config_path, "r", encoding="utf-8") as f:
        db_cfg = yaml.safe_load(f)

    os.makedirs("results/raw", exist_ok=True)
    os.makedirs("results/processed", exist_ok=True)
    os.makedirs("results/figures", exist_ok=True)

    query_csv_path = os.path.join("results/raw", "query_results.csv")
    crud_csv_path = os.path.join("results/raw", "crud_results.csv")
    storage_csv_path = os.path.join("results/raw", "storage_results.csv")

    query_fieldnames = [
        "database", "dataset", "scale_factor", "workload", "index_mode",
        "run", "latency_ms", "throughput", "rows_returned",
        "avg_cpu_percent", "peak_cpu_percent", "avg_memory_mb", "peak_memory_mb"
    ]
    crud_fieldnames = [
        "database", "dataset", "scale_factor", "operation", "index_mode",
        "run", "latency_ms", "throughput", "rows_affected"
    ]
    storage_fieldnames = [
        "database", "dataset", "scale_factor", "index_mode",
        "data_size_mb", "index_size_mb", "total_storage_mb"
    ]

    with open(query_csv_path, "w", newline="", encoding="utf-8") as f_q, \
         open(crud_csv_path, "w", newline="", encoding="utf-8") as f_c, \
         open(storage_csv_path, "w", newline="", encoding="utf-8") as f_s:

        writer_q = csv.DictWriter(f_q, fieldnames=query_fieldnames)
        writer_c = csv.DictWriter(f_c, fieldnames=crud_fieldnames)
        writer_s = csv.DictWriter(f_s, fieldnames=storage_fieldnames)

        writer_q.writeheader()
        writer_c.writeheader()
        writer_s.writeheader()

        # Connect to DBs
        pg_cfg = db_cfg["postgresql"]
        pg_conn = psycopg2.connect(
            host=pg_cfg["host"], port=pg_cfg["port"],
            user=pg_cfg["user"], password=pg_cfg["password"], dbname=pg_cfg["dbname"]
        )

        mg_cfg = db_cfg["mongodb"]
        mg_client = MongoClient(host=mg_cfg["host"], port=mg_cfg["port"])
        mg_db = mg_client[mg_cfg["dbname"]]

        for scale_name, sf_val in exp_cfg["scale_factors"].items():
            print(f"\n==================== SCALE FACTOR: {scale_name.upper()} ({sf_val}) ====================")
            data_dir = f"data/raw/sf_{sf_val}"
            generate_tpch_data(sf_val, data_dir)

            # Load baseline datasets into both DBs
            print("Loading baseline PostgreSQL dataset...")
            load_postgres_data(data_dir)
            print("Loading baseline MongoDB dataset...")
            load_mongo_data(data_dir)
            validate_datasets()

            for idx_mode in exp_cfg["index_modes"]:
                is_indexed = (idx_mode == "indexed")
                print(f"\n--- Indexing Mode: {idx_mode.upper()} ---")

                # Apply/drop indexes
                apply_postgres_indexes(pg_conn, is_indexed)
                if is_indexed:
                    apply_mongodb_indexes(mg_db)
                else:
                    drop_mongodb_indexes(mg_db)

                # Record Storage Footprint
                pg_storage = get_postgres_storage(pg_conn)
                mg_storage = get_mongodb_storage(mg_db)

                writer_s.writerow({
                    "database": "postgresql", "dataset": scale_name, "scale_factor": sf_val,
                    "index_mode": idx_mode, **pg_storage
                })
                writer_s.writerow({
                    "database": "mongodb", "dataset": scale_name, "scale_factor": sf_val,
                    "index_mode": idx_mode, **mg_storage
                })

                # Execute Q1 - Q5 Query Workloads
                for q_id in exp_cfg["workloads"]:
                    if q_id == "crud":
                        continue

                    pg_fn, mg_fn = WORKLOAD_MAP[q_id]
                    print(f"Running Workload {q_id.upper()} on PostgreSQL ({idx_mode})...")
                    pg_res = run_workload(pg_fn, pg_conn, warmup_runs=exp_cfg["warmup_runs"], measurement_runs=exp_cfg["measurement_runs"])
                    for row in pg_res:
                        writer_q.writerow({
                            "database": "postgresql", "dataset": scale_name, "scale_factor": sf_val,
                            "workload": q_id, "index_mode": idx_mode, **row
                        })

                    print(f"Running Workload {q_id.upper()} on MongoDB ({idx_mode})...")
                    mg_res = run_workload(mg_fn, mg_db, warmup_runs=exp_cfg["warmup_runs"], measurement_runs=exp_cfg["measurement_runs"])
                    for row in mg_res:
                        writer_q.writerow({
                            "database": "mongodb", "dataset": scale_name, "scale_factor": sf_val,
                            "workload": q_id, "index_mode": idx_mode, **row
                        })

                # Execute CRUD Workloads
                for op in ["create", "read", "update", "delete"]:
                    print(f"Running CRUD Operation '{op}' on PostgreSQL...")
                    for r_i in range(1, exp_cfg["measurement_runs"] + 1):
                        lat, tp, count = run_crud_postgres(pg_conn, op, count=500)
                        writer_c.writerow({
                            "database": "postgresql", "dataset": scale_name, "scale_factor": sf_val,
                            "operation": op, "index_mode": idx_mode, "run": r_i,
                            "latency_ms": round(lat, 4), "throughput": round(tp, 2), "rows_affected": count
                        })

                    print(f"Running CRUD Operation '{op}' on MongoDB...")
                    for r_i in range(1, exp_cfg["measurement_runs"] + 1):
                        lat, tp, count = run_crud_mongodb(mg_db, op, count=500)
                        writer_c.writerow({
                            "database": "mongodb", "dataset": scale_name, "scale_factor": sf_val,
                            "operation": op, "index_mode": idx_mode, "run": r_i,
                            "latency_ms": round(lat, 4), "throughput": round(tp, 2), "rows_affected": count
                        })

        pg_conn.close()
        mg_client.close()

    print("\n[SUCCESS] Entire Master Benchmark Matrix executed cleanly! Results saved to results/raw/")

if __name__ == "__main__":
    run_experiment_matrix()
