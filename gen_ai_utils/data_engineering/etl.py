"""
ETL Pipeline - Extract, Transform, Load utilities

Provides a framework for building ETL pipelines with support for
data extraction, transformation, validation, and loading.
"""

import pandas as pd
from typing import Callable, List, Dict, Any, Optional, Union
from pathlib import Path
import logging
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ETLResult:
    """Result of an ETL operation"""
    success: bool
    records_processed: int
    records_failed: int
    duration_seconds: float
    errors: List[str]
    metadata: Dict[str, Any]


class ETLPipeline:
    """ETL Pipeline for data processing workflows"""

    def __init__(self, name: str, log_dir: Optional[str] = None):
        """
        Initialize ETL Pipeline

        Args:
            name: Pipeline name
            log_dir: Directory for ETL logs
        """
        self.name = name
        self.log_dir = Path(log_dir) if log_dir else None
        self.extractors: List[Callable] = []
        self.transformers: List[Callable] = []
        self.validators: List[Callable] = []
        self.loaders: List[Callable] = []
        self.error_handlers: List[Callable] = []

        if self.log_dir:
            self.log_dir.mkdir(parents=True, exist_ok=True)

    def add_extractor(self, func: Callable) -> 'ETLPipeline':
        """Add an extractor function"""
        self.extractors.append(func)
        return self

    def add_transformer(self, func: Callable) -> 'ETLPipeline':
        """Add a transformer function"""
        self.transformers.append(func)
        return self

    def add_validator(self, func: Callable) -> 'ETLPipeline':
        """Add a validator function"""
        self.validators.append(func)
        return self

    def add_loader(self, func: Callable) -> 'ETLPipeline':
        """Add a loader function"""
        self.loaders.append(func)
        return self

    def add_error_handler(self, func: Callable) -> 'ETLPipeline':
        """Add an error handler function"""
        self.error_handlers.append(func)
        return self

    def extract(self, **kwargs) -> Any:
        """
        Execute extraction phase

        Args:
            **kwargs: Arguments for extractors

        Returns:
            Extracted data
        """
        logger.info(f"[{self.name}] Starting extraction phase")

        data = None
        for extractor in self.extractors:
            try:
                logger.info(f"Running extractor: {extractor.__name__}")
                data = extractor(**kwargs) if data is None else extractor(data, **kwargs)
            except Exception as e:
                logger.error(f"Extraction failed: {str(e)}")
                self._handle_error(e, 'extraction')
                raise

        logger.info(f"[{self.name}] Extraction completed")
        return data

    def transform(self, data: Any) -> Any:
        """
        Execute transformation phase

        Args:
            data: Data to transform

        Returns:
            Transformed data
        """
        logger.info(f"[{self.name}] Starting transformation phase")

        for transformer in self.transformers:
            try:
                logger.info(f"Running transformer: {transformer.__name__}")
                data = transformer(data)
            except Exception as e:
                logger.error(f"Transformation failed: {str(e)}")
                self._handle_error(e, 'transformation')
                raise

        logger.info(f"[{self.name}] Transformation completed")
        return data

    def validate(self, data: Any) -> tuple:
        """
        Execute validation phase

        Args:
            data: Data to validate

        Returns:
            Tuple of (is_valid, errors)
        """
        logger.info(f"[{self.name}] Starting validation phase")

        errors = []
        for validator in self.validators:
            try:
                logger.info(f"Running validator: {validator.__name__}")
                is_valid, validation_errors = validator(data)

                if not is_valid:
                    errors.extend(validation_errors)
            except Exception as e:
                logger.error(f"Validation failed: {str(e)}")
                errors.append(str(e))

        is_valid = len(errors) == 0
        logger.info(f"[{self.name}] Validation {'passed' if is_valid else 'failed'}")

        return is_valid, errors

    def load(self, data: Any, **kwargs) -> bool:
        """
        Execute loading phase

        Args:
            data: Data to load
            **kwargs: Arguments for loaders

        Returns:
            True if successful
        """
        logger.info(f"[{self.name}] Starting loading phase")

        for loader in self.loaders:
            try:
                logger.info(f"Running loader: {loader.__name__}")
                loader(data, **kwargs)
            except Exception as e:
                logger.error(f"Loading failed: {str(e)}")
                self._handle_error(e, 'loading')
                raise

        logger.info(f"[{self.name}] Loading completed")
        return True

    def run(self, validate_data: bool = True, **kwargs) -> ETLResult:
        """
        Run the complete ETL pipeline

        Args:
            validate_data: Whether to run validation
            **kwargs: Arguments for pipeline stages

        Returns:
            ETLResult with execution details
        """
        start_time = datetime.now()
        errors = []
        records_processed = 0
        records_failed = 0

        try:
            # Extract
            data = self.extract(**kwargs)

            # Transform
            data = self.transform(data)

            # Count records
            if isinstance(data, pd.DataFrame):
                records_processed = len(data)
            elif isinstance(data, list):
                records_processed = len(data)

            # Validate
            if validate_data and self.validators:
                is_valid, validation_errors = self.validate(data)
                if not is_valid:
                    errors.extend(validation_errors)
                    records_failed = records_processed
                    records_processed = 0
                    return ETLResult(
                        success=False,
                        records_processed=records_processed,
                        records_failed=records_failed,
                        duration_seconds=(datetime.now() - start_time).total_seconds(),
                        errors=errors,
                        metadata={'pipeline': self.name}
                    )

            # Load
            self.load(data, **kwargs)

            duration = (datetime.now() - start_time).total_seconds()

            return ETLResult(
                success=True,
                records_processed=records_processed,
                records_failed=records_failed,
                duration_seconds=duration,
                errors=errors,
                metadata={'pipeline': self.name}
            )

        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            errors.append(str(e))
            duration = (datetime.now() - start_time).total_seconds()

            return ETLResult(
                success=False,
                records_processed=records_processed,
                records_failed=records_processed,
                duration_seconds=duration,
                errors=errors,
                metadata={'pipeline': self.name}
            )

    def _handle_error(self, error: Exception, phase: str):
        """Handle errors using registered handlers"""
        for handler in self.error_handlers:
            try:
                handler(error, phase, self.name)
            except Exception as e:
                logger.error(f"Error handler failed: {str(e)}")


def transform(func: Callable) -> Callable:
    """
    Decorator for transformation functions with error handling

    Args:
        func: Transformation function

    Returns:
        Wrapped function
    """
    def wrapper(data: Any, *args, **kwargs) -> Any:
        try:
            return func(data, *args, **kwargs)
        except Exception as e:
            logger.error(f"Transformation error in {func.__name__}: {str(e)}")
            raise

    return wrapper


# Common ETL transformations
@transform
def filter_null_values(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Remove rows with null values"""
    if columns:
        return df.dropna(subset=columns)
    return df.dropna()


@transform
def deduplicate(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Remove duplicate rows"""
    return df.drop_duplicates(subset=columns)


@transform
def rename_columns(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """Rename columns"""
    return df.rename(columns=mapping)


@transform
def select_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Select specific columns"""
    return df[columns]


@transform
def add_timestamp(df: pd.DataFrame, column_name: str = 'processed_at') -> pd.DataFrame:
    """Add processing timestamp"""
    df[column_name] = datetime.now()
    return df


@transform
def convert_types(df: pd.DataFrame, type_mapping: Dict[str, str]) -> pd.DataFrame:
    """Convert column types"""
    return df.astype(type_mapping)


@transform
def filter_rows(df: pd.DataFrame, condition: Callable) -> pd.DataFrame:
    """Filter rows based on condition"""
    return df[condition(df)]


@transform
def aggregate_data(
    df: pd.DataFrame,
    group_by: List[str],
    aggregations: Dict[str, Union[str, List[str]]]
) -> pd.DataFrame:
    """Aggregate data by group"""
    return df.groupby(group_by).agg(aggregations).reset_index()
