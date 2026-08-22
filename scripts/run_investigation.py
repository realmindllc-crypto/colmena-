"""CLI script for running investigations."""

import click
import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.models import Investigation
from shared.utils import setup_logging
from agents.orchestrator.orchestrator import Orchestrator
from agents.research.research_agent import ResearchAgent
from agents.financial.financial_agent import FinancialAnalystAgent
from agents.technical.technical_agent import TechnicalAnalystAgent
from agents.sentiment.sentiment_agent import SentimentAgent
from agents.macro.macro_agent import MacroAgent
from agents.risk.risk_agent import RiskManagerAgent
from agents.devils_advocate.devils_advocate_agent import DevilsAdvocateAgent
from agents.report.report_agent import ReportAgent


@click.group()
def cli():
    """PROYECTO COLMENA - Multiagent Investigation System."""
    pass


@cli.command()
@click.argument('topic')
@click.option('--objective', default=None, help='Investigation objective')
@click.option('--log-level', default='INFO', help='Logging level')
def investigate(topic: str, objective: str, log_level: str):
    """Run a complete investigation."""
    # Setup logging
    logger = setup_logging("COLMENA", log_level)
    logger.info(f"🐝 PROYECTO COLMENA - Investigation Started")
    logger.info(f"Topic: {topic}")

    # Initialize agents
    agents = {
        "research_agent": ResearchAgent(),
        "financial_agent": FinancialAnalystAgent(),
        "technical_agent": TechnicalAnalystAgent(),
        "sentiment_agent": SentimentAgent(),
        "macro_agent": MacroAgent(),
        "risk_agent": RiskManagerAgent(),
        "devils_advocate_agent": DevilsAdvocateAgent(),
        "report_agent": ReportAgent(),
    }

    # Create orchestrator
    orchestrator = Orchestrator(agents)

    # Create investigation
    investigation = Investigation(
        topic=topic,
        objective=objective or f"Comprehensive analysis of {topic}"
    )

    # Execute
    try:
        result = orchestrator.execute_investigation(investigation)
        
        # Display results
        click.echo("\n" + "="*80)
        if result.final_report:
            click.echo(result.final_report)
        click.echo("="*80)
        click.echo(f"\n✅ Investigation completed successfully!")
        click.echo(f"Duration: {result.duration_seconds:.2f}s")
        click.echo(f"Agents: {len(result.agent_results)}")
        click.echo(f"Findings: {sum(len(r.findings) for r in result.agent_results.values())}")
        
    except Exception as e:
        click.echo(f"\n❌ Error: {e}", err=True)
        logger.error(f"Investigation failed: {e}", exc_info=True)
        sys.exit(1)


@cli.command()
def version():
    """Show version information."""
    click.echo("PROYECTO COLMENA v1.0.0")
    click.echo("Multiagent AI Investigation System")
    click.echo("Phase 1 - MVP")


@cli.command()
def health():
    """Check system health."""
    click.echo("🐝 PROYECTO COLMENA - Health Check\n")
    
    checks = {
        "Core imports": _check_imports(),
        "LLM configuration": _check_llm(),
        "Financial data API": _check_yfinance(),
        "Apify integration": _check_apify(),
    }
    
    all_pass = True
    for check_name, status in checks.items():
        symbol = "✅" if status else "❌"
        click.echo(f"{symbol} {check_name}")
        if not status:
            all_pass = False
    
    click.echo()
    if all_pass:
        click.echo("✅ All systems operational")
    else:
        click.echo("⚠️  Some systems unavailable (non-critical)")


def _check_imports() -> bool:
    """Check if core imports work."""
    try:
        from shared.models import Investigation
        from agents.orchestrator.orchestrator import Orchestrator
        return True
    except Exception:
        return False


def _check_llm() -> bool:
    """Check LLM configuration."""
    try:
        from core.llm_client import LLMClient
        client = LLMClient()
        return True
    except Exception:
        return False


def _check_yfinance() -> bool:
    """Check yfinance."""
    try:
        import yfinance as yf
        return True
    except Exception:
        return False


def _check_apify() -> bool:
    """Check Apify."""
    try:
        import os
        return bool(os.getenv("APIFY_TOKEN"))
    except Exception:
        return False


if __name__ == "__main__":
    cli()
