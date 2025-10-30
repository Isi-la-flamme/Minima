import yaml
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from minima.core.logger import logger
from minima.core.errors import ConfigError

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
_config = {}


def load_config():
    """Charge la configuration YAML principale."""
    global _config
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            _config = yaml.safe_load(f) or {}
            logger.info(f"Configuration chargée depuis {CONFIG_PATH}")
    except FileNotFoundError:
        logger.warning(f"Fichier de configuration introuvable: {CONFIG_PATH}")
        _config = {}
    except yaml.YAMLError as e:
        raise ConfigError(f"Erreur YAML dans {CONFIG_PATH}: {e}")
    return _config


def get(key, default=None):
    """Récupère une clé de configuration."""
    return _config.get(key, default)


def ensure_paths():
    """Vérifie et crée les dossiers essentiels si manquants."""
    required_dirs = ["data", "logs", "exports"]
    for d in required_dirs:
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
            logger.info(f"Répertoire créé: {d}")
        else:
            logger.debug(f"Répertoire présent: {d}")


class ConfigWatcher(FileSystemEventHandler):
    """Surveille les modifications du fichier de configuration."""
    def __init__(self, path):
        self.path = path

    def on_modified(self, event):
        if event.src_path.endswith("config.yaml"):
            logger.info("Fichier de configuration modifié. Rechargement...")
            load_config()


def start_config_watcher():
    """Démarre le watcher sur le fichier de config."""
    event_handler = ConfigWatcher(CONFIG_PATH)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(CONFIG_PATH), recursive=False)
    observer.start()
    logger.info(f"ConfigWatcher actif sur {CONFIG_PATH}")
    return observer
