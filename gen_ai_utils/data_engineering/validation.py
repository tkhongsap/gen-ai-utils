"""
Data Validation - Schema validation and data quality checks

Provides comprehensive data validation capabilities using Pydantic schemas,
data quality checks, and custom validation rules.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Callable, Tuple
from pydantic import BaseModel, validator, ValidationError
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ValidationResult:
    """Result of data validation"""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passed: bool = True

    def add_error(self, message: str):
        """Add an error"""
        self.errors.append(message)
        self.passed = False

    def add_warning(self, message: str):
        """Add a warning"""
        self.warnings.append(message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'passed': self.passed,
            'errors': self.errors,
            'warnings': self.warnings,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings)
        }


class DataValidator:
    """Comprehensive data validator"""

    def __init__(self):
        self.rules: List[Callable] = []

    def add_rule(self, rule: Callable) -> 'DataValidator':
        """
        Add a validation rule

        Args:
            rule: Validation function that returns (is_valid, errors)

        Returns:
            Self for chaining
        """
        self.rules.append(rule)
        return self

    def validate(self, data: pd.DataFrame) -> ValidationResult:
        """
        Validate data against all rules

        Args:
            data: DataFrame to validate

        Returns:
            ValidationResult
        """
        result = ValidationResult()

        for rule in self.rules:
            try:
                is_valid, errors = rule(data)
                if not is_valid:
                    for error in errors:
                        result.add_error(error)
            except Exception as e:
                result.add_error(f"Validation rule failed: {str(e)}")

        return result


def validate_schema(
    data: pd.DataFrame,
    schema: Dict[str, type],
    strict: bool = False
) -> Tuple[bool, List[str]]:
    """
    Validate DataFrame schema

    Args:
        data: DataFrame to validate
        schema: Dictionary mapping column names to expected types
        strict: Whether to require exact column match

    Returns:
        Tuple of (is_valid, errors)
    """
    errors = []

    # Check for missing columns
    expected_cols = set(schema.keys())
    actual_cols = set(data.columns)

    missing_cols = expected_cols - actual_cols
    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")

    # Check for extra columns (if strict mode)
    if strict:
        extra_cols = actual_cols - expected_cols
        if extra_cols:
            errors.append(f"Extra columns: {extra_cols}")

    # Check column types
    for col, expected_type in schema.items():
        if col in data.columns:
            actual_type = data[col].dtype

            # Type mapping
            type_matches = {
                int: ['int64', 'int32', 'int16', 'int8'],
                float: ['float64', 'float32', 'float16'],
                str: ['object'],
                bool: ['bool'],
                datetime: ['datetime64[ns]']
            }

            expected_types = type_matches.get(expected_type, [str(expected_type)])

            if str(actual_type) not in expected_types:
                errors.append(
                    f"Column '{col}' has type {actual_type}, expected {expected_type}"
                )

    is_valid = len(errors) == 0
    return is_valid, errors


def check_data_quality(
    data: pd.DataFrame,
    checks: Optional[Dict[str, Any]] = None
) -> Tuple[bool, List[str]]:
    """
    Perform data quality checks

    Args:
        data: DataFrame to check
        checks: Dictionary of quality checks to perform

    Returns:
        Tuple of (is_valid, errors)
    """
    if checks is None:
        checks = {
            'missing_values': True,
            'duplicates': True,
            'outliers': False,
            'data_types': True
        }

    errors = []

    # Missing values check
    if checks.get('missing_values'):
        missing = data.isnull().sum()
        missing_cols = missing[missing > 0]
        if len(missing_cols) > 0:
            for col, count in missing_cols.items():
                pct = (count / len(data)) * 100
                errors.append(f"Column '{col}' has {count} ({pct:.2f}%) missing values")

    # Duplicates check
    if checks.get('duplicates'):
        dup_count = data.duplicated().sum()
        if dup_count > 0:
            errors.append(f"Found {dup_count} duplicate rows")

    # Data types check
    if checks.get('data_types'):
        for col in data.columns:
            if data[col].dtype == 'object':
                # Check if numeric values stored as strings
                try:
                    pd.to_numeric(data[col].dropna().head(100))
                    errors.append(f"Column '{col}' appears to be numeric but stored as string")
                except:
                    pass

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_range(
    data: pd.DataFrame,
    column: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None
) -> Tuple[bool, List[str]]:
    """
    Validate that column values are within range

    Args:
        data: DataFrame to check
        column: Column name
        min_value: Minimum allowed value
        max_value: Maximum allowed value

    Returns:
        Tuple of (is_valid, errors)
    """
    errors = []

    if column not in data.columns:
        errors.append(f"Column '{column}' not found")
        return False, errors

    if min_value is not None:
        below_min = (data[column] < min_value).sum()
        if below_min > 0:
            errors.append(f"Column '{column}' has {below_min} values below minimum {min_value}")

    if max_value is not None:
        above_max = (data[column] > max_value).sum()
        if above_max > 0:
            errors.append(f"Column '{column}' has {above_max} values above maximum {max_value}")

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_unique(
    data: pd.DataFrame,
    columns: List[str]
) -> Tuple[bool, List[str]]:
    """
    Validate that specified columns have unique values

    Args:
        data: DataFrame to check
        columns: List of column names

    Returns:
        Tuple of (is_valid, errors)
    """
    errors = []

    for col in columns:
        if col not in data.columns:
            errors.append(f"Column '{col}' not found")
            continue

        duplicates = data[col].duplicated().sum()
        if duplicates > 0:
            errors.append(f"Column '{col}' has {duplicates} duplicate values")

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_not_null(
    data: pd.DataFrame,
    columns: List[str]
) -> Tuple[bool, List[str]]:
    """
    Validate that specified columns have no null values

    Args:
        data: DataFrame to check
        columns: List of column names

    Returns:
        Tuple of (is_valid, errors)
    """
    errors = []

    for col in columns:
        if col not in data.columns:
            errors.append(f"Column '{col}' not found")
            continue

        null_count = data[col].isnull().sum()
        if null_count > 0:
            errors.append(f"Column '{col}' has {null_count} null values")

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_pattern(
    data: pd.DataFrame,
    column: str,
    pattern: str
) -> Tuple[bool, List[str]]:
    """
    Validate that column values match a regex pattern

    Args:
        data: DataFrame to check
        column: Column name
        pattern: Regex pattern

    Returns:
        Tuple of (is_valid, errors)
    """
    errors = []

    if column not in data.columns:
        errors.append(f"Column '{column}' not found")
        return False, errors

    # Check pattern match
    matches = data[column].astype(str).str.match(pattern)
    non_matches = (~matches).sum()

    if non_matches > 0:
        errors.append(f"Column '{column}' has {non_matches} values not matching pattern")

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_allowed_values(
    data: pd.DataFrame,
    column: str,
    allowed_values: List[Any]
) -> Tuple[bool, List[str]]:
    """
    Validate that column values are in allowed list

    Args:
        data: DataFrame to check
        column: Column name
        allowed_values: List of allowed values

    Returns:
        Tuple of (is_valid, errors)
    """
    errors = []

    if column not in data.columns:
        errors.append(f"Column '{column}' not found")
        return False, errors

    invalid = ~data[column].isin(allowed_values)
    invalid_count = invalid.sum()

    if invalid_count > 0:
        unique_invalid = data[column][invalid].unique()
        errors.append(
            f"Column '{column}' has {invalid_count} values not in allowed list. "
            f"Invalid values: {list(unique_invalid[:10])}"
        )

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_relationships(
    data: pd.DataFrame,
    foreign_key: str,
    reference_data: pd.DataFrame,
    reference_key: str
) -> Tuple[bool, List[str]]:
    """
    Validate foreign key relationships

    Args:
        data: DataFrame with foreign key
        foreign_key: Foreign key column name
        reference_data: Reference DataFrame
        reference_key: Reference key column name

    Returns:
        Tuple of (is_valid, errors)
    """
    errors = []

    if foreign_key not in data.columns:
        errors.append(f"Foreign key column '{foreign_key}' not found")
        return False, errors

    if reference_key not in reference_data.columns:
        errors.append(f"Reference key column '{reference_key}' not found")
        return False, errors

    # Check for orphaned records
    orphaned = ~data[foreign_key].isin(reference_data[reference_key])
    orphaned_count = orphaned.sum()

    if orphaned_count > 0:
        errors.append(f"Found {orphaned_count} orphaned records in '{foreign_key}'")

    is_valid = len(errors) == 0
    return is_valid, errors


def create_validation_report(
    data: pd.DataFrame,
    validations: List[Callable]
) -> Dict[str, Any]:
    """
    Create comprehensive validation report

    Args:
        data: DataFrame to validate
        validations: List of validation functions

    Returns:
        Validation report dictionary
    """
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_rows': len(data),
        'total_columns': len(data.columns),
        'validations': [],
        'passed': True
    }

    for validation in validations:
        is_valid, errors = validation(data)

        report['validations'].append({
            'validation': validation.__name__,
            'passed': is_valid,
            'errors': errors
        })

        if not is_valid:
            report['passed'] = False

    return report
