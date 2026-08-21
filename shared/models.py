"""Core data models for PROYECTO COLMENA."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid


class ConfidenceLevel(Enum):
    """Confidence levels for findings."""
    VERY_LOW = 0.0      # 0.00-0.25
    LOW = 0.25          # 0.25-0.50
    MODERATE = 0.50     # 0.50-0.75
    HIGH = 0.75         # 0.75-0.95
    VERY_HIGH = 1.0     # 0.95-1.00


class SourceType(Enum):
    """Types of information sources."""
    HISTORICAL_DATA = "historical_data"
    REAL_TIME_API = "real_time_api"
    NEWS_ARTICLE = "news_article"
    SOCIAL_MEDIA = "social_media"
    FINANCIAL_STATEMENT = "financial_statement"
    TECHNICAL_INDICATOR = "technical_indicator"
    MACRO_DATA = "macro_data"
    INTERNAL_ANALYSIS = "internal_analysis"
    AI_MODEL = "ai_model"
    WEB_INTELLIGENCE = "web_intelligence"


@dataclass
class Source:
    """Represents a source of information."""
    type: SourceType
    url: Optional[str] = None
    title: Optional[str] = None
    fetched_at: datetime = field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
    reliability_score: float = 0.5  # 0.0-1.0
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "url": self.url,
            "title": self.title,
            "fetched_at": self.fetched_at.isoformat(),
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "reliability_score": self.reliability_score,
            "notes": self.notes,
        }


@dataclass
class Finding:
    """Represents a finding from an agent."""
    title: str
    description: str
    evidence: List[str]  # List of supporting claims
    confidence: ConfidenceLevel
    sources: List[Source]
    contradictions: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "evidence": self.evidence,
            "confidence": self.confidence.name,
            "sources": [s.to_dict() for s in self.sources],
            "contradictions": self.contradictions,
            "tags": self.tags,
        }


@dataclass
class AgentTask:
    """Represents a task assigned to an agent."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_name: str = ""
    objective: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    required_data: List[str] = field(default_factory=list)
    priority: int = 5  # 1 (highest) - 10 (lowest)
    created_at: datetime = field(default_factory=datetime.utcnow)
    timeout_seconds: int = 300

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "agent_name": self.agent_name,
            "objective": self.objective,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "timeout_seconds": self.timeout_seconds,
        }


@dataclass
class AgentResult:
    """Result from an agent's execution."""
    agent_name: str
    task_id: str
    objective: str
    status: str  # "success", "partial", "failed", "timeout"
    findings: List[Finding] = field(default_factory=list)
    recommendations: str = ""
    risks: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    completed_at: datetime = field(default_factory=datetime.utcnow)
    duration_seconds: float = 0.0
    error_message: Optional[str] = None

    def overall_confidence(self) -> ConfidenceLevel:
        """Calculates average confidence of findings."""
        if not self.findings:
            return ConfidenceLevel.VERY_LOW
        avg = sum(f.confidence.value for f in self.findings) / len(self.findings)
        # Map average value to ConfidenceLevel
        if avg < 0.25:
            return ConfidenceLevel.VERY_LOW
        elif avg < 0.50:
            return ConfidenceLevel.LOW
        elif avg < 0.75:
            return ConfidenceLevel.MODERATE
        elif avg < 0.95:
            return ConfidenceLevel.HIGH
        else:
            return ConfidenceLevel.VERY_HIGH

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "task_id": self.task_id,
            "objective": self.objective,
            "status": self.status,
            "findings_count": len(self.findings),
            "overall_confidence": self.overall_confidence().name,
            "duration_seconds": self.duration_seconds,
            "error_message": self.error_message,
        }


@dataclass
class Investigation:
    """Complete investigation of a topic."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    topic: str = ""
    objective: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = "pending"  # pending, running, completed, failed

    # Results by agent
    agent_results: Dict[str, AgentResult] = field(default_factory=dict)

    # Meta-analysis from orchestrator
    orchestrator_analysis: Optional[str] = None
    contradictions_found: List[Dict[str, Any]] = field(default_factory=list)
    final_report: Optional[str] = None

    # Error tracking
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "topic": self.topic,
            "objective": self.objective,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "agent_results_count": len(self.agent_results),
            "errors_count": len(self.errors),
        }
