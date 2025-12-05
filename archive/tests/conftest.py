"""Pytest configuration and fixtures"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path


@pytest.fixture
def sample_dataframe():
    """Sample DataFrame for testing"""
    return pd.DataFrame({
        'id': range(100),
        'value': np.random.randn(100),
        'category': np.random.choice(['A', 'B', 'C'], 100),
        'date': pd.date_range('2024-01-01', periods=100)
    })


@pytest.fixture
def sample_embeddings():
    """Sample embeddings for testing"""
    return [[float(x) for x in np.random.randn(384)] for _ in range(10)]


@pytest.fixture
def temp_dir(tmp_path):
    """Temporary directory for test files"""
    return tmp_path


@pytest.fixture
def mock_api_key():
    """Mock API key for testing"""
    return "test_api_key_12345"
