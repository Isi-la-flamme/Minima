import os
import time
import yaml
import requests

from minima.core.logger import logger
from minima.core.queue import PersistentQueue
from minima.core.generic_analyzer import GenericAnalyzer
from minima.core.exporter import export_results
from minima.core.config_loader import ensure_paths
from minima.core.errors import MinimaError

# Chemin de la configuration
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/config.yaml"))
QUEUE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/queue.json"))


def load_config():
    logger.info(f"Tentative de chargement du fichier de config: {CONFIG_PATH}")
    if not os.path.exists(CONFIG_PATH):
        logger.warning(f"Config file not found: {CONFIG_PATH}")
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        logger.info(f"Configuration chargée avec succès ({len(cfg)} clés)")
        return cfg
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la config: {e}")
        return {}


def fetch_html(url, headers=None, timeout=10):
    logger.info(f"Téléchargement de {url}")
    try:
        response = requests.get(url, headers=headers or {}, timeout=timeout)
        response.raise_for_status()
        logger.info(f"Réponse HTTP {response.status_code} reçue pour {url}")
        return response.text
    except Exception as e:
        logger.warning(f"Fetch failed for {url}: {e}")
        return None


def main():
    logger.info("=== DÉMARRAGE MINIMA v0.9 ===")

    try:
        # Vérifie les répertoires nécessaires
        ensure_paths()

        cfg = load_config()
        headers = cfg.get("headers", {})
        delay = cfg.get("delay", 0)
        urls = cfg.get("urls", [])

        logger.info(f"Initialisation de la file persistante: {QUEUE_PATH}")
        os.makedirs(os.path.dirname(QUEUE_PATH), exist_ok=True)
        queue = PersistentQueue(QUEUE_PATH)
        analyzer = GenericAnalyzer(logger=logger)
        results = []

        # Initialisation de la queue
        if queue.is_empty():
            logger.info("Queue vide au démarrage")
            if urls:
                logger.info(f"Ajout de {len(urls)} URLs depuis config.yaml")
                for u in urls:
                    queue.add(u)
            else:
                logger.warning("Aucune URL dans la configuration")

        logger.info("Début du traitement des URLs")

        while not queue.is_empty():
            url = queue.get()
            if not url:
                logger.warning("Queue.get() a renvoyé None — fin de boucle")
                break

            logger.info(f"Analyse de {url}")
            html = fetch_html(url, headers=headers, timeout=cfg.get("timeout", 10))
            if not html:
                logger.warning(f"Contenu vide ou échec pour {url}")
                continue

            result = analyzer.analyze(html, url)
            results.append(result)
            queue.mark_processed(url)
            logger.info(f"Analyse terminée pour {url}")

            if delay > 0:
                logger.info(f"Pause de {delay}s avant la prochaine requête")
                time.sleep(delay)

        if results:
            logger.info(f"Exportation de {len(results)} résultats")
            export_results(results)
        else:
            logger.warning("Aucun résultat à exporter")

        logger.info("=== FIN DU PIPELINE MINIMA ===")

    except MinimaError as e:
        logger.error(f"Erreur Minima détectée: {e}")
    except Exception as e:
        logger.exception(f"Erreur critique non gérée: {e}")


if __name__ == "__main__":
    main()
