import json
import csv
from minima.core.exporter import Exporter

def test_exporter_json(tmp_path):
    exp = Exporter(output_dir=tmp_path)
    data = [{"a": 1, "b": 2}]
    json_path = exp.save_json(data)
    assert json_path.exists()
    assert json.loads(json_path.read_text())[0]["a"] == 1

def test_exporter_csv(tmp_path):
    exp = Exporter(output_dir=tmp_path)
    data = [{"a": 1, "b": 2}]
    csv_path = exp.save_csv(data)
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert rows[0]["a"] == "1"
