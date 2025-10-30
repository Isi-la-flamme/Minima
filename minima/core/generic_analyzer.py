from bs4 import BeautifulSoup
from minima.core.logger import logger

def extract_title(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title else "Untitled"
        return title
    except Exception as e:
        logger.warning(f"Title extraction failed: {e}")
        return "Error"

def analyze_page(url, html):
    return {"url": url, "title": extract_title(html)}# generic_analyzer.py
