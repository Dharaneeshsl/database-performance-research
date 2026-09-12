"""
High-Precision Execution Timer
"""

import time
from contextlib import contextmanager

class BenchmarkTimer:
    """Timer context manager delivering microsecond accuracy via perf_counter."""
    def __init__(self):
        self.start_time = 0.0
        self.end_time = 0.0
        self.latency_ms = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.latency_ms = (self.end_time - self.start_time) * 1000.0

@contextmanager
def time_execution():
    """Convenience timer generator context manager."""
    start = time.perf_counter()
    metrics = {"latency_ms": 0.0}
    try:
        yield metrics
    finally:
        end = time.perf_counter()
        metrics["latency_ms"] = (end - start) * 1000.0
