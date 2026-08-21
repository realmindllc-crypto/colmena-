"""Risk Manager Agent - Risk assessment and management."""

from typing import Dict, Any
from shared.models import (
    AgentResult, AgentTask, Finding, ConfidenceLevel, Source, SourceType
)
from agents.base_agent import BaseAgent


class RiskManagerAgent(BaseAgent):
    """Identifies and evaluates risks."""

    def __init__(self):
        super().__init__(
            name="risk_agent",
            description="Risk management - volatility, drawdowns, exposure evaluation"
        )

    def analyze(self, task: AgentTask, context: Dict[str, Any]) -> AgentResult:
        """Execute risk analysis."""
        topic = context.get("investigation_topic", "")
        self.logger.info(f"Risk analysis for: {topic}")

        findings = []
        risks = []

        # Analyze previous agent results for risks
        previous_results = context.get("previous_results", {})
        
        # Identify key risks based on other agents' findings
        for agent_name, result in previous_results.items():
            if result.risks:
                risks.extend(result.risks)

        # Add standard risks
        standard_risks = [
            "Market volatility and unexpected price movements",
            "Liquidity risk and execution risk",
            "Regulatory and compliance changes",
            "Information risk and false signals",
            "Concentration risk",
            "Geopolitical events"
        ]

        risk_assessment = Finding(
            title="Comprehensive Risk Assessment",
            description="Evaluation of major risks",
            evidence=standard_risks + risks,
            confidence=ConfidenceLevel.HIGH,
            sources=[Source(
                type=SourceType.INTERNAL_ANALYSIS,
                title="Risk Assessment",
                reliability_score=0.9
            )]
        )
        findings.append(risk_assessment)

        return AgentResult(
            agent_name=self.name,
            task_id=task.id,
            objective=task.objective,
            findings=findings,
            recommendations="PROCEED WITH CAUTION. Multiple risk factors identified.",
            risks=risks + standard_risks,
            next_steps=["Implement risk controls", "Set stop losses"]
        )
