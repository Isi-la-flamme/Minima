import yaml
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from minima.core.logger import logger

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
_config = {}

def load_config():
    global _config
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            _config = yaml.safe_load(f) or {}
            logger.info(f"Configuration loaded from {CONFIG_PATH}")
    except FileNotFoundError:
        logger.warning(f"Config file not found: {CONFIG_PATH}")
        _config = {}
    return _config

def get(key, default=None):
    return _config.get(key, default)

class ConfigWatcher(FileSystemEventHandler):
    def __init__(self, path):
        self.path = path

    def on_modified(self, event):
        if event.src_path.endswith("config.yaml"):
            logger.info("Config file modified. Reloading...")
            load_config()

def start_config_watcher():
    event_handler = ConfigWatcher(CONFIG_PATH)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(CONFIG_PATH), recursive=False)
    observer.start()
    logger.info(f"ConfigWatcher started on {CONFIG_PATH}")
    return observer# config_loader.py
