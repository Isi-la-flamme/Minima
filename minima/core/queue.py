import queue
from minima.core.logger import logger

class TaskQueue:
    def __init__(self):
        self.q = queue.Queue()

    def add(self, item):
        self.q.put(item)
        logger.info(f"Added to queue: {item}")

    def get(self):
        if not self.q.empty():
            return self.q.get()
        return None

    def clear(self):
        with self.q.mutex:
            self.q.queue.clear()
        logger.info("Queue cleared")

    def size(self):
        return self.q.qsize()

    def is_empty(self):
        return self.q.empty()# queue.py
