"""Utility functions for PROYECTO COLMENA."""

import logging
from datetime import datetime
from typing import Any, Dict
import json


def setup_logging(name: str, level: str = "INFO") -> logging.Logger:
    """Setup logger for a module."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Console handler
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def format_currency(value: float, symbol: str = "$") -> str:
    """Format value as currency."""
    return f"{symbol}{value:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format value as percentage."""
    return f"{value:{decimals}f}%"


def calculate_change(old: float, new: float) -> Dict[str, float]:
    """Calculate absolute and percentage change."""
    if old == 0:
        return {"absolute": 0, "percentage": 0}
    
    absolute = new - old
    percentage = (absolute / old) * 100
    
    return {
        "absolute": round(absolute, 4),
        "percentage": round(percentage, 2),
    }


def safe_json_dumps(obj: Any, indent: int = 2) -> str:
    """Safely convert object to JSON string."""
    try:
        return json.dumps(obj, indent=indent, default=str)
    except Exception as e:
        return f'{{"error": "Failed to serialize: {str(e)}"}}'  


def timestamp_to_iso(ts: Any) -> str:
    """Convert timestamp to ISO format."""
    if isinstance(ts, datetime):
        return ts.isoformat()
    return str(ts)
