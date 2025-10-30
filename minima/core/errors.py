# minima/core/errors.py

class MinimaError(Exception):
    """Base pour toutes les exceptions spécifiques à Minima."""
    pass


class ConfigError(MinimaError):
    """Erreur liée à la configuration (fichier manquant, invalide, etc.)."""
    pass


class NetworkError(MinimaError):
    """Erreur survenue lors d’une requête réseau."""
    pass


class ExportError(MinimaError):
    """Erreur lors de l’exportation des résultats."""
    pass


class QueueError(MinimaError):
    """Erreur dans la gestion de la file persistante."""
    pass
