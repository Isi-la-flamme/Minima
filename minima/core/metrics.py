import time
from minima.core.logger import logger

class Metrics:
    def __init__(self):
        self.start_time = time.time()
        self.total = 0
        self.success = 0
        self.fail = 0
        self.total_bytes = 0
        self.latencies = []

    def record(self, success, size, latency):
        self.total += 1
        self.total_bytes += size
        self.latencies.append(latency)
        if success:
            self.success += 1
        else:
            self.fail += 1

    def summary(self):
        elapsed = time.time() - self.start_time
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        rps = self.success / elapsed if elapsed > 0 else 0
        return {
            "processed": self.total,
            "success": self.success,
            "fail": self.fail,
            "rps": round(rps, 2),
            "avg_latency": round(avg_latency, 3),
            "total_bytes": self.total_bytes
        }

    def log_summary(self):
        s = self.summary()
        logger.info(f"Metrics summary: processed={s['processed']} success={s['success']} "
                    f"fail={s['fail']} rps={s['rps']} avg_latency={s['avg_latency']}s total_bytes={s['total_bytes']}")
