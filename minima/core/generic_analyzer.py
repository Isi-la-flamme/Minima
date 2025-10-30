# minima/core/generic_analyzer.py
from bs4 import BeautifulSoup

class GenericAnalyzer:
    def __init__(self, logger=None):
        self.logger = logger

    def analyze(self, html, url):
        """Analyse basique du contenu HTML"""
        try:
            soup = BeautifulSoup(html, "lxml")
            title = soup.title.string.strip() if soup.title else "Sans titre"
            links = [a.get("href") for a in soup.find_all("a", href=True)]
            images = [img.get("src") for img in soup.find_all("img", src=True)]
            result = {
                "url": url,
                "title": title,
                "links": links,
                "images": images,
                "link_count": len(links),
                "image_count": len(images),
            }
            if self.logger:
                self.logger.info(f"Analyse terminée pour {url}")
            return result
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Échec de l’analyse pour {url}: {e}")
            return {"url": url, "error": str(e)}
