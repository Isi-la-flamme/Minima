import json
import csv
from datetime import datetime
from pathlib import Path
from minima.core.logger import logger

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def _timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def export_results(results, prefix="results"):
    json_path = EXPORT_DIR / f"{prefix}_{_timestamp()}.json"
    csv_path = EXPORT_DIR / f"{prefix}_{_timestamp()}.csv"

    try:
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(results, jf, ensure_ascii=False, indent=2)
        logger.info(f"JSON export -> {json_path}")

        with open(csv_path, "w", newline="", encoding="utf-8") as cf:
            writer = csv.DictWriter(cf, fieldnames=results[0].keys() if results else [])
            writer.writeheader()
            writer.writerows(results)
        logger.info(f"CSV export -> {csv_path}")
    except Exception as e:
        logger.error(f"Export failed: {e}")# exporter.py
