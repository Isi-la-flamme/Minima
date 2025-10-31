# minima/core/base_plugin.py
from __future__ import annotations
from typing import Any, Dict, Optional, Protocol

class PluginInterface(Protocol):
    """Interface minimale pour un plugin Minima."""
    name: str

    def setup(self, config: Dict[str, Any]) -> None:
        """Initialisation du plugin avec la configuration."""
        ...

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Processus principal du plugin. Retourne un dict enrichi."""
        ...

class BasePlugin:
    """Classe de base pour les plugins.

    Hériter de cette classe et surcharger `process`.
    """
    name: str = "base"

    def setup(self, config: Dict[str, Any]) -> None:
        self.config = config

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return payload
