"""
Batch Processor - Parallel and distributed batch processing

Provides utilities for processing large datasets in batches with support for
parallel execution, progress tracking, and error handling.
"""

import pandas as pd
from typing import Callable, List, Any, Optional, Iterator, Dict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
import logging
from tqdm import tqdm
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class BatchResult:
    """Result of batch processing"""
    batch_id: int
    success: bool
    records_processed: int
    records_failed: int
    duration_seconds: float
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BatchProcessor:
    """Process data in batches with parallel execution support"""

    def __init__(
        self,
        batch_size: int = 1000,
        max_workers: Optional[int] = None,
        use_processes: bool = False
    ):
        """
        Initialize BatchProcessor

        Args:
            batch_size: Number of records per batch
            max_workers: Maximum number of parallel workers (None for CPU count)
            use_processes: Use ProcessPoolExecutor instead of ThreadPoolExecutor
        """
        self.batch_size = batch_size
        self.max_workers = max_workers or cpu_count()
        self.use_processes = use_processes

    def process_dataframe(
        self,
        df: pd.DataFrame,
        process_func: Callable[[pd.DataFrame], pd.DataFrame],
        show_progress: bool = True
    ) -> pd.DataFrame:
        """
        Process DataFrame in batches

        Args:
            df: DataFrame to process
            process_func: Function to apply to each batch
            show_progress: Whether to show progress bar

        Returns:
            Processed DataFrame
        """
        num_batches = (len(df) + self.batch_size - 1) // self.batch_size
        batches = [
            df.iloc[i:i + self.batch_size]
            for i in range(0, len(df), self.batch_size)
        ]

        results = []
        executor_class = ProcessPoolExecutor if self.use_processes else ThreadPoolExecutor

        with executor_class(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(process_func, batch): i
                for i, batch in enumerate(batches)
            }

            iterator = as_completed(futures)
            if show_progress:
                iterator = tqdm(iterator, total=num_batches, desc="Processing batches")

            for future in iterator:
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Batch processing failed: {str(e)}")
                    raise

        return pd.concat(results, ignore_index=True)

    def process_list(
        self,
        items: List[Any],
        process_func: Callable[[Any], Any],
        show_progress: bool = True
    ) -> List[Any]:
        """
        Process list items in parallel

        Args:
            items: List of items to process
            process_func: Function to apply to each item
            show_progress: Whether to show progress bar

        Returns:
            List of processed items
        """
        executor_class = ProcessPoolExecutor if self.use_processes else ThreadPoolExecutor

        with executor_class(max_workers=self.max_workers) as executor:
            futures = {executor.submit(process_func, item): i for i, item in enumerate(items)}

            results = [None] * len(items)
            iterator = as_completed(futures)

            if show_progress:
                iterator = tqdm(iterator, total=len(items), desc="Processing items")

            for future in iterator:
                try:
                    idx = futures[future]
                    results[idx] = future.result()
                except Exception as e:
                    logger.error(f"Item processing failed: {str(e)}")
                    raise

        return results

    def process_with_results(
        self,
        items: List[Any],
        process_func: Callable[[Any], Any],
        show_progress: bool = True
    ) -> List[BatchResult]:
        """
        Process items and return detailed results for each

        Args:
            items: List of items to process
            process_func: Function to apply to each item
            show_progress: Whether to show progress bar

        Returns:
            List of BatchResult objects
        """
        results = []
        executor_class = ProcessPoolExecutor if self.use_processes else ThreadPoolExecutor

        with executor_class(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._process_with_timing, process_func, item, i): i
                for i, item in enumerate(items)
            }

            iterator = as_completed(futures)
            if show_progress:
                iterator = tqdm(iterator, total=len(items), desc="Processing")

            for future in iterator:
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    batch_id = futures[future]
                    results.append(BatchResult(
                        batch_id=batch_id,
                        success=False,
                        records_processed=0,
                        records_failed=1,
                        duration_seconds=0,
                        error=str(e)
                    ))

        return results

    @staticmethod
    def _process_with_timing(
        process_func: Callable,
        item: Any,
        batch_id: int
    ) -> BatchResult:
        """Process item with timing and result tracking"""
        start_time = datetime.now()

        try:
            result = process_func(item)
            duration = (datetime.now() - start_time).total_seconds()

            # Determine records count
            records_processed = 1
            if isinstance(result, (list, pd.DataFrame)):
                records_processed = len(result)

            return BatchResult(
                batch_id=batch_id,
                success=True,
                records_processed=records_processed,
                records_failed=0,
                duration_seconds=duration
            )
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return BatchResult(
                batch_id=batch_id,
                success=False,
                records_processed=0,
                records_failed=1,
                duration_seconds=duration,
                error=str(e)
            )


def parallel_process(
    items: List[Any],
    func: Callable[[Any], Any],
    max_workers: Optional[int] = None,
    show_progress: bool = True,
    use_processes: bool = False
) -> List[Any]:
    """
    Simple parallel processing function

    Args:
        items: Items to process
        func: Function to apply
        max_workers: Maximum workers (None for CPU count)
        show_progress: Show progress bar
        use_processes: Use processes instead of threads

    Returns:
        List of results

    Example:
        results = parallel_process(urls, fetch_url, max_workers=10)
    """
    max_workers = max_workers or cpu_count()
    executor_class = ProcessPoolExecutor if use_processes else ThreadPoolExecutor

    with executor_class(max_workers=max_workers) as executor:
        futures = {executor.submit(func, item): i for i, item in enumerate(items)}

        results = [None] * len(items)
        iterator = as_completed(futures)

        if show_progress:
            iterator = tqdm(iterator, total=len(items))

        for future in iterator:
            idx = futures[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                logger.error(f"Processing failed for item {idx}: {str(e)}")
                results[idx] = None

    return results


def chunked_process(
    items: List[Any],
    func: Callable[[List[Any]], Any],
    chunk_size: int = 100,
    show_progress: bool = True
) -> List[Any]:
    """
    Process items in chunks

    Args:
        items: Items to process
        func: Function that processes a chunk
        chunk_size: Size of each chunk
        show_progress: Show progress bar

    Returns:
        List of chunk results

    Example:
        # func receives a list of items and returns a result
        results = chunked_process(data, process_batch, chunk_size=500)
    """
    chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

    results = []
    iterator = chunks

    if show_progress:
        iterator = tqdm(chunks, desc="Processing chunks")

    for chunk in iterator:
        try:
            result = func(chunk)
            results.append(result)
        except Exception as e:
            logger.error(f"Chunk processing failed: {str(e)}")
            results.append(None)

    return results


def batch_generator(
    items: List[Any],
    batch_size: int
) -> Iterator[List[Any]]:
    """
    Generate batches from a list

    Args:
        items: List of items
        batch_size: Size of each batch

    Yields:
        Batch of items

    Example:
        for batch in batch_generator(large_list, 100):
            process(batch)
    """
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


def dataframe_batch_generator(
    df: pd.DataFrame,
    batch_size: int
) -> Iterator[pd.DataFrame]:
    """
    Generate DataFrame batches

    Args:
        df: DataFrame to split
        batch_size: Rows per batch

    Yields:
        DataFrame batch

    Example:
        for batch_df in dataframe_batch_generator(large_df, 1000):
            process(batch_df)
    """
    for i in range(0, len(df), batch_size):
        yield df.iloc[i:i + batch_size]
