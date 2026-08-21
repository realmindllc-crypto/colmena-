"""Constants for PROYECTO COLMENA."""

# Agent names
AGENT_ORCHESTRATOR = "orchestrator"
AGENT_RESEARCH = "research_agent"
AGENT_FINANCIAL = "financial_agent"
AGENT_TECHNICAL = "technical_agent"
AGENT_SENTIMENT = "sentiment_agent"
AGENT_MACRO = "macro_agent"
AGENT_RISK = "risk_agent"
AGENT_DEVILS_ADVOCATE = "devils_advocate_agent"
AGENT_REPORT = "report_agent"

# Phase 2+
AGENT_FACT_CHECK = "fact_check_agent"
AGENT_MEMORY = "memory_agent"

# Task priorities
PRIORITY_CRITICAL = 1
PRIORITY_HIGH = 2
PRIORITY_MEDIUM = 5
PRIORITY_LOW = 8
PRIORITY_BACKGROUND = 10

# Status
STATUS_PENDING = "pending"
STATUS_RUNNING = "running"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"
STATUS_PARTIAL = "partial"
STATUS_TIMEOUT = "timeout"

# Timeouts (seconds)
DEFAULT_TASK_TIMEOUT = 300
FASTAST_AGENT_TIMEOUT = 60  # Research, tech
NORMAL_AGENT_TIMEOUT = 180  # Financial, sentiment
SLOW_AGENT_TIMEOUT = 300  # Complex analysis

# Confidence thresholds
CONF_THRESHOLD_ACTION = 0.75  # High confidence needed for recommendations
CONF_THRESHOLD_ALERT = 0.50   # Alert if below this

# Financial markets
MAJOR_US_INDICES = ["SPY", "QQQ", "IWM", "DIA"]
MAJOR_CRYPTO = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD"]

# LLM defaults
DEFAULT_LLM_TEMPERATURE = 0.7
DEFAULT_LLM_MAX_TOKENS = 2000
