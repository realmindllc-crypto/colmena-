"""Main Orchestrator - Coordinates all agents."""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from shared.models import Investigation, AgentTask, AgentResult
from agents.base_agent import BaseAgent
from shared.constants import (
    PRIORITY_CRITICAL, PRIORITY_HIGH, PRIORITY_MEDIUM,
    STATUS_RUNNING, STATUS_COMPLETED
)


class Orchestrator:
    """Central coordinator of PROYECTO COLMENA."""

    def __init__(self, agents: Dict[str, BaseAgent]):
        """Initialize orchestrator with agents."""
        self.agents = agents
        self.logger = logging.getLogger("Orchestrator")
        self.logger.info(f"Orchestrator initialized with {len(agents)} agents")

    def plan_investigation(self, investigation: Investigation) -> List[AgentTask]:
        """Create execution plan for investigation."""
        tasks = []

        # Phase 1: Research (must be first)
        if "research_agent" in self.agents:
            tasks.append(AgentTask(
                agent_name="research_agent",
                objective=f"Research: {investigation.objective}",
                context={"topic": investigation.topic},
                priority=PRIORITY_CRITICAL
            ))

        # Phase 2: Parallel analysis
        parallel_agents = [
            "financial_agent",
            "technical_agent",
            "sentiment_agent",
            "macro_agent"
        ]

        for agent_name in parallel_agents:
            if agent_name in self.agents:
                tasks.append(AgentTask(
                    agent_name=agent_name,
                    objective=f"{agent_name.replace('_', ' ').title()}: {investigation.objective}",
                    priority=PRIORITY_HIGH
                ))

        # Phase 3: Evaluation (depends on analysis)
        eval_agents = ["risk_agent", "devils_advocate_agent"]
        for agent_name in eval_agents:
            if agent_name in self.agents:
                tasks.append(AgentTask(
                    agent_name=agent_name,
                    objective=f"{agent_name.replace('_', ' ').title()}: {investigation.objective}",
                    priority=PRIORITY_MEDIUM + 1
                ))

        # Phase 4: Report generation
        if "report_agent" in self.agents:
            tasks.append(AgentTask(
                agent_name="report_agent",
                objective=f"Generate report: {investigation.objective}",
                priority=PRIORITY_MEDIUM + 2
            ))

        return tasks

    def execute_investigation(
        self,
        investigation: Investigation,
        max_workers: int = 5
    ) -> Investigation:
        """Execute complete investigation."""
        investigation.status = STATUS_RUNNING
        investigation.started_at = datetime.utcnow()

        self.logger.info(f"Starting investigation: {investigation.topic}")

        tasks = self.plan_investigation(investigation)
        tasks_by_priority = self._group_by_priority(tasks)

        # Execute by priority
        for priority in sorted(tasks_by_priority.keys()):
            self.logger.info(f"Executing priority {priority} tasks...")
            self._execute_task_batch(
                tasks_by_priority[priority],
                investigation,
                max_workers
            )

        # Post-processing
        self._detect_contradictions(investigation)
        self._generate_final_report(investigation)

        investigation.status = STATUS_COMPLETED
        investigation.completed_at = datetime.utcnow()

        self.logger.info(f"Investigation completed in {investigation.duration_seconds:.2f}s")
        return investigation

    def _group_by_priority(self, tasks: List[AgentTask]) -> Dict[int, List[AgentTask]]:
        """Group tasks by priority."""
        grouped = {}
        for task in tasks:
            if task.priority not in grouped:
                grouped[task.priority] = []
            grouped[task.priority].append(task)
        return grouped

    def _execute_task_batch(
        self,
        tasks: List[AgentTask],
        investigation: Investigation,
        max_workers: int
    ):
        """Execute batch of tasks in parallel."""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}

            for task in tasks:
                agent = self.agents.get(task.agent_name)
                if not agent:
                    self.logger.warning(f"Agent not found: {task.agent_name}")
                    continue

                # Prepare context
                context = {
                    "investigation_topic": investigation.topic,
                    "previous_results": investigation.agent_results
                }

                future = executor.submit(agent.execute, task, context)
                futures[future] = task.agent_name

            # Collect results
            for future in as_completed(futures):
                agent_name = futures[future]
                try:
                    result = future.result(timeout=300)
                    investigation.agent_results[agent_name] = result
                    self.logger.info(f"✅ {agent_name}: {result.status}")
                except Exception as e:
                    self.logger.error(f"❌ {agent_name}: {e}")
                    investigation.errors.append(f"{agent_name}: {e}")

    def _detect_contradictions(self, investigation: Investigation):
        """Detect contradictions between agent results."""
        self.logger.info("Analyzing for contradictions...")
        # Simplified for MVP - could be expanded
        pass

    def _generate_final_report(self, investigation: Investigation):
        """Generate final consolidated report."""
        self.logger.info("Generating final report...")

        summary = f"""═══════════════════════════════════════════════════════════
🐝 PROYECTO COLMENA - INVESTIGATION SUMMARY
═══════════════════════════════════════════════════════════

Topic: {investigation.topic}
Status: {investigation.status}
Duration: {investigation.duration_seconds:.2f}s
Timestamp: {investigation.completed_at.isoformat()}

───────────────────────────────────────────────────────────
AGENT RESULTS:
───────────────────────────────────────────────────────────
"""

        for agent_name, result in investigation.agent_results.items():
            status_emoji = "✅" if result.status == "success" else "⚠️"
            summary += f"{status_emoji} {agent_name}\n"
            summary += f"   Status: {result.status}\n"
            summary += f"   Findings: {len(result.findings)}\n"
            summary += f"   Duration: {result.duration_seconds:.2f}s\n"
            summary += f"   Confidence: {result.overall_confidence().name}\n\n"

        summary += f"""───────────────────────────────────────────────────────────
ERRORS: {len(investigation.errors)}
───────────────────────────────────────────────────────────
"""

        if investigation.errors:
            for error in investigation.errors:
                summary += f"  ⚠️ {error}\n"
        else:
            summary += "  ✅ No errors"

        summary += f"""\n═══════════════════════════════════════════════════════════
"""

        investigation.final_report = summary
        investigation.orchestrator_analysis = summary

    @property
    def duration_seconds(self) -> float:
        """Get duration in seconds."""
        return self._duration
