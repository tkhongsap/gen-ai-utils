"""Tests for data validation"""

import pytest
import pandas as pd
from gen_ai_utils.data_engineering.validation import (
    validate_schema,
    validate_range,
    validate_not_null
)


def test_validate_schema():
    """Test schema validation"""
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['A', 'B', 'C'],
        'value': [1.0, 2.0, 3.0]
    })

    schema = {
        'id': int,
        'name': str,
        'value': float
    }

    is_valid, errors = validate_schema(df, schema)
    assert is_valid
    assert len(errors) == 0


def test_validate_range():
    """Test range validation"""
    df = pd.DataFrame({'value': [1, 2, 3, 4, 5]})

    is_valid, errors = validate_range(df, 'value', min_value=0, max_value=10)
    assert is_valid

    is_valid, errors = validate_range(df, 'value', min_value=3, max_value=10)
    assert not is_valid


def test_validate_not_null():
    """Test not null validation"""
    df = pd.DataFrame({
        'required': [1, 2, 3],
        'optional': [1, None, 3]
    })

    is_valid, errors = validate_not_null(df, ['required'])
    assert is_valid

    is_valid, errors = validate_not_null(df, ['optional'])
    assert not is_valid
