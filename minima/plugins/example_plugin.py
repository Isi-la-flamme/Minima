from minima.core.plugin_base import BasePlugin
from bs4 import BeautifulSoup

class ExamplePlugin(BasePlugin):
    name = "example_plugin"

    def process(self, url, content, metadata):
        soup = BeautifulSoup(content, "html.parser")
        title = soup.title.string.strip() if soup.title else "No title"
        metadata["title"] = title

        self.logger.info(f"[PLUGIN:{self.name}] Title: {title}")
        return metadata# example_plugin.py
