"""Research Agent - Information gathering and verification."""

from typing import Dict, Any, List
from shared.models import (
    AgentResult, AgentTask, Finding, ConfidenceLevel, Source, SourceType
)
from agents.base_agent import BaseAgent
from core.data_fetcher import NewsDataFetcher, WebDataFetcher


class ResearchAgent(BaseAgent):
    """Gathers and verifies information about companies and markets."""

    def __init__(self):
        super().__init__(
            name="research_agent",
            description="Information gathering and source verification"
        )
        self.news_fetcher = NewsDataFetcher()
        self.web_fetcher = WebDataFetcher()

    def analyze(self, task: AgentTask, context: Dict[str, Any]) -> AgentResult:
        """Execute research task."""
        topic = context.get("investigation_topic", "")
        self.logger.info(f"Researching: {topic}")

        findings = []
        sources = []

        # 1. Fetch basic info
        basic_finding = Finding(
            title=f"Basic Information: {topic}",
            description=f"Initial research on {topic}",
            evidence=[
                f"Topic: {topic}",
                "Research phase initiated"
            ],
            confidence=ConfidenceLevel.MODERATE,
            sources=[Source(
                type=SourceType.INTERNAL_ANALYSIS,
                title="Research Agent Initial Task",
                reliability_score=0.8
            )]
        )
        findings.append(basic_finding)

        # 2. Fetch news (placeholder)
        try:
            news = self.news_fetcher.fetch_company_news(topic, limit=5)
            if news:
                news_finding = Finding(
                    title=f"Recent News: {topic}",
                    description="Recent news and developments",
                    evidence=[n.get("title", "") for n in news],
                    confidence=ConfidenceLevel.HIGH,
                    sources=[Source(
                        type=SourceType.NEWS_ARTICLE,
                        url=n.get("url"),
                        title=n.get("title"),
                        reliability_score=0.85
                    ) for n in news]
                )
                findings.append(news_finding)
        except Exception as e:
            self.logger.warning(f"Failed to fetch news: {e}")

        return AgentResult(
            agent_name=self.name,
            task_id=task.id,
            objective=task.objective,
            findings=findings,
            recommendations="Research phase completed. Ready for specialized analysis.",
            next_steps=[
                "Financial analysis should proceed",
                "Technical analysis should proceed",
                "Sentiment analysis should proceed"
            ]
        )
