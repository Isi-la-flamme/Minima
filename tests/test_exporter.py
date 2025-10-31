import os
import json
import csv
from minima.core.exporter import export_results, EXPORT_DIR

def test_export_json_and_csv(tmp_path):
    results = [{"url": "https://example.com", "status": "ok"}]
    export_results(results, prefix="test_export")

    files = list(EXPORT_DIR.glob("test_export_*.json"))
    assert files, "JSON export manquant"
    json_file = files[-1]
    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)
    assert data == results

    csv_files = list(EXPORT_DIR.glob("test_export_*.csv"))
    assert csv_files, "CSV export manquant"
    with open(csv_files[-1], encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert rows[0]["url"] == "https://example.com"
