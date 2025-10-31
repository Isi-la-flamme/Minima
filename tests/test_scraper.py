import requests
from minima.core.scraper import Scraper

class DummyResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

def test_fetch_html_success(monkeypatch):
    def mock_get(url, headers=None, timeout=None):
        return DummyResponse("<html>ok</html>")
    monkeypatch.setattr(requests, "get", mock_get)

    s = Scraper()
    html = s.fetch_html("https://fake.com")
    assert "<html>" in html

def test_fetch_html_failure(monkeypatch):
    def mock_get(url, headers=None, timeout=None):
        raise requests.RequestException("timeout")
    monkeypatch.setattr(requests, "get", mock_get)

    s = Scraper()
    html = s.fetch_html("https://fail.com")
    assert html is None
