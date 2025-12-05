"""
Structured Logging - JSON and text logging with correlation IDs

Provides structured logging capabilities with support for JSON formatting,
correlation IDs for request tracing, and context management.
"""

import logging
import sys
import json
from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path
import traceback
from contextvars import ContextVar

# Context variable for correlation ID
correlation_id: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)


class JSONFormatter(logging.Formatter):
    """JSON log formatter"""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add correlation ID if available
        corr_id = correlation_id.get()
        if corr_id:
            log_data['correlation_id'] = corr_id

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }

        # Add extra fields
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data

        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """Colored text formatter for console output"""

    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors"""
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"

        # Add correlation ID if available
        corr_id = correlation_id.get()
        if corr_id:
            record.msg = f"[{corr_id[:8]}] {record.msg}"

        return super().format(record)


class StructuredLogger(logging.Logger):
    """Enhanced logger with structured logging support"""

    def _log_with_extra(
        self,
        level: int,
        msg: str,
        extra_data: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs
    ):
        """Log with extra structured data"""
        extra = kwargs.get('extra', {})
        if extra_data:
            extra['extra_data'] = extra_data
            kwargs['extra'] = extra
        super()._log(level, msg, args, **kwargs)

    def debug_with_data(self, msg: str, data: Optional[Dict[str, Any]] = None):
        """Debug log with structured data"""
        self._log_with_extra(logging.DEBUG, msg, data)

    def info_with_data(self, msg: str, data: Optional[Dict[str, Any]] = None):
        """Info log with structured data"""
        self._log_with_extra(logging.INFO, msg, data)

    def warning_with_data(self, msg: str, data: Optional[Dict[str, Any]] = None):
        """Warning log with structured data"""
        self._log_with_extra(logging.WARNING, msg, data)

    def error_with_data(self, msg: str, data: Optional[Dict[str, Any]] = None):
        """Error log with structured data"""
        self._log_with_extra(logging.ERROR, msg, data)


def setup_logger(
    name: str = "gen_ai_utils",
    level: str = "INFO",
    format: str = "json",
    file_path: Optional[str] = None,
    max_bytes: int = 10485760,
    backup_count: int = 5
) -> logging.Logger:
    """
    Setup a logger with specified configuration

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format: Log format ('json' or 'text')
        file_path: Optional file path for file logging
        max_bytes: Maximum file size before rotation
        backup_count: Number of backup files to keep

    Returns:
        Configured logger instance
    """
    # Set custom logger class
    logging.setLoggerClass(StructuredLogger)

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if format == "json":
        console_handler.setFormatter(JSONFormatter())
    else:
        console_handler.setFormatter(
            ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
    logger.addHandler(console_handler)

    # File handler (if specified)
    if file_path:
        from logging.handlers import RotatingFileHandler

        file_path_obj = Path(file_path)
        file_path_obj.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "gen_ai_utils") -> logging.Logger:
    """
    Get a logger instance

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def set_correlation_id(corr_id: str):
    """
    Set correlation ID for current context

    Args:
        corr_id: Correlation ID string
    """
    correlation_id.set(corr_id)


def get_correlation_id() -> Optional[str]:
    """
    Get current correlation ID

    Returns:
        Correlation ID or None
    """
    return correlation_id.get()


def clear_correlation_id():
    """Clear correlation ID from current context"""
    correlation_id.set(None)


class LogContext:
    """Context manager for correlation ID"""

    def __init__(self, corr_id: str):
        """
        Initialize log context

        Args:
            corr_id: Correlation ID
        """
        self.corr_id = corr_id
        self.previous_id = None

    def __enter__(self):
        """Enter context"""
        self.previous_id = get_correlation_id()
        set_correlation_id(self.corr_id)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context"""
        if self.previous_id:
            set_correlation_id(self.previous_id)
        else:
            clear_correlation_id()


# Default logger instance
default_logger = setup_logger()
