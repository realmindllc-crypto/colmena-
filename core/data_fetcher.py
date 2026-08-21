"""Data fetchers for external APIs."""

import requests
from typing import Dict, Any, Optional, List
import logging
from shared.exceptions import DataFetchException


class DataFetcher:
    """Base class for data fetching."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "PROYECTO-COLMENA/1.0"
        })

    def _fetch_url(self, url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Safely fetch URL."""
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {url}: {e}")
            raise DataFetchException(f"Failed to fetch data: {e}")


class NewsDataFetcher(DataFetcher):
    """Fetches news data from various sources."""

    def fetch_company_news(self, company: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch recent news about a company."""
        # Placeholder - would integrate with real news API
        # For now, return empty list
        self.logger.info(f"Fetching news for {company}")
        return []


class WebDataFetcher(DataFetcher):
    """Fetches data from web pages."""

    def fetch_page(self, url: str) -> str:
        """Fetch HTML content from a page."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch page {url}: {e}")
            raise DataFetchException(f"Failed to fetch page: {e}")

    def parse_html(self, html: str, selector: str) -> List[str]:
        """Parse HTML using CSS selector."""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            elements = soup.select(selector)
            return [el.get_text() for el in elements]
        except Exception as e:
            self.logger.error(f"Failed to parse HTML: {e}")
            return []
