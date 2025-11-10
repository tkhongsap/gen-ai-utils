"""
Caching Utilities - Memory and file-based caching with TTL support

Provides flexible caching implementations including in-memory and file-based
caching with time-to-live (TTL) support and automatic cleanup.
"""

import json
import pickle
import time
from typing import Any, Optional, Dict, Callable
from pathlib import Path
from abc import ABC, abstractmethod
import hashlib
from functools import wraps


class Cache(ABC):
    """Abstract base class for cache implementations"""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache"""
        pass

    @abstractmethod
    def delete(self, key: str):
        """Delete value from cache"""
        pass

    @abstractmethod
    def clear(self):
        """Clear all cache entries"""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        pass


class MemoryCache(Cache):
    """In-memory cache with TTL support"""

    def __init__(self, default_ttl: int = 3600):
        """
        Initialize memory cache

        Args:
            default_ttl: Default time-to-live in seconds
        """
        self.default_ttl = default_ttl
        self._cache: Dict[str, tuple] = {}  # {key: (value, expiry_time)}

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        if key not in self._cache:
            return None

        value, expiry_time = self._cache[key]

        # Check if expired
        if expiry_time and time.time() > expiry_time:
            del self._cache[key]
            return None

        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (None for no expiry)
        """
        ttl = ttl if ttl is not None else self.default_ttl
        expiry_time = time.time() + ttl if ttl > 0 else None
        self._cache[key] = (value, expiry_time)

    def delete(self, key: str):
        """
        Delete value from cache

        Args:
            key: Cache key
        """
        if key in self._cache:
            del self._cache[key]

    def clear(self):
        """Clear all cache entries"""
        self._cache.clear()

    def exists(self, key: str) -> bool:
        """
        Check if key exists in cache

        Args:
            key: Cache key

        Returns:
            True if key exists and not expired
        """
        return self.get(key) is not None

    def cleanup_expired(self):
        """Remove all expired entries"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry_time) in self._cache.items()
            if expiry_time and current_time > expiry_time
        ]
        for key in expired_keys:
            del self._cache[key]

    def size(self) -> int:
        """Get number of cached items"""
        return len(self._cache)


class FileCache(Cache):
    """File-based cache with TTL support"""

    def __init__(self, cache_dir: str = ".cache", default_ttl: int = 3600):
        """
        Initialize file cache

        Args:
            cache_dir: Directory for cache files
            default_ttl: Default time-to-live in seconds
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.default_ttl = default_ttl

    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path for key"""
        # Hash the key to create a safe filename
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        cache_path = self._get_cache_path(key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)

            value, expiry_time = data

            # Check if expired
            if expiry_time and time.time() > expiry_time:
                cache_path.unlink()
                return None

            return value
        except (IOError, pickle.PickleError, EOFError):
            # If file is corrupted, delete it
            if cache_path.exists():
                cache_path.unlink()
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (None for default)
        """
        cache_path = self._get_cache_path(key)
        ttl = ttl if ttl is not None else self.default_ttl
        expiry_time = time.time() + ttl if ttl > 0 else None

        try:
            with open(cache_path, 'wb') as f:
                pickle.dump((value, expiry_time), f)
        except (IOError, pickle.PickleError) as e:
            print(f"Error writing cache file: {e}")

    def delete(self, key: str):
        """
        Delete value from cache

        Args:
            key: Cache key
        """
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            cache_path.unlink()

    def clear(self):
        """Clear all cache entries"""
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink()

    def exists(self, key: str) -> bool:
        """
        Check if key exists in cache

        Args:
            key: Cache key

        Returns:
            True if key exists and not expired
        """
        return self.get(key) is not None

    def cleanup_expired(self):
        """Remove all expired cache files"""
        current_time = time.time()

        for cache_file in self.cache_dir.glob("*.cache"):
            try:
                with open(cache_file, 'rb') as f:
                    _, expiry_time = pickle.load(f)

                if expiry_time and current_time > expiry_time:
                    cache_file.unlink()
            except (IOError, pickle.PickleError, EOFError):
                # Remove corrupted files
                cache_file.unlink()

    def size(self) -> int:
        """Get number of cached items"""
        return len(list(self.cache_dir.glob("*.cache")))


def cached(
    cache: Optional[Cache] = None,
    ttl: Optional[int] = None,
    key_prefix: str = ""
):
    """
    Decorator for caching function results

    Args:
        cache: Cache instance to use (defaults to global MemoryCache)
        ttl: Time-to-live in seconds
        key_prefix: Prefix for cache keys

    Returns:
        Decorated function
    """
    if cache is None:
        cache = MemoryCache()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_parts = [key_prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)

            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl=ttl)
            return result

        # Add cache control methods to wrapper
        wrapper.cache_clear = lambda: cache.clear()
        wrapper.cache_info = lambda: {"size": cache.size() if hasattr(cache, 'size') else None}

        return wrapper

    return decorator


# Global cache instances
memory_cache = MemoryCache()
file_cache = FileCache()
