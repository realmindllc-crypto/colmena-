"""Fixtures for tests."""

import pytest
from shared.models import Investigation, AgentTask, Finding, ConfidenceLevel, Source, SourceType


@pytest.fixture
def sample_investigation():
    """Create a sample investigation."""
    return Investigation(
        topic="AAPL",
        objective="Comprehensive analysis of Apple Inc."
    )


@pytest.fixture
def sample_agent_task():
    """Create a sample agent task."""
    return AgentTask(
        agent_name="test_agent",
        objective="Test objective",
        context={"test": True}
    )


@pytest.fixture
def sample_finding():
    """Create a sample finding."""
    return Finding(
        title="Test Finding",
        description="A test finding",
        evidence=["Evidence 1", "Evidence 2"],
        confidence=ConfidenceLevel.HIGH,
        sources=[
            Source(
                type=SourceType.INTERNAL_ANALYSIS,
                title="Test Source",
                reliability_score=0.9
            )
        ]
    )
