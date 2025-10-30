import json
import csv
from pathlib import Path
from minima.core.logger import logger

class Exporter:
    def __init__(self, export_dir="exports", save_mode="incremental"):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self.save_mode = save_mode
        self.results = []

    def save(self, data: dict):
        self.results.append(data)
        if self.save_mode == "incremental":
            self.incremental_save()

    def incremental_save(self):
        json_path = self.export_dir / "results.json"
        csv_path = self.export_dir / "results.csv"

        # JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        # CSV
        if self.results:
            keys = self.results[0].keys()
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.results)

        logger.info(f"INCREMENTAL SAVE -> JSON: {json_path} CSV: {csv_path}")

    def final_sync(self):
        if self.save_mode == "end":
            self.incremental_save()
        logger.info("[INFO] FINAL SYNC complete")
