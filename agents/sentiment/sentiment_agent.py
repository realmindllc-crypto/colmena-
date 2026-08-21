"""Sentiment Agent - Market and news sentiment analysis."""

from typing import Dict, Any, List
from shared.models import (
    AgentResult, AgentTask, Finding, ConfidenceLevel, Source, SourceType
)
from agents.base_agent import BaseAgent
from core.data_fetcher import NewsDataFetcher


class SentimentAgent(BaseAgent):
    """Analyzes market sentiment and news tone."""

    def __init__(self):
        super().__init__(
            name="sentiment_agent",
            description="Sentiment analysis - news tone, market mood, social signals"
        )
        self.news_fetcher = NewsDataFetcher()

    def analyze(self, task: AgentTask, context: Dict[str, Any]) -> AgentResult:
        """Execute sentiment analysis."""
        topic = context.get("investigation_topic", "")
        self.logger.info(f"Analyzing sentiment for: {topic}")

        findings = []

        # Fetch news for sentiment
        try:
            news_items = self.news_fetcher.fetch_company_news(topic, limit=10)
            if news_items:
                sentiment_finding = self._analyze_news_sentiment(news_items, topic)
                findings.append(sentiment_finding)
            else:
                # Fallback if no news
                findings.append(Finding(
                    title="Sentiment Analysis",
                    description="Initial sentiment assessment",
                    evidence=[f"Analyzing sentiment for {topic}"],
                    confidence=ConfidenceLevel.LOW,
                    sources=[Source(
                        type=SourceType.INTERNAL_ANALYSIS,
                        title="Sentiment Agent",
                        reliability_score=0.5
                    )]
                ))
        except Exception as e:
            self.logger.warning(f"Error in sentiment analysis: {e}")
            findings.append(Finding(
                title="Sentiment Analysis Attempted",
                description="Sentiment analysis initiated",
                evidence=[f"Topic: {topic}"],
                confidence=ConfidenceLevel.LOW,
                sources=[Source(
                    type=SourceType.INTERNAL_ANALYSIS,
                    title="Sentiment Agent",
                    reliability_score=0.5
                )]
            ))

        return AgentResult(
            agent_name=self.name,
            task_id=task.id,
            objective=task.objective,
            findings=findings,
            recommendations="Sentiment analysis complete",
            risks=["Sentiment can be misleading", "Social media noise"],
            next_steps=["Verify with hard data"]
        )

    def _analyze_news_sentiment(self, news_items: List[Dict], topic: str) -> Finding:
        """Analyze sentiment from news items."""
        # Simplified sentiment analysis
        positive_words = ["gain", "rise", "surge", "bull", "strong", "beat"]
        negative_words = ["fall", "drop", "bear", "weak", "miss", "loss"]

        positive_count = 0
        negative_count = 0

        for item in news_items[:5]:
            title = item.get("title", "").lower()
            for word in positive_words:
                if word in title:
                    positive_count += 1
            for word in negative_words:
                if word in title:
                    negative_count += 1

        if positive_count > negative_count:
            sentiment = "BULLISH"
            confidence = ConfidenceLevel.MODERATE
        elif negative_count > positive_count:
            sentiment = "BEARISH"
            confidence = ConfidenceLevel.MODERATE
        else:
            sentiment = "NEUTRAL"
            confidence = ConfidenceLevel.LOW

        return Finding(
            title="Market Sentiment",
            description=f"Overall sentiment assessment: {sentiment}",
            evidence=[
                f"Positive indicators: {positive_count}",
                f"Negative indicators: {negative_count}",
                f"Sentiment: {sentiment}"
            ],
            confidence=confidence,
            sources=[Source(
                type=SourceType.NEWS_ARTICLE,
                title="News sentiment analysis",
                reliability_score=0.7
            )]
        )
