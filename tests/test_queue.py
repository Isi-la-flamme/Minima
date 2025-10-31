import json
from minima.core.queue import PersistentQueue

def test_queue_persistence(tmp_path):
    file = tmp_path / "queue.json"
    q = PersistentQueue(file)
    q.add("https://site1.com")
    q.add("https://site2.com")
    q.mark_processed("https://site1.com")
    q.save()

    q2 = PersistentQueue(file)
    assert len(q2.queue) == 1
    assert q2.processed_count == 1
