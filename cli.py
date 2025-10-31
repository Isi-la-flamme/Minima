import typer
from minima.main import main
from minima.plugins.plugin_validator import validate_all

app = typer.Typer(help="CLI officielle de Minima")

@app.command()
def run(config: str = typer.Option("config/config.yaml", "--config", help="Chemin du fichier de configuration")):
    """Exécute le pipeline principal."""
    main(config_path=config)

@app.command()
def plugins_list():
    """Liste les plugins valides."""
    from minima.plugins.plugin_validator import PLUGIN_DIR
    valid = validate_all(PLUGIN_DIR)
    for p in valid:
        print(p.__name__)

@app.command()
def queue_status():
    """Affiche l’état de la file persistante."""
    import json, os
    path = "data/queue.json"
    if not os.path.exists(path):
        print("Queue introuvable.")
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"{len(data)} éléments en file.")
    for item in data:
        print("-", item.get("url"))
