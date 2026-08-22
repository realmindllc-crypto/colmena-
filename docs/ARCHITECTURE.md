# 🐝 PROYECTO COLMENA - ARCHITECTURE GUIDE

## System Overview

PROYECTO COLMENA is a **multiagent AI system** designed for comprehensive financial and market analysis. The architecture follows a **hierarchical coordination model** where specialized agents work together under orchestration.

```
┌─────────────────────────────────────────┐
│      ORCHESTRATOR (Central Hub)         │
│  - Plans investigation                  │
│  - Coordinates agents                   │
│  - Aggregates results                   │
│  - Detects contradictions               │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
     PHASE 1    PHASE 2    PHASE 3
  (Research)  (Analysis)  (Evaluation)
        │          │          │
   ┌────▼──┐  ┌────┴────┬───┴────┐  ┌──────────┬──────────┐
   │Research│  │Financial│Technical│  │Risk      │Devil's   │
   │Agent   │  │Agent    │Agent    │  │Agent     │Advocate  │
   └────────┘  └─────────┴────────┘  │          │          │
                                     └──────────┴──────────┘
        ┌──────────────────┐
        │                  │
        │  Sentiment Agent │
        │  Macro Agent     │
        │                  │
        └──────────────────┘

                   │
        ┌──────────▼──────────┐
        │   REPORT AGENT      │
        │  - Synthesizes      │
        │  - Generates report │
        └─────────────────────┘
```

## Layer Architecture

### 1. **Shared Layer** (`shared/`)

Central data models and utilities:

```
shared/
├── models.py         # Data classes (Investigation, Finding, AgentResult, etc.)
├── constants.py      # System constants (agent names, priorities, timeouts)
├── exceptions.py     # Custom exceptions
├── utils.py          # Utility functions (logging, formatting, etc.)
└── __init__.py
```

**Key Models:**
- `Investigation`: Complete investigation object
- `Finding`: Individual finding with evidence and confidence
- `AgentResult`: Agent execution result
- `AgentTask`: Task assigned to an agent
- `ConfidenceLevel`: Enum for confidence (VERY_LOW to VERY_HIGH)
- `SourceType`: Enum for source types

### 2. **Core Layer** (`core/`)

Fundamental system components:

```
core/
├── event_system.py   # Event emission and subscription (SQLite backed)
├── llm_client.py     # OpenAI API wrapper
├── data_fetcher.py   # Base fetchers for external data
└── __init__.py
```

**Components:**
- `EventSystem`: Persistent event logging and pub/sub
- `LLMClient`: Chat, analysis, and JSON extraction from OpenAI
- `DataFetcher`: Base class for data retrieval

### 3. **Agents Layer** (`agents/`)

Specialized analysis agents:

```
agents/
├── base_agent.py              # Abstract base class
├── research/
│   ├── research_agent.py      # Information gathering
│   └── __init__.py
├── financial/
│   ├── financial_agent.py     # Fundamental analysis
│   └── __init__.py
├── technical/
│   ├── technical_agent.py     # Technical indicators
│   └── __init__.py
├── sentiment/
│   ├── sentiment_agent.py     # Sentiment analysis
│   └── __init__.py
├── macro/
│   ├── macro_agent.py         # Macro context
│   └── __init__.py
├── risk/
│   ├── risk_agent.py          # Risk assessment
│   └── __init__.py
├── devils_advocate/
│   ├── devils_advocate_agent.py  # Adversarial analysis
│   └── __init__.py
├── report/
│   ├── report_agent.py        # Report generation
│   └── __init__.py
├── orchestrator/
│   ├── orchestrator.py        # Central coordinator
│   └── __init__.py
└── __init__.py
```

**Agent Base Class:**
```python
class BaseAgent(ABC):
    def __init__(self, name: str, description: str)
    @abstractmethod
    def analyze(self, task: AgentTask, context: Dict) -> AgentResult
    def execute(self, task: AgentTask, context: Dict) -> AgentResult  # With error handling
    def get_stats(self) -> Dict  # Execution statistics
```

### 4. **Integrations Layer** (`integrations/`)

External API connections:

```
integrations/
├── apify/
│   ├── apify_client.py        # Web scraping
│   └── __init__.py
├── financial_data/
│   ├── yfinance_connector.py  # yfinance API
│   └── __init__.py
└── __init__.py
```

**Available Integrations (Phase 1):**
- `yfinance`: Free historical and real-time financial data
- `Apify`: Web scraping and data collection
- (Phase 3+) PostgreSQL, Redis, n8n

### 5. **Scripts & CLI** (`scripts/`)

```
scripts/
└── run_investigation.py       # CLI entry point
```

**CLI Commands:**
```bash
python scripts/run_investigation.py investigate AAPL
python scripts/run_investigation.py health
python scripts/run_investigation.py version
```

### 6. **Tests** (`tests/`)

```
tests/
├── conftest.py               # Pytest fixtures
├── test_models.py            # Model tests
├── test_orchestrator.py      # Orchestrator tests
└── test_agents.py            # Agent tests
```

## Execution Flow

### Investigation Lifecycle

```
1. CREATE INVESTIGATION
   └─> Investigation(topic, objective)

2. ORCHESTRATOR.execute_investigation()
   ├─> plan_investigation()
   │   └─> Create AgentTasks ordered by priority
   │
   ├─> Phase 1: Research (CRITICAL priority)
   │   └─> ResearchAgent.execute()
   │       └─> AgentResult with findings
   │
   ├─> Phase 2: Parallel Analysis (HIGH priority)
   │   ├─> FinancialAgent.execute()
   │   ├─> TechnicalAgent.execute()
   │   ├─> SentimentAgent.execute()
   │   └─> MacroAgent.execute()
   │       └─> Each returns AgentResult
   │
   ├─> Phase 3: Evaluation (MEDIUM priority)
   │   ├─> RiskAgent.execute() (sees all previous results)
   │   └─> DevilsAdvocateAgent.execute() (refutes conclusions)
   │       └─> Each returns AgentResult
   │
   ├─> Phase 4: Reporting
   │   └─> ReportAgent.execute()
   │       └─> Generates markdown report
   │
   ├─> detect_contradictions()
   │   └─> Compare findings for conflicts
   │
   └─> generate_final_report()
       └─> Summary with agent results

3. RETURN Investigation
   ├─> status: "completed"
   ├─> agent_results: {agent_name: AgentResult}
   ├─> final_report: markdown summary
   └─> errors: list of any errors
```

## Agent Design Pattern

All agents follow this pattern:

```python
class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="my_agent",
            description="My agent description"
        )
    
    def analyze(self, task: AgentTask, context: Dict) -> AgentResult:
        # Extract context
        topic = context.get("investigation_topic", "")
        previous_results = context.get("previous_results", {})
        
        findings = []
        
        # Do analysis
        # ... fetch data, analyze, create Finding objects
        
        return AgentResult(
            agent_name=self.name,
            task_id=task.id,
            objective=task.objective,
            findings=findings,
            recommendations="...",
            risks=["..."]
        )
```

## Data Flow Example

```
Investigation: AAPL
    │
    ├─> ResearchAgent finds: "Apple is a tech company..."
    │   └─> Finding(confidence=MODERATE, sources=[...])
    │
    ├─> FinancialAgent finds: "P/E ratio 25.5, strong fundamentals"
    │   └─> Finding(confidence=HIGH, sources=[yfinance])
    │
    ├─> TechnicalAgent finds: "Price above 200-day MA, bullish"
    │   └─> Finding(confidence=MODERATE, sources=[price_data])
    │
    ├─> SentimentAgent finds: "Positive news sentiment"
    │   └─> Finding(confidence=LOW, sources=[news])
    │
    ├─> MacroAgent finds: "Interest rates rising, headwind for tech"
    │   └─> Finding(confidence=MODERATE, sources=[macro_data])
    │
    ├─> RiskAgent: "Risks: regulation, competition, rate sensitivity"
    │   └─> Finding with risk_list
    │
    ├─> DevilsAdvocate: "Valuation expensive, margin could compress"
    │   └─> Finding with contradictions
    │
    └─> ReportAgent aggregates all → Markdown report
```

## Configuration

### Environment Variables (`.env`)

```bash
# LLM
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.7

# Integrations
APIFY_TOKEN=...
YFINANCE_ENABLED=true

# Database
DATABASE_URL=sqlite:///./colmena.db

# System
DEBUG=false
LOG_LEVEL=INFO
```

## Priority System

```
PRIORITY_CRITICAL = 1    # Research (must complete first)
PRIORITY_HIGH = 2        # Parallel analysis
PRIORITY_MEDIUM = 5      # Evaluation & synthesis
PRIORITY_LOW = 8         # Non-essential
PRIORITY_BACKGROUND = 10 # Can run anytime
```

Agents execute in priority order. Higher priority (lower number) agents run first.

## Confidence Levels

```
VERY_HIGH (0.95-1.00)  ✅ High certainty, act on this
HIGH      (0.75-0.95)  ✅ Good confidence, reasonable to use
MODERATE  (0.50-0.75)  ⚠️  Medium confidence, needs verification
LOW       (0.25-0.50)  ⚠️  Low confidence, speculative
VERY_LOW  (0.00-0.25)  ❌ Very low confidence, ignore
```

## Extending the System

### Adding a New Agent

1. Create `agents/myagent/myagent.py`:
```python
from agents.base_agent import BaseAgent
from shared.models import AgentResult, AgentTask, Finding

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__("my_agent", "My agent description")
    
    def analyze(self, task: AgentTask, context: Dict) -> AgentResult:
        # Implementation
        pass
```

2. Register in Orchestrator:
```python
agents = {
    "my_agent": MyAgent(),
    # ... other agents
}
```

3. Add to Phase 2/3 in `orchestrator.plan_investigation()`

### Adding a New Integration

1. Create `integrations/myservice/client.py`
2. Implement connector class
3. Import in agents that need it

## Performance Considerations

- **Parallelization**: Phase 2 agents run in parallel (ThreadPoolExecutor)
- **Timeouts**: Each task has configurable timeout (default 300s)
- **Caching**: Future phases will add Redis caching
- **Database**: SQLite in Phase 1, PostgreSQL in Phase 3+

## Security

- ✅ API keys in `.env`, never in code
- ✅ `.gitignore` excludes sensitive files
- ✅ No automatic trading (Phase 1-5 analysis only)
- ✅ All decisions logged for audit

## Next Phases

**Phase 2**: Memory agent, fact-checking, persistence  
**Phase 3**: Database, n8n integration, advanced features  
**Phase 4**: Backtesting, optimization  
**Phase 5**: Paper trading simulation  
**Phase 6**: Real trading (with strict controls)  

---

*For questions or issues, see DEVELOPMENT.md*
