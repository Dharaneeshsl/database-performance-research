"""
Single Workload Runner
Manages warm-up runs (3 repetitions) and measured runs (10 repetitions) for a given workload.
"""

import time
from benchmark.system_monitor import SystemMonitor

def run_workload(workload_fn, conn_or_db, warmup_runs: int = 3, measurement_runs: int = 10, **kwargs):
    """
    Executes warmup and measurement runs for a workload function.
    Returns list of dict results per run.
    """
    # 1. Warm-up runs (unmeasured/discarded)
    for _ in range(warmup_runs):
        workload_fn(conn_or_db, **kwargs)

    # 2. Measurement runs
    results = []
    monitor = SystemMonitor()

    for run_idx in range(1, measurement_runs + 1):
        monitor.start()
        latency_ms, rows_count = workload_fn(conn_or_db, **kwargs)
        res_metrics = monitor.stop()

        throughput = (rows_count / (latency_ms / 1000.0)) if latency_ms > 0 else 0.0

        results.append({
            "run": run_idx,
            "latency_ms": round(latency_ms, 4),
            "throughput": round(throughput, 2),
            "rows_returned": rows_count,
            "avg_cpu_percent": res_metrics["avg_cpu_percent"],
            "peak_cpu_percent": res_metrics["peak_cpu_percent"],
            "avg_memory_mb": res_metrics["avg_memory_mb"],
            "peak_memory_mb": res_metrics["peak_memory_mb"]
        })

    return results
