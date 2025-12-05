"""
Pandas Helpers - Utilities for efficient DataFrame operations

Provides utilities for memory optimization, chunked reading, profiling,
and common DataFrame operations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Iterator, Any
from pathlib import Path


def optimize_dataframe(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Optimize DataFrame memory usage by downcasting numeric types

    Args:
        df: DataFrame to optimize
        verbose: Whether to print optimization results

    Returns:
        Optimized DataFrame
    """
    start_mem = df.memory_usage().sum() / 1024**2

    for col in df.columns:
        col_type = df[col].dtype

        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()

            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)

            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)

    end_mem = df.memory_usage().sum() / 1024**2

    if verbose:
        print(f'Memory usage decreased from {start_mem:.2f} MB to {end_mem:.2f} MB '
              f'({100 * (start_mem - end_mem) / start_mem:.1f}% reduction)')

    return df


def chunked_read_csv(
    filepath: str,
    chunksize: int = 10000,
    **kwargs
) -> Iterator[pd.DataFrame]:
    """
    Read CSV file in chunks for memory efficiency

    Args:
        filepath: Path to CSV file
        chunksize: Number of rows per chunk
        **kwargs: Additional arguments for pd.read_csv

    Yields:
        DataFrame chunks
    """
    for chunk in pd.read_csv(filepath, chunksize=chunksize, **kwargs):
        yield chunk


def profile_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a comprehensive profile of a DataFrame

    Args:
        df: DataFrame to profile

    Returns:
        Dictionary with profiling information
    """
    profile = {
        'shape': df.shape,
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'column_types': df.dtypes.value_counts().to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
        'categorical_columns': df.select_dtypes(include=['object', 'category']).columns.tolist(),
        'datetime_columns': df.select_dtypes(include=['datetime64']).columns.tolist(),
    }

    # Add statistics for numeric columns
    if profile['numeric_columns']:
        profile['numeric_stats'] = df[profile['numeric_columns']].describe().to_dict()

    return profile


def memory_usage_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get detailed memory usage summary for DataFrame

    Args:
        df: DataFrame to analyze

    Returns:
        DataFrame with memory usage details per column
    """
    mem_usage = df.memory_usage(deep=True)

    summary = pd.DataFrame({
        'Column': mem_usage.index,
        'Memory (MB)': mem_usage.values / 1024**2,
        'Data Type': df.dtypes.values,
        'Percentage': (mem_usage.values / mem_usage.sum() * 100)
    })

    summary = summary.sort_values('Memory (MB)', ascending=False).reset_index(drop=True)

    return summary


def convert_to_category(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    threshold: float = 0.5
) -> pd.DataFrame:
    """
    Convert object columns to category type for memory efficiency

    Args:
        df: DataFrame to convert
        columns: Specific columns to convert (None for auto-detection)
        threshold: Cardinality threshold (ratio of unique values to total)

    Returns:
        DataFrame with converted columns
    """
    df = df.copy()

    if columns is None:
        # Auto-detect columns with low cardinality
        object_cols = df.select_dtypes(include=['object']).columns
        columns = [
            col for col in object_cols
            if df[col].nunique() / len(df) < threshold
        ]

    for col in columns:
        df[col] = df[col].astype('category')

    return df


def missing_values_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate detailed missing values report

    Args:
        df: DataFrame to analyze

    Returns:
        DataFrame with missing value statistics
    """
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100

    report = pd.DataFrame({
        'Column': missing.index,
        'Missing Count': missing.values,
        'Missing Percentage': missing_pct.values,
        'Data Type': df.dtypes.values
    })

    report = report[report['Missing Count'] > 0].sort_values(
        'Missing Percentage',
        ascending=False
    ).reset_index(drop=True)

    return report


def quick_summary(df: pd.DataFrame) -> None:
    """
    Print a quick summary of DataFrame

    Args:
        df: DataFrame to summarize
    """
    print("=" * 60)
    print("DATAFRAME QUICK SUMMARY")
    print("=" * 60)
    print(f"\nShape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"\nData Types:")
    print(df.dtypes.value_counts())
    print(f"\nMissing Values: {df.isnull().sum().sum():,} ({df.isnull().sum().sum() / df.size * 100:.2f}%)")
    print(f"Duplicate Rows: {df.duplicated().sum():,}")
    print("\nFirst Few Rows:")
    print(df.head())
    print("=" * 60)


def split_features_target(
    df: pd.DataFrame,
    target_column: str,
    drop_columns: Optional[List[str]] = None
) -> tuple:
    """
    Split DataFrame into features and target

    Args:
        df: DataFrame to split
        target_column: Name of target column
        drop_columns: Additional columns to drop from features

    Returns:
        Tuple of (X, y) where X is features and y is target
    """
    y = df[target_column].copy()

    drop_cols = [target_column]
    if drop_columns:
        drop_cols.extend(drop_columns)

    X = df.drop(columns=drop_cols)

    return X, y


def detect_constant_columns(
    df: pd.DataFrame,
    threshold: float = 0.99
) -> List[str]:
    """
    Detect columns with constant or near-constant values

    Args:
        df: DataFrame to analyze
        threshold: Threshold for value frequency

    Returns:
        List of constant column names
    """
    constant_cols = []

    for col in df.columns:
        if df[col].value_counts().iloc[0] / len(df) > threshold:
            constant_cols.append(col)

    return constant_cols


def safe_merge(
    left: pd.DataFrame,
    right: pd.DataFrame,
    on: Optional[str] = None,
    how: str = 'inner',
    validate: Optional[str] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Safely merge DataFrames with validation and logging

    Args:
        left: Left DataFrame
        right: Right DataFrame
        on: Column(s) to merge on
        how: Type of merge ('inner', 'outer', 'left', 'right')
        validate: Merge validation type
        **kwargs: Additional arguments for pd.merge

    Returns:
        Merged DataFrame
    """
    initial_len = len(left)

    result = pd.merge(left, right, on=on, how=how, validate=validate, **kwargs)

    print(f"Merge completed:")
    print(f"  Left: {len(left):,} rows")
    print(f"  Right: {len(right):,} rows")
    print(f"  Result: {len(result):,} rows")
    print(f"  Change: {len(result) - initial_len:+,} rows")

    return result
