# tests/test_scraper.py
import pytest
from minima.core.scraper import Scraper

class DummyResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code


def test_fetch_html_success(monkeypatch, caplog):
    def mock_get(url, headers=None, timeout=None):
        return DummyResponse("<html>ok</html>", 200)

    monkeypatch.setattr("requests.get", mock_get)
    s = Scraper()
    html = s.fetch_html("https://example.com")

    assert "<html>" in html
    assert any("Fetched https://example.com" in msg for msg in caplog.text)


def test_fetch_html_failure(monkeypatch, caplog):
    def mock_get(url, headers=None, timeout=None):
        raise Exception("network down")

    monkeypatch.setattr("requests.get", mock_get)
    s = Scraper()
    result = s.fetch_html("https://fail.com")

    assert result is None
    assert any("Failed to fetch https://fail.com" in msg for msg in caplog.text)
    assert any("network down" in msg for msg in caplog.text)


def test_fetch_all_parallel(monkeypatch, caplog):
    def mock_get(url, headers=None, timeout=None):
        if "ok" in url:
            return DummyResponse(f"<html>{url}</html>", 200)
        raise Exception("fail")

    monkeypatch.setattr("requests.get", mock_get)
    s = Scraper()
    urls = ["https://ok1.com", "https://ok2.com", "https://fail.com"]
    results = s.fetch_all(urls)

    assert len(results) == 3
    assert results["https://ok1.com"] is not None
    assert results["https://ok2.com"] is not None
    assert results["https://fail.com"] is None

    # Vérifie la présence de logs clés
    assert any("Parallel fetch complete" in msg for msg in caplog.text)
    assert any("Fetched https://ok1.com" in msg for msg in caplog.text)
    assert any("Failed to fetch https://fail.com" in msg for msg in caplog.text)
