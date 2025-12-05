"""Tests for pandas helpers"""

import pytest
import pandas as pd
from gen_ai_utils.data_science.pandas_helpers import (
    optimize_dataframe,
    profile_dataframe,
    missing_values_report
)


def test_optimize_dataframe(sample_dataframe):
    """Test DataFrame optimization"""
    optimized = optimize_dataframe(sample_dataframe, verbose=False)
    assert len(optimized) == len(sample_dataframe)
    assert list(optimized.columns) == list(sample_dataframe.columns)


def test_profile_dataframe(sample_dataframe):
    """Test DataFrame profiling"""
    profile = profile_dataframe(sample_dataframe)
    assert 'shape' in profile
    assert 'memory_usage_mb' in profile
    assert profile['shape'] == sample_dataframe.shape


def test_missing_values_report():
    """Test missing values reporting"""
    df = pd.DataFrame({
        'a': [1, 2, None, 4],
        'b': [None, None, 3, 4]
    })
    report = missing_values_report(df)
    assert len(report) == 2  # Both columns have missing values
