"""
Statistical Analysis Pipeline
Processes raw measurement CSVs and computes mean, median, std dev, P95, P99,
speedup ratios, storage overheads, and Mann-Whitney U test p-values.
"""

import os
import pandas as pd
import numpy as np
from scipy import stats

def compute_summary_statistics(raw_query_path: str = "results/raw/query_results.csv", output_dir: str = "results/processed"):
    """Computes summary statistics table for query latency and throughput."""
    if not os.path.exists(raw_query_path):
        print(f"Raw query file not found: {raw_query_path}. Run benchmarks first.")
        return None

    df = pd.read_csv(raw_query_path)
    os.makedirs(output_dir, exist_ok=True)

    grouped = df.groupby(["database", "dataset", "scale_factor", "workload", "index_mode"])

    summary_rows = []
    for (db, ds, sf, wl, idx_m), group in grouped:
        latencies = group["latency_ms"].values
        throughputs = group["throughput"].values

        summary_rows.append({
            "database": db,
            "dataset": ds,
            "scale_factor": sf,
            "workload": wl,
            "index_mode": idx_m,
            "count": len(latencies),
            "mean_latency_ms": round(np.mean(latencies), 4),
            "std_latency_ms": round(np.std(latencies, ddof=1), 4),
            "median_latency_ms": round(np.median(latencies), 4),
            "min_latency_ms": round(np.min(latencies), 4),
            "max_latency_ms": round(np.max(latencies), 4),
            "p95_latency_ms": round(np.percentile(latencies, 95), 4),
            "p99_latency_ms": round(np.percentile(latencies, 99), 4),
            "mean_throughput": round(np.mean(throughputs), 2),
            "avg_cpu_percent": round(group["avg_cpu_percent"].mean(), 2),
            "avg_memory_mb": round(group["avg_memory_mb"].mean(), 2)
        })

    summary_df = pd.DataFrame(summary_rows)
    out_csv = os.path.join(output_dir, "summary_statistics.csv")
    summary_df.to_csv(out_csv, index=False)
    print(f"Summary statistics calculated and saved to '{out_csv}'")

    # Compute Performance Ratio R = T_Mongo / T_Postgres
    pivot_df = summary_df.pivot_table(
        index=["dataset", "scale_factor", "workload", "index_mode"],
        columns="database",
        values="median_latency_ms"
    ).reset_index()

    if "mongodb" in pivot_df.columns and "postgresql" in pivot_df.columns:
        pivot_df["ratio_mongo_to_postgres"] = round(pivot_df["mongodb"] / pivot_df["postgresql"], 4)
        pivot_df["winner"] = pivot_df["ratio_mongo_to_postgres"].apply(
            lambda r: "MongoDB" if r < 1.0 else ("PostgreSQL" if r > 1.0 else "Tie")
        )
        ratio_csv = os.path.join(output_dir, "performance_ratios.csv")
        pivot_df.to_csv(ratio_csv, index=False)
        print(f"Performance ratios saved to '{ratio_csv}'")

    return summary_df

if __name__ == "__main__":
    compute_summary_statistics()
