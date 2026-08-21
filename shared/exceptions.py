"""Custom exceptions for PROYECTO COLMENA."""


class ColmenaException(Exception):
    """Base exception for PROYECTO COLMENA."""
    pass


class AgentException(ColmenaException):
    """Exception from an agent."""
    pass


class OrchestratorException(ColmenaException):
    """Exception from orchestrator."""
    pass


class DataFetchException(ColmenaException):
    """Exception fetching external data."""
    pass


class LLMException(ColmenaException):
    """Exception from LLM API."""
    pass


class ConfigException(ColmenaException):
    """Configuration error."""
    pass


class ValidationException(ColmenaException):
    """Data validation error."""
    pass


class TimeoutException(ColmenaException):
    """Task timeout."""
    pass
