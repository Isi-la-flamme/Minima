import os
import time
import yaml
from minima.core.logger import logger
from minima.core.queue import PersistentQueue
from minima.core.scraper import Scraper
from minima.core.generic_analyzer import GenericAnalyzer
from minima.core.exporter import Exporter
from minima.core.config_loader import ensure_paths
from minima.core.errors import MinimaError

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/config.yaml"))
QUEUE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/queue.json"))


def load_config():
    logger.info(f"Tentative de chargement du fichier de config: {CONFIG_PATH}")
    if not os.path.exists(CONFIG_PATH):
        logger.warning(f"Fichier de configuration introuvable: {CONFIG_PATH}")
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        logger.info(f"Configuration chargée ({len(cfg)} clés)")
        return cfg
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la configuration: {e}")
        return {}


def main():
    logger.info("=== DÉMARRAGE MINIMA v0.9 (Phase 4) ===")

    try:
        ensure_paths()
        cfg = load_config()

        urls = cfg.get("urls", [])
        delay = cfg.get("delay", 0)

        logger.info(f"Initialisation de la file persistante: {QUEUE_PATH}")
        os.makedirs(os.path.dirname(QUEUE_PATH), exist_ok=True)
        queue = PersistentQueue(QUEUE_PATH)

        scraper = Scraper()             # headers gérés automatiquement par config_loader
        analyzer = GenericAnalyzer(logger=logger)
        exporter = Exporter()
        results = []

        # Initialisation de la queue
        if queue.is_empty():
            logger.info("Queue vide au démarrage")
            if urls:
                logger.info(f"Ajout de {len(urls)} URLs depuis config.yaml")
                for url in urls:
                    queue.add(url)
            else:
                logger.warning("Aucune URL définie dans la configuration")

        logger.info("Début du traitement des URLs")
        urls_to_fetch = queue.remaining_urls()

        if not urls_to_fetch:
            logger.warning("Aucune URL à traiter")
            return

        html_map = scraper.fetch_all(urls_to_fetch)

        for url, html in html_map.items():
            if not html:
                logger.warning(f"Contenu vide ou échec pour {url}")
                continue

            result = analyzer.analyze(html, url)
            results.append(result)
            queue.mark_processed(url)
            logger.info(f"Analyse terminée pour {url}")

            if delay > 0:
                logger.info(f"Pause de {delay}s avant la prochaine URL")
                time.sleep(delay)

        if results:
            logger.info(f"Exportation de {len(results)} résultats")
            exporter.export_results(results)
        else:
            logger.warning("Aucun résultat à exporter")

        logger.info("=== FIN DU PIPELINE MINIMA ===")

    except MinimaError as e:
        logger.error(f"Erreur Minima détectée: {e}")
    except Exception as e:
        logger.exception(f"Erreur critique non gérée: {e}")


if __name__ == "__main__":
    main()
