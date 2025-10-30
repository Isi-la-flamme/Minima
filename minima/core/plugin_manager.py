import importlib
import pkgutil
from minima.core.logger import logger

_plugins = []

def load_plugins():
    from minima import plugins
    for _, name, _ in pkgutil.iter_modules(plugins.__path__):
        try:
            module = importlib.import_module(f"minima.plugins.{name}")
            _plugins.append(module)
            logger.info(f"Plugin loaded: {name}")
        except Exception as e:
            logger.warning(f"Failed to load plugin {name}: {e}")

def apply_plugins(url, data):
    for plugin in _plugins:
        if hasattr(plugin, "process"):
            try:
                plugin.process(url, data)
            except Exception as e:
                logger.warning(f"Plugin {plugin.__name__} failed on {url}: {e}")# plugin_manager.py
