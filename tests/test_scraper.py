import pytest
from minima.core.scraper import Scraper

def test_scraper_init():
    s = Scraper()
    assert hasattr(s, "fetch_url")

@pytest.mark.parametrize("url", ["https://httpbin.org/get"])
def test_scraper_fetch(url):
    s = Scraper()
    result = s.fetch_url(url)
    assert result is not None
    assert "status_code" in result or "html" in result
