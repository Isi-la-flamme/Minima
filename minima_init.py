import os
import subprocess
import sys

# --- Dossiers du projet ---
dirs = [
    "minima/core",
    "minima/plugins",
    "minima/data",
    "config",
    "exports",
    "logs",
]

# --- Fichiers du projet ---
files = [
    "README.md",
    "requirements.txt",
    "setup.py",
    "pyproject.toml",
    "config/config.yaml",
    "minima/__init__.py",
    "minima/main.py",
    "minima/core/__init__.py",
    "minima/core/config_loader.py",
    "minima/core/logger.py",
    "minima/core/plugin_manager.py",
    "minima/core/generic_analyzer.py",
    "minima/core/exporter.py",
    "minima/core/queue.py",
    "minima/core/scraper.py",
    "minima/plugins/__init__.py",
    "minima/plugins/example_plugin.py",
    "minima/plugins/analyzer_plugin.py",
    "minima/plugins/nlp_plugin.py",
]

# --- Création des dossiers ---
for d in dirs:
    os.makedirs(d, exist_ok=True)

# --- Création des fichiers ---
for f in files:
    if not os.path.exists(f):
        with open(f, "w") as fp:
            if f.endswith(".py"):
                fp.write(f"# {os.path.basename(f)}\n")
            elif f.endswith(".yaml"):
                fp.write(
                    """threads: 4
timeout: 5
retries: 3
export_path: "exports"
log_path: "logs/minima.log"
log_max_bytes: 1048576
log_backup_count: 5
save_mode: "incremental"
urls:
  - "https://google.com"
  - "https://wikipedia.org"
  - "https://github.com"

headers:
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
  Accept-Language: en-US,en;q=0.9
  Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
"""
                )
            else:
                fp.write("")

print("✅ Arborescence Minima v0.9 créée avec succès.")

# --- Création du venv ---
if not os.path.exists("venv"):
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    print("✅ Environnement virtuel 'venv' créé.")

# --- Commande d’activation ---
if os.name == "posix":  # Termux / Linux / macOS
    activate_cmd = "source venv/bin/activate"
else:  # Windows
    activate_cmd = "venv\\Scripts\\activate"

print(f"➡️ Pour activer le venv, exécute : {activate_cmd}")
