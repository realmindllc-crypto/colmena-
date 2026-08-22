# 🐝 PROYECTO COLMENA - README

## Overview

**PROYECTO COLMENA** is a sophisticated **multiagent AI system** designed for comprehensive financial analysis, research, and decision support. Like a colony of bees, each agent is specialized and collaborative, working together to produce intelligent analysis.

> "In a honeycomb, intelligence doesn't reside in a single bee, but in the collaboration of all of them."

## Key Features

✨ **Multiagent Architecture**
- 8 specialized agents working in coordination
- Hierarchical orchestration with priority-based task scheduling
- Parallel execution for maximum efficiency

🔬 **Comprehensive Analysis**
- **Research Agent**: Gathers and verifies information
- **Financial Agent**: Fundamental analysis (P/E, earnings, valuations)
- **Technical Agent**: Price patterns, indicators, trends
- **Sentiment Agent**: Market mood and news sentiment
- **Macro Agent**: Economic context and broader market
- **Risk Agent**: Risk identification and assessment
- **Devil's Advocate**: Challenges conclusions and identifies counter-arguments
- **Report Agent**: Synthesizes findings into comprehensive reports

🛡️ **Risk Management**
- Built-in risk assessment at every stage
- Contradiction detection
- Adversarial analysis to challenge assumptions
- No automatic execution (analysis and simulation only in Phase 1-5)

📊 **Data Integration**
- yfinance for free financial data
- Apify for web intelligence
- Extensible architecture for additional APIs

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/realmindllc-crypto/colmena-.git
cd colmena-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### First Investigation

```bash
# Run a simple analysis
python scripts/run_investigation.py investigate AAPL

# Check system health
python scripts/run_investigation.py health

# See version
python scripts/run_investigation.py version
```

### Python API

```python
from agents.orchestrator.orchestrator import Orchestrator
from agents.research.research_agent import ResearchAgent
from agents.financial.financial_agent import FinancialAnalystAgent
from agents.technical.technical_agent import TechnicalAnalystAgent
from agents.sentiment.sentiment_agent import SentimentAgent
from agents.macro.macro_agent import MacroAgent
from agents.risk.risk_agent import RiskManagerAgent
from agents.devils_advocate.devils_advocate_agent import DevilsAdvocateAgent
from agents.report.report_agent import ReportAgent
from shared.models import Investigation

# Create agents
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
    topic="AAPL",
    objective="Comprehensive analysis of Apple Inc."
)

# Execute
result = orchestrator.execute_investigation(investigation)

# View results
print(result.final_report)
for agent_name, agent_result in result.agent_results.items():
    print(f"\n{agent_name}:")
    print(f"  Status: {agent_result.status}")
    print(f"  Findings: {len(agent_result.findings)}")
    print(f"  Confidence: {agent_result.overall_confidence().name}")
```

## Configuration

Create `.env` file with required settings:

```bash
# Required: OpenAI API Key
OPENAI_API_KEY=sk-your-key-here
LLM_MODEL=gpt-4o-mini

# Optional: Apify (web scraping)
APIFY_TOKEN=your-token
APIFY_ENABLED=true

# Optional: Other settings
LOG_LEVEL=INFO
DEBUG=false
```

## Project Structure

```
colmena-/
├── agents/                    # Agent implementations
│   ├── base_agent.py          # Abstract base class
│   ├── orchestrator/          # Central coordinator
│   ├── research/              # Information gathering
│   ├── financial/             # Fundamental analysis
│   ├── technical/             # Technical indicators
│   ├── sentiment/             # Sentiment analysis
│   ├── macro/                 # Macro context
│   ├── risk/                  # Risk assessment
│   ├── devils_advocate/       # Adversarial analysis
│   └── report/                # Report generation
├── core/                      # System core
│   ├── event_system.py        # Event logging
│   ├── llm_client.py          # OpenAI wrapper
│   └── data_fetcher.py        # Data retrieval base
├── integrations/              # External APIs
│   ├── apify/                 # Web scraping
│   └── financial_data/        # Financial APIs
├── shared/                    # Shared utilities
│   ├── models.py              # Data classes
│   ├── constants.py           # Constants
│   ├── exceptions.py          # Exceptions
│   └── utils.py               # Utilities
├── scripts/                   # CLI and scripts
├── tests/                     # Unit tests
├── docs/                      # Documentation
├── requirements.txt           # Dependencies
├── pytest.ini                 # Test config
├── Makefile                   # Build commands
└── README.md                  # This file
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov=shared --cov=core

# Run specific tests
pytest tests/test_models.py -v
pytest tests/test_orchestrator.py -v

# Run without slow tests
pytest -m "not slow"

# Run external API tests only
pytest -m external_api
```

## Make Commands

```bash
make help          # Show available commands
make install       # Install dependencies
make test          # Run tests
make test-cov      # Run tests with coverage
make lint          # Run linting (flake8, mypy)
make format        # Format code (black)
make run           # Run investigation CLI
make clean         # Clean generated files
```

## Data Model

### Investigation
Top-level container for analysis:
```python
Investigation(
    id: str
    topic: str
    objective: str
    status: str  # pending, running, completed, failed
    agent_results: Dict[str, AgentResult]
    final_report: str
    errors: List[str]
)
```

### Finding
Individual agent finding with evidence:
```python
Finding(
    title: str
    description: str
    evidence: List[str]
    confidence: ConfidenceLevel  # VERY_LOW, LOW, MODERATE, HIGH, VERY_HIGH
    sources: List[Source]
    contradictions: List[str]
    tags: List[str]
)
```

### AgentResult
Result from agent execution:
```python
AgentResult(
    agent_name: str
    task_id: str
    status: str  # success, partial, failed, timeout
    findings: List[Finding]
    recommendations: str
    risks: List[str]
    duration_seconds: float
)
```

## Example Output

```
════════════════════════════════════════════════════════════════════════════════
🐝 PROYECTO COLMENA - INVESTIGATION SUMMARY
════════════════════════════════════════════════════════════════════════════════

Topic: AAPL
Status: completed
Duration: 12.45s
Timestamp: 2026-08-22T10:30:45.123456

────────────────────────────────────────────────────────────────────────────────
AGENT RESULTS:
────────────────────────────────────────────────────────────────────────────────
✅ research_agent
   Status: success
   Findings: 2
   Duration: 1.23s
   Confidence: MODERATE

✅ financial_agent
   Status: success
   Findings: 3
   Duration: 2.34s
   Confidence: HIGH

... [more agents] ...

────────────────────────────────────────────────────────────────────────────────
ERRORS: 0
────────────────────────────────────────────────────────────────────────────────
✅ All agents completed successfully
```

## Roadmap

### Phase 1 ✅ (MVP - Current)
- [x] Core architecture
- [x] 8 specialized agents
- [x] Orchestrator
- [x] CLI interface
- [ ] Complete test coverage

### Phase 2 (Completeness)
- [ ] Memory Agent
- [ ] Fact-Check Agent
- [ ] Database persistence
- [ ] Dashboard

### Phase 3 (Integration)
- [ ] PostgreSQL
- [ ] Redis caching
- [ ] n8n workflows
- [ ] Advanced integrations

### Phase 4 (Backtesting)
- [ ] Historical validation
- [ ] Performance metrics
- [ ] Strategy optimization

### Phase 5 (Paper Trading)
- [ ] Simulation engine
- [ ] Portfolio tracking
- [ ] Risk metrics

### Phase 6 (Real Trading)
- [ ] Broker integration
- [ ] Execution engine
- [ ] Strict risk controls

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- No hardcoded credentials
- Use type hints

## Disclaimer

⚠️ **IMPORTANT:**

This system is designed for **analysis and research purposes only**. It is not financial advice. Always:

1. Conduct your own due diligence
2. Consult with financial professionals
3. Understand the risks involved
4. Never trade with capital you cannot afford to lose
5. Test thoroughly before any real trading

The authors assume no liability for losses resulting from use of this system.

## License

MIT License - See LICENSE file

## Support

For issues, questions, or contributions:
- 🐛 [Report Issues](https://github.com/realmindllc-crypto/colmena-/issues)
- 💬 [Discussions](https://github.com/realmindllc-crypto/colmena-/discussions)
- 📖 [Documentation](docs/)

## Acknowledgments

Inspired by swarm intelligence and multiagent systems. Built with:
- OpenAI GPT-4
- yfinance
- Apify
- Python ecosystem

---

**PROYECTO COLMENA** - "In collaboration, we find wisdom."

*Made by realmindllc-crypto* 🐝
