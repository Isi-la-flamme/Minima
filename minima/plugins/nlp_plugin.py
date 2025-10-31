from minima.core.plugin_base import BasePlugin
import re

class NLPPlugin(BasePlugin):
    name = "nlp_plugin"

    def process(self, url, content, metadata):
        text = re.sub(r"<[^>]+>", " ", content)
        words = text.split()
        metadata["word_count"] = len(words)
        metadata["unique_words"] = len(set(words))

        self.logger.info(f"[PLUGIN:{self.name}] {url} -> {metadata['word_count']} words")
        return metadata# nlp_plugin.py


def process(url, html):
    return {"plugin_result": f"{__name__} a traité {url}"}
