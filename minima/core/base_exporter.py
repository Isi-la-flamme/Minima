# minima/core/base_exporter.py
from __future__ import annotations
from typing import Iterable, Mapping
from pathlib import Path

class BaseExporter:
    """Interface d'exporteur.

    Implémenter `save_json` et `save_csv`. Doit retourner le Path du fichier créé.
    """
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_json(self, data: Iterable[Mapping], filename: str) -> Path:
        """Sauvegarde JSON. Retourne Path."""
        raise NotImplementedError

    def save_csv(self, data: Iterable[Mapping], filename: str) -> Path:
        """Sauvegarde CSV. Retourne Path."""
        raise NotImplementedError
