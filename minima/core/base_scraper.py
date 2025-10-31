# minima/core/base_scraper.py
from __future__ import annotations
from typing import Optional, Dict, Iterable
from dataclasses import dataclass

@dataclass
class ScrapeResult:
    """Structure légère pour un résultat de scraping."""
    url: str
    content: Optional[str]

class BaseScraper:
    """
    Interface minimaliste pour un scraper.
    Implémenter `fetch(url)` pour récupérer le HTML.
    Optionnel : `fetch_all(urls)` peut être fourni pour parallélisme.
    """
    def __init__(self, timeout: int = 5, retries: int = 3, headers: Dict[str, str] | None = None):
        self.timeout = int(timeout)
        self.retries = int(retries)
        self.headers = headers or {}

    def fetch(self, url: str) -> Optional[str]:
        """Récupère le contenu HTML d'une URL. Retourne None si échec."""
        raise NotImplementedError

    def fetch_all(self, urls: Iterable[str]) -> Dict[str, Optional[str]]:
        """Optionnel : téléchargement parallèle. Retourne mapping url -> content|None."""
        raise NotImplementedError
