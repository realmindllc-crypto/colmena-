"""Macro Agent - Macroeconomic context and analysis."""

from typing import Dict, Any
from shared.models import (
    AgentResult, AgentTask, Finding, ConfidenceLevel, Source, SourceType
)
from agents.base_agent import BaseAgent


class MacroAgent(BaseAgent):
    """Analyzes macroeconomic factors and context."""

    def __init__(self):
        super().__init__(
            name="macro_agent",
            description="Macroeconomic analysis - inflation, rates, GDP, geopolitics"
        )

    def analyze(self, task: AgentTask, context: Dict[str, Any]) -> AgentResult:
        """Execute macro analysis."""
        topic = context.get("investigation_topic", "")
        self.logger.info(f"Macro analysis for: {topic}")

        findings = []

        # Fetch major indices for context
        try:
            indices_data = self._fetch_major_indices()
            if indices_data:
                findings.extend(self._analyze_market_context(indices_data))
        except Exception as e:
            self.logger.warning(f"Error fetching macro data: {e}")

        if not findings:
            findings.append(Finding(
                title="Macroeconomic Context",
                description="Macro economic analysis initiated",
                evidence=[f"Analyzing {topic} in broader market context"],
                confidence=ConfidenceLevel.MODERATE,
                sources=[Source(
                    type=SourceType.MACRO_DATA,
                    title="Macro Agent Initial Analysis",
                    reliability_score=0.7
                )]
            ))

        return AgentResult(
            agent_name=self.name,
            task_id=task.id,
            objective=task.objective,
            findings=findings,
            recommendations="Macro analysis complete",
            risks=["Geopolitical surprises", "Central bank policy changes"],
            next_steps=["Monitor economic calendar"]
        )

    def _fetch_major_indices(self) -> Dict[str, float]:
        """Fetch major market indices."""
        try:
            import yfinance as yf
            indices = {"SPY": None, "QQQ": None, "BTC-USD": None}
            
            for symbol in indices.keys():
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="1d")
                    if len(hist) > 0:
                        indices[symbol] = hist["Close"].iloc[-1]
                except Exception:
                    pass
            
            return indices
        except Exception as e:
            self.logger.error(f"Failed to fetch indices: {e}")
            return {}

    def _analyze_market_context(self, indices_data: Dict[str, float]) -> list:
        """Analyze broader market context."""
        findings = []

        evidence = []
        for symbol, price in indices_data.items():
            if price:
                evidence.append(f"{symbol}: ${price:.2f}")

        if evidence:
            findings.append(Finding(
                title="Major Market Indices",
                description="Broader market context",
                evidence=evidence,
                confidence=ConfidenceLevel.HIGH,
                sources=[Source(
                    type=SourceType.REAL_TIME_API,
                    title="Market indices data",
                    reliability_score=0.95
                )]
            ))

        return findings
