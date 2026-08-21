"""Financial Agent - Fundamental analysis of companies and securities."""

import os
from typing import Dict, Any, Optional
from shared.models import (
    AgentResult, AgentTask, Finding, ConfidenceLevel, Source, SourceType
)
from agents.base_agent import BaseAgent


class FinancialAnalystAgent(BaseAgent):
    """Analyzes fundamental financial metrics."""

    def __init__(self):
        super().__init__(
            name="financial_agent",
            description="Fundamental analysis - earnings, ratios, valuation"
        )

    def analyze(self, task: AgentTask, context: Dict[str, Any]) -> AgentResult:
        """Execute financial analysis."""
        topic = context.get("investigation_topic", "")
        self.logger.info(f"Analyzing fundamentals for: {topic}")

        findings = []

        # Try to fetch financial data
        try:
            financial_data = self._fetch_financial_data(topic)
            if financial_data:
                findings.extend(self._analyze_financial_data(financial_data, topic))
        except Exception as e:
            self.logger.warning(f"Could not fetch financial data: {e}")

        if not findings:
            # Fallback finding
            findings.append(Finding(
                title="Financial Data Collection",
                description="Attempted to collect fundamental financial metrics",
                evidence=[f"Analyzing ticker: {topic}"],
                confidence=ConfidenceLevel.MODERATE,
                sources=[Source(
                    type=SourceType.INTERNAL_ANALYSIS,
                    title="Financial Agent Initial Analysis",
                    reliability_score=0.7
                )]
            ))

        return AgentResult(
            agent_name=self.name,
            task_id=task.id,
            objective=task.objective,
            findings=findings,
            recommendations="Fundamental analysis complete",
            risks=["Market volatility", "Earnings surprises", "Regulatory changes"],
            next_steps=["Cross-check with technical analysis"]
        )

    def _fetch_financial_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Fetch financial data from yfinance."""
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            info = stock.info
            history = stock.history(period="1y")
            
            return {
                "info": info,
                "history": history
            }
        except Exception as e:
            self.logger.error(f"Failed to fetch yfinance data: {e}")
            return None

    def _analyze_financial_data(
        self, data: Dict[str, Any], ticker: str
    ) -> list:
        """Analyze financial data and create findings."""
        findings = []
        info = data.get("info", {})

        # Extract key metrics
        pe_ratio = info.get("trailingPE", None)
        dividend_yield = info.get("dividendYield", None)
        market_cap = info.get("marketCap", None)
        revenue = info.get("totalRevenue", None)

        evidence = []
        if market_cap:
            evidence.append(f"Market Cap: ${market_cap:,.0f}")
        if revenue:
            evidence.append(f"Revenue: ${revenue:,.0f}")
        if pe_ratio:
            evidence.append(f"P/E Ratio: {pe_ratio:.2f}")
        if dividend_yield:
            evidence.append(f"Dividend Yield: {dividend_yield*100:.2f}%")

        if evidence:
            findings.append(Finding(
                title="Key Financial Metrics",
                description="Fundamental financial indicators",
                evidence=evidence,
                confidence=ConfidenceLevel.HIGH,
                sources=[Source(
                    type=SourceType.FINANCIAL_STATEMENT,
                    title=f"yfinance data for {ticker}",
                    reliability_score=0.9
                )]
            ))

        return findings
