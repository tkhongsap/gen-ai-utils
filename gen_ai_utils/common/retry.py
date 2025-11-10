"""
Retry Utilities - Configurable retry logic with exponential backoff

Provides decorators and utilities for retrying failed operations with
configurable retry policies, exponential backoff, and jitter.
"""

import time
import random
from typing import Callable, Optional, Tuple, Type
from functools import wraps
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class RetryConfig:
    """Configuration for retry behavior"""
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True
    exceptions: Tuple[Type[Exception], ...] = (Exception,)


def calculate_delay(
    attempt: int,
    initial_delay: float,
    exponential_base: float,
    max_delay: float,
    jitter: bool
) -> float:
    """
    Calculate retry delay with exponential backoff

    Args:
        attempt: Current attempt number (0-indexed)
        initial_delay: Initial delay in seconds
        exponential_base: Base for exponential backoff
        max_delay: Maximum delay in seconds
        jitter: Whether to add random jitter

    Returns:
        Delay in seconds
    """
    delay = min(initial_delay * (exponential_base ** attempt), max_delay)

    if jitter:
        # Add random jitter between 0 and 50% of delay
        delay = delay * (0.5 + random.random() * 0.5)

    return delay


def retry(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None
):
    """
    Decorator to retry a function on failure with exponential backoff

    Args:
        max_attempts: Maximum number of attempts
        initial_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        exponential_base: Base for exponential backoff calculation
        jitter: Whether to add random jitter to delays
        exceptions: Tuple of exception types to catch and retry
        on_retry: Optional callback function called on each retry

    Returns:
        Decorated function

    Example:
        @retry(max_attempts=3, initial_delay=2.0)
        def fetch_data():
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt < max_attempts - 1:
                        delay = calculate_delay(
                            attempt,
                            initial_delay,
                            exponential_base,
                            max_delay,
                            jitter
                        )

                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {delay:.2f}s..."
                        )

                        if on_retry:
                            on_retry(e, attempt + 1)

                        time.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}: {str(e)}"
                        )

            # Re-raise the last exception after all retries are exhausted
            raise last_exception

        return wrapper

    return decorator


def retry_with_config(config: RetryConfig):
    """
    Decorator to retry a function using a RetryConfig object

    Args:
        config: RetryConfig instance with retry settings

    Returns:
        Decorated function

    Example:
        retry_config = RetryConfig(max_attempts=5, initial_delay=2.0)

        @retry_with_config(retry_config)
        def fetch_data():
            return requests.get(url).json()
    """
    return retry(
        max_attempts=config.max_attempts,
        initial_delay=config.initial_delay,
        max_delay=config.max_delay,
        exponential_base=config.exponential_base,
        jitter=config.jitter,
        exceptions=config.exceptions
    )


class Retryable:
    """Context manager for retrying operations"""

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        exceptions: Tuple[Type[Exception], ...] = (Exception,)
    ):
        """
        Initialize Retryable context manager

        Args:
            max_attempts: Maximum number of attempts
            initial_delay: Initial delay between retries
            max_delay: Maximum delay between retries
            exponential_base: Base for exponential backoff
            jitter: Whether to add random jitter
            exceptions: Tuple of exception types to catch
        """
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.exceptions = exceptions
        self.attempt = 0

    def __enter__(self):
        """Enter context"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context"""
        if exc_type is None:
            return True

        if not issubclass(exc_type, self.exceptions):
            return False

        self.attempt += 1

        if self.attempt < self.max_attempts:
            delay = calculate_delay(
                self.attempt - 1,
                self.initial_delay,
                self.exponential_base,
                self.max_delay,
                self.jitter
            )

            logger.warning(
                f"Attempt {self.attempt}/{self.max_attempts} failed: {str(exc_val)}. "
                f"Retrying in {delay:.2f}s..."
            )

            time.sleep(delay)
            return True  # Suppress the exception

        logger.error(f"All {self.max_attempts} attempts failed: {str(exc_val)}")
        return False  # Re-raise the exception


def retry_async(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator to retry an async function on failure with exponential backoff

    Args:
        max_attempts: Maximum number of attempts
        initial_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        exponential_base: Base for exponential backoff calculation
        jitter: Whether to add random jitter to delays
        exceptions: Tuple of exception types to catch and retry

    Returns:
        Decorated async function

    Example:
        @retry_async(max_attempts=3)
        async def fetch_data():
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            import asyncio

            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt < max_attempts - 1:
                        delay = calculate_delay(
                            attempt,
                            initial_delay,
                            exponential_base,
                            max_delay,
                            jitter
                        )

                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {delay:.2f}s..."
                        )

                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}: {str(e)}"
                        )

            raise last_exception

        return wrapper

    return decorator
