"""Devil's Advocate Agent - Challenges and refutes conclusions."""

from typing import Dict, Any
from shared.models import (
    AgentResult, AgentTask, Finding, ConfidenceLevel, Source, SourceType
)
from agents.base_agent import BaseAgent


class DevilsAdvocateAgent(BaseAgent):
    """Challenges conclusions and identifies counter-arguments."""

    def __init__(self):
        super().__init__(
            name="devils_advocate_agent",
            description="Adversarial analysis - challenges assumptions and conclusions"
        )

    def analyze(self, task: AgentTask, context: Dict[str, Any]) -> AgentResult:
        """Execute adversarial analysis."""
        topic = context.get("investigation_topic", "")
        self.logger.info(f"Devil's advocate analysis for: {topic}")

        findings = []

        # Challenge previous conclusions
        previous_results = context.get("previous_results", {})
        
        counter_arguments = []
        
        if previous_results:
            # Generic counter-arguments
            counter_arguments = [
                "Historical performance does not guarantee future results",
                "Market conditions can change rapidly and unpredictably",
                "Correlations can break down in crisis situations",
                "Management or competitive landscape could deteriorate",
                "Valuation metrics may not reflect true risk",
                "External shocks (economic, geopolitical) are always possible"
            ]

        contradictions_finding = Finding(
            title="Alternative Scenarios and Counter-Arguments",
            description="Challenging assumptions and identifying risks to thesis",
            evidence=counter_arguments,
            confidence=ConfidenceLevel.MODERATE,
            sources=[Source(
                type=SourceType.INTERNAL_ANALYSIS,
                title="Adversarial Analysis",
                reliability_score=0.8
            )],
            contradictions=counter_arguments
        )
        findings.append(contradictions_finding)

        return AgentResult(
            agent_name=self.name,
            task_id=task.id,
            objective=task.objective,
            findings=findings,
            recommendations="CAUTION: These counter-arguments should be carefully considered before any decisions.",
            risks=counter_arguments,
            next_steps=["Re-evaluate assumptions", "Stress test conclusions"]
        )
