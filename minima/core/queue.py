# minima/core/queue.py
import os
import json
from minima.core.logger import logger

class PersistentQueue:
    def __init__(self, path):
        self.path = path
        self.data = {"queue": [], "processed": []}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                logger.info(f"Queue chargée depuis {self.path} ({len(self.data['queue'])} en attente)")
            except Exception as e:
                logger.warning(f"Échec du chargement de la queue: {e}")
        else:
            logger.info(f"Aucune queue trouvée, création d'une nouvelle: {self.path}")
            self._save()

    def _save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la queue: {e}")

    def add(self, item):
        if item not in self.data["queue"] and item not in self.data["processed"]:
            self.data["queue"].append(item)
            logger.info(f"Added to queue: {item}")
            self._save()

    def get(self):
        if self.is_empty():
            return None
        item = self.data["queue"].pop(0)
        self._save()
        return item

    def mark_processed(self, item):
        self.data["processed"].append(item)
        logger.info(f"Marqué comme traité: {item}")
        self._save()

    def is_empty(self):
        return len(self.data["queue"]) == 0

    def clear(self):
        self.data = {"queue": [], "processed": []}
        self._save()
        logger.info("Queue réinitialisée")
