import os
import json
from minima.core.queue import PersistentQueue

def test_queue_creation(temp_dir):
    path = os.path.join(temp_dir, "queue.json")
    q = PersistentQueue(path)
    assert q.is_empty()
    assert os.path.exists(path)

def test_add_and_get_item(temp_dir):
    path = os.path.join(temp_dir, "queue.json")
    q = PersistentQueue(path)
    q.add("item1")
    assert not q.is_empty()
    item = q.get()
    assert item == "item1"
    assert q.is_empty()

def test_processed_tracking(temp_dir):
    path = os.path.join(temp_dir, "queue.json")
    q = PersistentQueue(path)
    q.add("x")
    item = q.get()
    q.mark_processed(item)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "x" in data["processed"]

def test_clear_queue(temp_dir):
    path = os.path.join(temp_dir, "queue.json")
    q = PersistentQueue(path)
    q.add("a")
    q.clear()
    assert q.is_empty()
