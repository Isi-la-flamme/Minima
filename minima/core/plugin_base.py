# minima/core/plugin_base.py
class BasePlugin:
    """Classe de base pour tous les plugins Minima."""

    name = "UnnamedPlugin"
    version = "1.0"

    def process(self, url: str, html: str) -> dict | None:
        """Méthode à surcharger par les plugins."""
        raise NotImplementedError("La méthode process() doit être implémentée dans le plugin.")
