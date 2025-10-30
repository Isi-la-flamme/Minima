import requests
from minima.core.config_loader import get
from minima.core.logger import logger

class Scraper:
    def __init__(self):
        self.timeout = int(get("timeout", 5))
        self.retries = int(get("retries", 3))
        self.headers = get("headers", {})

    def fetch_html(self, url):
        for attempt in range(1, self.retries + 1):
            try:
                resp = requests.get(url, headers=self.headers, timeout=self.timeout)
                if resp.status_code == 200:
                    return resp.text
                logger.warning(f"{url} -> HTTP {resp.status_code}")
            except Exception as e:
                logger.warning(f"{url} -> attempt {attempt}/{self.retries} failed: {e}")
        return None# scraper.py
