"""
Gen AI Utils - Comprehensive utilities for AI/ML, Data Science, and Data Engineering

A professional toolkit providing:
- OpenAI Assistant integrations
- Document parsing with LlamaParse
- Data science utilities (pandas, visualization, statistics)
- Data engineering tools (ETL, batch processing, validation)
- AI/ML engineering utilities (embeddings, vector stores, evaluation)
"""

__version__ = "1.0.0"
__author__ = "Gen AI Utils Team"

# Import core modules for easy access
from gen_ai_utils.common import config, logging, cache, retry

__all__ = [
    "config",
    "logging",
    "cache",
    "retry",
]
