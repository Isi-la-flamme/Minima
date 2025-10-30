import time

class Metrics:
    def __init__(self):
        self.start_time = time.time()
        self.processed = 0
        self.success = 0
        self.fail = 0
        self.total_bytes = 0
        self.latencies = []

    def record(self, success: bool, latency: float, size: int = 0):
        self.processed += 1
        if success:
            self.success += 1
        else:
            self.fail += 1
        self.total_bytes += size
        self.latencies.append(latency)

    def summary(self):
        elapsed = time.time() - self.start_time
        rps = self.processed / elapsed if elapsed > 0 else 0
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        return {
            "processed": self.processed,
            "success": self.success,
            "fail": self.fail,
            "rps": round(rps, 2),
            "avg_latency": round(avg_latency, 3),
            "total_bytes": self.total_bytes,
        }
