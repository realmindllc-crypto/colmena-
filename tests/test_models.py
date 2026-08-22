"""Tests for data models."""

import pytest
from shared.models import (
    Investigation, AgentTask, Finding, AgentResult, 
    ConfidenceLevel, Source, SourceType
)


class TestInvestigation:
    """Test Investigation model."""

    def test_creation(self):
        """Test creating an investigation."""
        inv = Investigation(topic="AAPL", objective="Test")
        assert inv.topic == "AAPL"
        assert inv.objective == "Test"
        assert inv.status == "pending"
        assert inv.id is not None

    def test_to_dict(self):
        """Test to_dict serialization."""
        inv = Investigation(topic="AAPL")
        d = inv.to_dict()
        assert d["topic"] == "AAPL"
        assert "id" in d
        assert "status" in d


class TestFinding:
    """Test Finding model."""

    def test_creation(self, sample_finding):
        """Test creating a finding."""
        assert sample_finding.title == "Test Finding"
        assert len(sample_finding.evidence) == 2
        assert sample_finding.confidence == ConfidenceLevel.HIGH

    def test_to_dict(self, sample_finding):
        """Test serialization."""
        d = sample_finding.to_dict()
        assert d["title"] == "Test Finding"
        assert d["confidence"] == "HIGH"
        assert len(d["sources"]) == 1


class TestAgentResult:
    """Test AgentResult model."""

    def test_overall_confidence(self, sample_finding):
        """Test confidence calculation."""
        result = AgentResult(
            agent_name="test",
            task_id="123",
            objective="Test",
            status="success",
            findings=[sample_finding]
        )
        assert result.overall_confidence() == ConfidenceLevel.HIGH

    def test_overall_confidence_empty(self):
        """Test confidence with no findings."""
        result = AgentResult(
            agent_name="test",
            task_id="123",
            objective="Test",
            status="success",
            findings=[]
        )
        assert result.overall_confidence() == ConfidenceLevel.VERY_LOW
