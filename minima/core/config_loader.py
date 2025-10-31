# minima/core/config_loader.py
from pathlib import Path
import yaml
import os
from minima.core.logger import logger
from minima.core.errors import ConfigError

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "config.yaml"
_config = {}


def load_config(path: Path = None):
    """Charge la configuration YAML principale."""
    global _config
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            _config = yaml.safe_load(f) or {}
            logger.info(f"Configuration chargée depuis {config_path}")
    except FileNotFoundError:
        logger.warning(f"Fichier de configuration introuvable: {config_path}")
        _config = {}
    except yaml.YAMLError as e:
        raise ConfigError(f"Erreur YAML dans {config_path}: {e}")
    return _config


def get(key, default=None):
    """Récupère une clé de configuration."""
    return _config.get(key, default)


def ensure_paths():
    """Vérifie et crée les dossiers essentiels si manquants."""
    required_dirs = ["data", "logs", "exports"]
    for d in required_dirs:
        path = Path(d)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Répertoire créé: {path}")
        else:
            logger.debug(f"Répertoire présent: {path}")
