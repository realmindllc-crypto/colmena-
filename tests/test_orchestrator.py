"""Tests for orchestrator."""

import pytest
from shared.models import Investigation, AgentTask
from agents.orchestrator.orchestrator import Orchestrator
from agents.base_agent import BaseAgent
from agents.research.research_agent import ResearchAgent
from agents.financial.financial_agent import FinancialAnalystAgent


class TestOrchestrator:
    """Test Orchestrator."""

    def test_initialization(self):
        """Test orchestrator initialization."""
        agents = {
            "research_agent": ResearchAgent(),
            "financial_agent": FinancialAnalystAgent(),
        }
        orch = Orchestrator(agents)
        assert len(orch.agents) == 2

    def test_plan_investigation(self):
        """Test investigation planning."""
        agents = {
            "research_agent": ResearchAgent(),
            "financial_agent": FinancialAnalystAgent(),
            "report_agent": None,  # Mock
        }
        orch = Orchestrator(agents)
        
        inv = Investigation(topic="AAPL", objective="Test")
        tasks = orch.plan_investigation(inv)
        
        assert len(tasks) > 0
        assert any(t.agent_name == "research_agent" for t in tasks)

    @pytest.mark.slow
    def test_execute_simple_investigation(self, sample_investigation):
        """Test simple investigation execution."""
        agents = {
            "research_agent": ResearchAgent(),
        }
        orch = Orchestrator(agents)
        
        # This is a slow test since it makes API calls
        result = orch.execute_investigation(sample_investigation, max_workers=1)
        
        assert result.status == "completed"
        assert len(result.agent_results) > 0
