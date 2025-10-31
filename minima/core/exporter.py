from __future__ import annotations
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable, Mapping, Any
from minima.core.logger import logger

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def _timestamp() -> str:
    """Retourne un timestamp compact pour nommer les fichiers d’export."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


class Exporter:
    """Gère l’écriture des résultats au format JSON et CSV."""

    def __init__(self, output_dir: Path = EXPORT_DIR) -> None:
        self.output_dir = output_dir

    def save_json(self, data: Iterable[Mapping[str, Any]], filename: str | None = None) -> Path:
        filename = filename or f"results_{_timestamp()}.json"
        path = self.output_dir / filename

        try:
            with open(path, "w", encoding="utf-8") as jf:
                json.dump(list(data), jf, ensure_ascii=False, indent=2)
            logger.info(f"JSON export -> {path}")
        except Exception as e:
            logger.error(f"Export JSON failed: {e}")
            raise
        return path

    def save_csv(self, data: Iterable[Mapping[str, Any]], filename: str | None = None) -> Path:
        filename = filename or f"results_{_timestamp()}.csv"
        path = self.output_dir / filename
        data_list = list(data)

        try:
            if not data_list:
                logger.warning("No results to export in CSV")
                path.touch()
                return path

            with open(path, "w", newline="", encoding="utf-8") as cf:
                writer = csv.DictWriter(cf, fieldnames=data_list[0].keys())
                writer.writeheader()
                writer.writerows(data_list)
            logger.info(f"CSV export -> {path}")
        except Exception as e:
            logger.error(f"Export CSV failed: {e}")
            raise
        return path

    def export_results(self, results: Iterable[Mapping[str, Any]], prefix: str = "results") -> tuple[Path, Path]:
        json_path = self.save_json(results, f"{prefix}_{_timestamp()}.json")
        csv_path = self.save_csv(results, f"{prefix}_{_timestamp()}.csv")
        return json_path, csv_path


# --- Compatibilité rétroactive avec l'ancien appel ---
def export_results(results: Iterable[Mapping[str, Any]], prefix: str = "results") -> tuple[Path, Path]:
    """
    Fonction de compatibilité : exporte les résultats comme avant.
    Utilise la classe Exporter interne.
    """
    exporter = Exporter()
    return exporter.export_results(results, prefix)
