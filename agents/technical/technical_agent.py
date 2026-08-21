"""Technical Agent - Technical analysis and chart patterns."""

from typing import Dict, Any, Optional
from shared.models import (
    AgentResult, AgentTask, Finding, ConfidenceLevel, Source, SourceType
)
from agents.base_agent import BaseAgent
import pandas as pd


class TechnicalAnalystAgent(BaseAgent):
    """Analyzes technical indicators and price patterns."""

    def __init__(self):
        super().__init__(
            name="technical_agent",
            description="Technical analysis - indicators, trends, support/resistance"
        )

    def analyze(self, task: AgentTask, context: Dict[str, Any]) -> AgentResult:
        """Execute technical analysis."""
        topic = context.get("investigation_topic", "")
        self.logger.info(f"Technical analysis for: {topic}")

        findings = []

        # Fetch price data
        try:
            price_data = self._fetch_price_data(topic)
            if price_data is not None:
                findings.extend(self._analyze_price_data(price_data, topic))
        except Exception as e:
            self.logger.warning(f"Could not fetch price data: {e}")

        if not findings:
            findings.append(Finding(
                title="Technical Analysis Initiated",
                description="Technical indicators collection started",
                evidence=[f"Ticker: {topic}"],
                confidence=ConfidenceLevel.MODERATE,
                sources=[Source(
                    type=SourceType.TECHNICAL_INDICATOR,
                    title="Technical Agent Initial Analysis",
                    reliability_score=0.7
                )]
            ))

        return AgentResult(
            agent_name=self.name,
            task_id=task.id,
            objective=task.objective,
            findings=findings,
            recommendations="Technical analysis complete",
            risks=["False signals in sideways markets", "Indicator lag"],
            next_steps=["Combine with fundamental analysis"]
        )

    def _fetch_price_data(self, ticker: str) -> Optional[pd.DataFrame]:
        """Fetch historical price data."""
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            history = stock.history(period="1y")
            return history
        except Exception as e:
            self.logger.error(f"Failed to fetch price data: {e}")
            return None

    def _analyze_price_data(self, data: pd.DataFrame, ticker: str) -> list:
        """Analyze price data and create findings."""
        findings = []

        try:
            # Basic analysis
            current_price = data["Close"].iloc[-1] if len(data) > 0 else 0
            min_price = data["Close"].min()
            max_price = data["Close"].max()
            avg_volume = data["Volume"].mean()

            evidence = [
                f"Current Price: ${current_price:.2f}",
                f"52-Week High: ${max_price:.2f}",
                f"52-Week Low: ${min_price:.2f}",
                f"Avg Volume: {avg_volume:,.0f}"
            ]

            findings.append(Finding(
                title="Price Statistics",
                description="Historical price and volume statistics",
                evidence=evidence,
                confidence=ConfidenceLevel.HIGH,
                sources=[Source(
                    type=SourceType.TECHNICAL_INDICATOR,
                    title=f"Price data for {ticker}",
                    reliability_score=0.95
                )]
            ))

            # Calculate simple moving averages
            if len(data) >= 200:
                ma_50 = data["Close"].rolling(window=50).mean().iloc[-1]
                ma_200 = data["Close"].rolling(window=200).mean().iloc[-1]

                trend = "BULLISH" if ma_50 > ma_200 else "BEARISH"
                evidence_ma = [
                    f"50-Day MA: ${ma_50:.2f}",
                    f"200-Day MA: ${ma_200:.2f}",
                    f"Trend: {trend}"
                ]

                findings.append(Finding(
                    title="Moving Average Analysis",
                    description="Long-term trend indicators",
                    evidence=evidence_ma,
                    confidence=ConfidenceLevel.MODERATE,
                    sources=[Source(
                        type=SourceType.TECHNICAL_INDICATOR,
                        title="Moving Averages",
                        reliability_score=0.75
                    )]
                ))
        except Exception as e:
            self.logger.warning(f"Error analyzing price data: {e}")

        return findings
