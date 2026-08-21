"""Apify client for web scraping."""

import os
from typing import Dict, Any, Optional, List
import requests
import logging
from shared.exceptions import DataFetchException


class ApifyClient:
    """Client for Apify web scraping service."""

    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or os.getenv("APIFY_TOKEN")
        self.base_url = "https://api.apify.com/v2"
        self.logger = logging.getLogger("ApifyClient")

        if self.api_token:
            self.logger.info("Apify client initialized")
        else:
            self.logger.warning("Apify token not configured")

    def is_available(self) -> bool:
        """Check if Apify is available."""
        return bool(self.api_token)

    def scrape_website(
        self,
        url: str,
        actor_id: str = "apify/web-scraper",
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Scrape a website using Apify."""
        if not self.is_available():
            raise DataFetchException("Apify token not configured")

        if not options:
            options = {}

        payload = {
            "startUrls": [{"url": url}],
            **options
        }

        try:
            # Start actor run
            response = requests.post(
                f"{self.base_url}/acts/{actor_id}/runs",
                json=payload,
                params={"token": self.api_token},
                timeout=30
            )
            response.raise_for_status()
            
            run_data = response.json()
            run_id = run_data.get("data", {}).get("id")
            
            if not run_id:
                raise DataFetchException("Failed to start Apify run")

            # Wait for completion and get results
            return self._wait_for_results(actor_id, run_id)

        except requests.RequestException as e:
            self.logger.error(f"Apify error: {e}")
            raise DataFetchException(f"Apify scraping failed: {e}")

    def scrape_google_search(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, str]]:
        """Scrape Google search results."""
        if not self.is_available():
            self.logger.warning("Apify not available, returning empty results")
            return []

        try:
            # This would use Apify's Google Search scraper
            # Implementation depends on Apify actor availability
            self.logger.info(f"Scraping Google for: {query}")
            # Placeholder - would need proper Apify actor
            return []
        except Exception as e:
            self.logger.error(f"Google scrape failed: {e}")
            return []

    def _wait_for_results(
        self,
        actor_id: str,
        run_id: str,
        max_wait: int = 60
    ) -> Dict[str, Any]:
        """Wait for Apify run to complete and get results."""
        import time
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(
                    f"{self.base_url}/acts/{actor_id}/runs/{run_id}",
                    params={"token": self.api_token},
                    timeout=10
                )
                response.raise_for_status()
                
                run_data = response.json().get("data", {})
                
                if run_data.get("status") in ["SUCCEEDED", "FAILED"]:
                    # Get dataset results
                    dataset_id = run_data.get("defaultDatasetId")
                    if dataset_id:
                        return self._get_dataset(dataset_id)
                    return run_data
                
                time.sleep(2)  # Poll every 2 seconds
                
            except requests.RequestException as e:
                self.logger.error(f"Error checking run status: {e}")
                raise DataFetchException(f"Failed to check Apify run status: {e}")
        
        raise DataFetchException("Apify run timeout")

    def _get_dataset(self, dataset_id: str) -> List[Dict[str, Any]]:
        """Get results from Apify dataset."""
        try:
            response = requests.get(
                f"{self.base_url}/datasets/{dataset_id}/items",
                params={"token": self.api_token},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error fetching dataset: {e}")
            raise DataFetchException(f"Failed to fetch Apify dataset: {e}")
