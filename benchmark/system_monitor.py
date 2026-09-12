"""
System Resource Monitor Thread
Monitors CPU % and RAM footprint during workload execution.
"""

import time
import threading
import psutil

class SystemMonitor:
    def __init__(self, interval: float = 0.05):
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread = None
        self.cpu_samples = []
        self.memory_samples = []

    def _monitor(self):
        process = psutil.Process()
        while not self._stop_event.is_set():
            cpu = psutil.cpu_percent(interval=None)
            mem = process.memory_info().rss / (1024 * 1024) # MB
            self.cpu_samples.append(cpu)
            self.memory_samples.append(mem)
            time.sleep(self.interval)

    def start(self):
        self.cpu_samples.clear()
        self.memory_samples.clear()
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._monitor, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1.0)
        
        avg_cpu = sum(self.cpu_samples) / len(self.cpu_samples) if self.cpu_samples else 0.0
        peak_cpu = max(self.cpu_samples) if self.cpu_samples else 0.0
        avg_mem = sum(self.memory_samples) / len(self.memory_samples) if self.memory_samples else 0.0
        peak_mem = max(self.memory_samples) if self.memory_samples else 0.0

        return {
            "avg_cpu_percent": round(avg_cpu, 2),
            "peak_cpu_percent": round(peak_cpu, 2),
            "avg_memory_mb": round(avg_mem, 2),
            "peak_memory_mb": round(peak_mem, 2)
        }
