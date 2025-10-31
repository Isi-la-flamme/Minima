import os
import hashlib
from pathlib import Path
from minima.core.logger import logger
import importlib.util

PLUGIN_DIR = Path(__file__).parent
HASH_FILE = PLUGIN_DIR / "trusted_hashes.txt"


def sha256sum(path: Path) -> str:
    """Calcule le hash SHA256 d’un fichier."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_trusted_hashes() -> dict[str, str]:
    """Charge les empreintes SHA256 approuvées."""
    trusted = {}
    if not HASH_FILE.exists():
        logger.warning("Fichier trusted_hashes.txt manquant")
        return trusted

    with open(HASH_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                h, path = parts
                normalized_path = os.path.normpath(path)
                trusted[normalized_path] = h
    return trusted


def validate_plugin(plugin_path: Path, trusted: dict[str, str]) -> bool:
    """Valide un seul plugin par empreinte SHA256."""
    digest = sha256sum(plugin_path)
    rel_path = os.path.normpath(str(plugin_path))

    if any(digest == h for h in trusted.values()):
        logger.info(f"Plugin approuvé: {plugin_path.name}")
        return True

    logger.warning(f"Plugin rejeté (signature inconnue): {plugin_path.name}")
    return False


def validate_plugins() -> list[Path]:
    """Retourne la liste des plugins valides."""
    trusted = load_trusted_hashes()
    if not trusted:
        logger.warning("Aucune empreinte SHA256 approuvée trouvée")
        return []

    valid_plugins = []
    for plugin in PLUGIN_DIR.glob("*.py"):
        if plugin.name in {"plugin_validator.py", "__init__.py"}:
            continue
        if validate_plugin(plugin, trusted):
            valid_plugins.append(plugin)

    return valid_plugins


def validate_all(plugin_dir):
    valid_plugins = []
    if not os.path.exists(plugin_dir):
        logger.warning(f"Dossier plugins introuvable: {plugin_dir}")
        return valid_plugins

    with open(os.path.join(plugin_dir, "trusted_hashes.txt"), "r", encoding="utf-8") as f:
        trusted = [line.strip().split()[0] for line in f if line.strip()]

    approved_count = 0
    total = 0

    for file in Path(plugin_dir).glob("*.py"):
        if file.name in {"plugin_validator.py", "__init__.py"}:
            continue  # on ignore ces fichiers internes

        total += 1
        sha = hashlib.sha256(open(file, "rb").read()).hexdigest()
        if sha not in trusted:
            logger.warning(f"Plugin rejeté (signature inconnue): {file.name}")
            continue
        logger.info(f"Plugin approuvé: {file.name}")
        approved_count += 1
        spec = importlib.util.spec_from_file_location(file.stem, file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        setattr(mod, "__name__", file.stem)
        valid_plugins.append(mod)


    logger.info(f"Validation plugins: {approved_count}/{total} approuvés")
    return valid_plugins

def process(url, html):
    return {"plugin_result": f"{__name__} a traité {url}"}
