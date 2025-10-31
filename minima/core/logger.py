import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os
import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.yaml"

def setup_logger():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    else:
        cfg = {}

    log_path = Path(cfg.get("log_path", "logs/minima.log"))
    log_path.parent.mkdir(parents=True, exist_ok=True)
    max_bytes = int(cfg.get("log_max_bytes", 1048576))
    backup_count = int(cfg.get("log_backup_count", 5))

    handler = RotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    root_logger = logging.getLogger("minima")
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    root_logger.addHandler(console)
    return root_logger

logger = setup_logger()# logger.py
def get_logger(name=None):
    return logging.getLogger("minima" if name is None else name)
