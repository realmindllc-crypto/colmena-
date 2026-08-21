"""yfinance connector for financial data."""

import logging
from typing import Optional, Dict, Any
import pandas as pd
from shared.exceptions import DataFetchException


class YFinanceConnector:
    """Connector for yfinance financial data API."""

    def __init__(self):
        self.logger = logging.getLogger("YFinanceConnector")
        self.logger.info("YFinance connector initialized")

    def get_ticker_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get ticker data from yfinance."""
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            
            return {
                "info": stock.info,
                "history": stock.history(period="1y"),
                "ticker": ticker
            }
        except Exception as e:
            self.logger.error(f"Failed to fetch yfinance data for {ticker}: {e}")
            raise DataFetchException(f"yfinance error: {e}")

    def get_historical_data(
        self,
        ticker: str,
        period: str = "1y"
    ) -> Optional[pd.DataFrame]:
        """Get historical price data."""
        try:
            import yfinance as yf
            return yf.download(ticker, period=period, progress=False)
        except Exception as e:
            self.logger.error(f"Failed to fetch historical data: {e}")
            raise DataFetchException(f"yfinance history error: {e}")

    def get_multiple_tickers(
        self,
        tickers: list,
        period: str = "1y"
    ) -> Optional[pd.DataFrame]:
        """Get data for multiple tickers."""
        try:
            import yfinance as yf
            return yf.download(tickers, period=period, progress=False)
        except Exception as e:
            self.logger.error(f"Failed to fetch multiple tickers: {e}")
            raise DataFetchException(f"yfinance multi-ticker error: {e}")
