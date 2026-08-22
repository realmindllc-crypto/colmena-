"""Tests for agents."""

import pytest
from shared.models import AgentTask
from agents.research.research_agent import ResearchAgent
from agents.financial.financial_agent import FinancialAnalystAgent
from agents.technical.technical_agent import TechnicalAnalystAgent


class TestResearchAgent:
    """Test Research Agent."""

    def test_initialization(self):
        """Test agent initialization."""
        agent = ResearchAgent()
        assert agent.name == "research_agent"
        assert len(agent.description) > 0

    def test_execute(self, sample_agent_task):
        """Test agent execution."""
        agent = ResearchAgent()
        context = {"investigation_topic": "AAPL"}
        
        result = agent.execute(sample_agent_task, context)
        
        assert result.agent_name == "research_agent"
        assert result.status in ["success", "partial", "failed"]
        assert result.duration_seconds >= 0


class TestFinancialAgent:
    """Test Financial Agent."""

    def test_initialization(self):
        """Test agent initialization."""
        agent = FinancialAnalystAgent()
        assert agent.name == "financial_agent"

    @pytest.mark.external_api
    def test_execute_with_real_data(self, sample_agent_task):
        """Test with real financial data."""
        agent = FinancialAnalystAgent()
        context = {"investigation_topic": "AAPL"}
        
        result = agent.execute(sample_agent_task, context)
        assert result.status in ["success", "partial", "failed"]


class TestTechnicalAgent:
    """Test Technical Agent."""

    def test_initialization(self):
        """Test agent initialization."""
        agent = TechnicalAnalystAgent()
        assert agent.name == "technical_agent"
