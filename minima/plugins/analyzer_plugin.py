from minima.core.plugin_base import BasePlugin

class AnalyzerPlugin(BasePlugin):
    name = "analyzer_plugin"

    def process(self, url, content, metadata):
        links = content.count("<a ")
        imgs = content.count("<img ")
        page_size = len(content)

        metadata["links_count"] = links
        metadata["imgs_count"] = imgs
        metadata["page_size_bytes"] = page_size

        self.logger.info(f"[PLUGIN:{self.name}] Analyzed {url} -> links={links}, imgs={imgs}, size={page_size}")
        return metadata# analyzer_plugin.py

def process(url, html):
    return {"plugin_result": f"{__name__} a traité {url}"}
