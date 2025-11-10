"""
Data Science Utilities - Pandas helpers, visualization, and statistical analysis
"""

from gen_ai_utils.data_science.pandas_helpers import (
    optimize_dataframe,
    chunked_read_csv,
    profile_dataframe,
    memory_usage_summary
)
from gen_ai_utils.data_science.visualization import (
    quick_plot,
    plot_distribution,
    plot_correlation_matrix,
    plot_time_series
)
from gen_ai_utils.data_science.statistics import (
    detect_outliers,
    calculate_correlation,
    distribution_summary,
    test_normality
)

__all__ = [
    # Pandas helpers
    "optimize_dataframe",
    "chunked_read_csv",
    "profile_dataframe",
    "memory_usage_summary",
    # Visualization
    "quick_plot",
    "plot_distribution",
    "plot_correlation_matrix",
    "plot_time_series",
    # Statistics
    "detect_outliers",
    "calculate_correlation",
    "distribution_summary",
    "test_normality",
]
