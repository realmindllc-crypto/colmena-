"""Base agent class for PROYECTO COLMENA."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from shared.models import AgentResult, AgentTask
import logging
import time


class BaseAgent(ABC):
    """Base class for all agents."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(self.name)
        self.execution_count = 0
        self.total_duration = 0.0

    @abstractmethod
    def analyze(self, task: AgentTask, context: Dict[str, Any]) -> AgentResult:
        """Execute agent's analysis."""
        pass

    def execute(self, task: AgentTask, context: Dict[str, Any]) -> AgentResult:
        """Execute with timing and error handling."""
        self.logger.info(f"Starting task: {task.objective}")
        start_time = time.time()

        try:
            result = self.analyze(task, context)
            duration = time.time() - start_time

            result.duration_seconds = duration
            result.status = "success"

            self.execution_count += 1
            self.total_duration += duration

            self.logger.info(
                f"Completed. Findings: {len(result.findings)}, "
                f"Duration: {duration:.2f}s"
            )

            return result

        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"Execution error: {str(e)}", exc_info=True)

            return AgentResult(
                agent_name=self.name,
                task_id=task.id,
                objective=task.objective,
                status="failed",
                error_message=str(e),
                duration_seconds=duration
            )

    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        return {
            "name": self.name,
            "executions": self.execution_count,
            "avg_duration": self.total_duration / self.execution_count
                           if self.execution_count > 0 else 0,
            "total_duration": self.total_duration
        }
