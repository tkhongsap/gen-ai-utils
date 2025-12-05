"""
Statistical Analysis Utilities - Outlier detection, correlation, and distribution analysis

Provides common statistical operations for data analysis including outlier
detection, correlation analysis, distribution testing, and hypothesis testing.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from scipy import stats


def detect_outliers(
    data: pd.Series,
    method: str = 'iqr',
    threshold: float = 1.5
) -> pd.Series:
    """
    Detect outliers in a series

    Args:
        data: Series to analyze
        method: Detection method ('iqr', 'zscore', 'modified_zscore')
        threshold: Threshold value (1.5 for IQR, 3 for z-score)

    Returns:
        Boolean series indicating outliers
    """
    if method == 'iqr':
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return (data < lower_bound) | (data > upper_bound)

    elif method == 'zscore':
        z_scores = np.abs(stats.zscore(data.dropna()))
        outliers = pd.Series(False, index=data.index)
        outliers[data.notna()] = z_scores > threshold
        return outliers

    elif method == 'modified_zscore':
        median = data.median()
        mad = np.median(np.abs(data - median))
        modified_z_scores = 0.6745 * (data - median) / mad
        return np.abs(modified_z_scores) > threshold

    else:
        raise ValueError(f"Unknown method: {method}")


def calculate_correlation(
    data: pd.DataFrame,
    method: str = 'pearson',
    threshold: Optional[float] = None
) -> pd.DataFrame:
    """
    Calculate correlation matrix with optional filtering

    Args:
        data: DataFrame with numeric columns
        method: Correlation method ('pearson', 'spearman', 'kendall')
        threshold: Optional threshold to filter weak correlations

    Returns:
        Correlation matrix DataFrame
    """
    numeric_data = data.select_dtypes(include=[np.number])
    corr = numeric_data.corr(method=method)

    if threshold is not None:
        # Filter correlations below threshold (keeping diagonal)
        corr = corr.mask(
            (np.abs(corr) < threshold) & (corr != 1.0),
            np.nan
        )

    return corr


def distribution_summary(data: pd.Series) -> Dict[str, Any]:
    """
    Generate comprehensive distribution summary

    Args:
        data: Series to analyze

    Returns:
        Dictionary with distribution statistics
    """
    clean_data = data.dropna()

    summary = {
        'count': len(clean_data),
        'missing': data.isna().sum(),
        'mean': clean_data.mean(),
        'median': clean_data.median(),
        'mode': clean_data.mode().iloc[0] if len(clean_data.mode()) > 0 else None,
        'std': clean_data.std(),
        'var': clean_data.var(),
        'min': clean_data.min(),
        'max': clean_data.max(),
        'range': clean_data.max() - clean_data.min(),
        'q25': clean_data.quantile(0.25),
        'q50': clean_data.quantile(0.50),
        'q75': clean_data.quantile(0.75),
        'iqr': clean_data.quantile(0.75) - clean_data.quantile(0.25),
        'skewness': stats.skew(clean_data),
        'kurtosis': stats.kurtosis(clean_data),
        'cv': clean_data.std() / clean_data.mean() if clean_data.mean() != 0 else np.nan
    }

    return summary


def test_normality(
    data: pd.Series,
    alpha: float = 0.05
) -> Dict[str, Any]:
    """
    Test for normality using multiple tests

    Args:
        data: Series to test
        alpha: Significance level

    Returns:
        Dictionary with test results
    """
    clean_data = data.dropna()

    results = {}

    # Shapiro-Wilk test
    if len(clean_data) <= 5000:  # Shapiro-Wilk is suitable for smaller samples
        shapiro_stat, shapiro_p = stats.shapiro(clean_data)
        results['shapiro_wilk'] = {
            'statistic': shapiro_stat,
            'p_value': shapiro_p,
            'is_normal': shapiro_p > alpha
        }

    # Kolmogorov-Smirnov test
    ks_stat, ks_p = stats.kstest(
        clean_data,
        'norm',
        args=(clean_data.mean(), clean_data.std())
    )
    results['kolmogorov_smirnov'] = {
        'statistic': ks_stat,
        'p_value': ks_p,
        'is_normal': ks_p > alpha
    }

    # D'Agostino's K-squared test
    if len(clean_data) >= 8:
        dagostino_stat, dagostino_p = stats.normaltest(clean_data)
        results['dagostino_k2'] = {
            'statistic': dagostino_stat,
            'p_value': dagostino_p,
            'is_normal': dagostino_p > alpha
        }

    return results


def confidence_interval(
    data: pd.Series,
    confidence: float = 0.95
) -> Tuple[float, float]:
    """
    Calculate confidence interval for mean

    Args:
        data: Series to analyze
        confidence: Confidence level (default 0.95 for 95%)

    Returns:
        Tuple of (lower_bound, upper_bound)
    """
    clean_data = data.dropna()
    n = len(clean_data)
    mean = clean_data.mean()
    se = stats.sem(clean_data)
    margin = se * stats.t.ppf((1 + confidence) / 2, n - 1)

    return (mean - margin, mean + margin)


def statistical_tests(
    group1: pd.Series,
    group2: pd.Series,
    test_type: str = 'auto',
    alpha: float = 0.05
) -> Dict[str, Any]:
    """
    Perform statistical tests to compare two groups

    Args:
        group1: First group
        group2: Second group
        test_type: Type of test ('auto', 'ttest', 'mannwhitneyu', 'ks')
        alpha: Significance level

    Returns:
        Dictionary with test results
    """
    clean_group1 = group1.dropna()
    clean_group2 = group2.dropna()

    results = {}

    if test_type == 'auto':
        # Check normality
        _, p1 = stats.shapiro(clean_group1) if len(clean_group1) <= 5000 else (0, 0)
        _, p2 = stats.shapiro(clean_group2) if len(clean_group2) <= 5000 else (0, 0)

        if p1 > alpha and p2 > alpha:
            test_type = 'ttest'
        else:
            test_type = 'mannwhitneyu'

        results['selected_test'] = test_type

    if test_type == 'ttest':
        # Independent t-test
        stat, p_value = stats.ttest_ind(clean_group1, clean_group2)
        results['test'] = 't-test'

    elif test_type == 'mannwhitneyu':
        # Mann-Whitney U test (non-parametric)
        stat, p_value = stats.mannwhitneyu(clean_group1, clean_group2)
        results['test'] = 'Mann-Whitney U'

    elif test_type == 'ks':
        # Kolmogorov-Smirnov test
        stat, p_value = stats.ks_2samp(clean_group1, clean_group2)
        results['test'] = 'Kolmogorov-Smirnov'

    else:
        raise ValueError(f"Unknown test type: {test_type}")

    results['statistic'] = stat
    results['p_value'] = p_value
    results['significant'] = p_value < alpha
    results['alpha'] = alpha

    return results


def cramers_v(x: pd.Series, y: pd.Series) -> float:
    """
    Calculate Cramér's V statistic for categorical association

    Args:
        x: First categorical series
        y: Second categorical series

    Returns:
        Cramér's V value (0 to 1)
    """
    confusion_matrix = pd.crosstab(x, y)
    chi2 = stats.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    min_dim = min(confusion_matrix.shape) - 1

    return np.sqrt(chi2 / (n * min_dim))


def calculate_vif(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Variance Inflation Factor (VIF) for multicollinearity detection

    Args:
        data: DataFrame with numeric features

    Returns:
        DataFrame with VIF values
    """
    from statsmodels.stats.outliers_influence import variance_inflation_factor

    numeric_data = data.select_dtypes(include=[np.number])

    vif_data = pd.DataFrame()
    vif_data["Feature"] = numeric_data.columns
    vif_data["VIF"] = [
        variance_inflation_factor(numeric_data.values, i)
        for i in range(numeric_data.shape[1])
    ]

    return vif_data.sort_values('VIF', ascending=False)


def effect_size_cohen_d(group1: pd.Series, group2: pd.Series) -> float:
    """
    Calculate Cohen's d effect size

    Args:
        group1: First group
        group2: Second group

    Returns:
        Cohen's d value
    """
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(), group2.var()

    # Pooled standard deviation
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))

    # Cohen's d
    d = (group1.mean() - group2.mean()) / pooled_std

    return d


def autocorrelation(data: pd.Series, lag: int = 1) -> float:
    """
    Calculate autocorrelation at specified lag

    Args:
        data: Time series data
        lag: Lag value

    Returns:
        Autocorrelation coefficient
    """
    return data.autocorr(lag=lag)


def rolling_statistics(
    data: pd.Series,
    window: int,
    statistics: List[str] = ['mean', 'std', 'min', 'max']
) -> pd.DataFrame:
    """
    Calculate rolling statistics

    Args:
        data: Series to analyze
        window: Rolling window size
        statistics: List of statistics to calculate

    Returns:
        DataFrame with rolling statistics
    """
    result = pd.DataFrame(index=data.index)

    for stat in statistics:
        if stat == 'mean':
            result[f'rolling_mean_{window}'] = data.rolling(window).mean()
        elif stat == 'std':
            result[f'rolling_std_{window}'] = data.rolling(window).std()
        elif stat == 'min':
            result[f'rolling_min_{window}'] = data.rolling(window).min()
        elif stat == 'max':
            result[f'rolling_max_{window}'] = data.rolling(window).max()
        elif stat == 'median':
            result[f'rolling_median_{window}'] = data.rolling(window).median()

    return result
