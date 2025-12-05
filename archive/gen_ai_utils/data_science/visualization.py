"""
Visualization Utilities - Quick plotting and chart templates

Provides convenient functions for common data visualization tasks using
matplotlib and seaborn with sensible defaults and customization options.
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Tuple, Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns

# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def quick_plot(
    data: pd.DataFrame,
    x: Optional[str] = None,
    y: Optional[str] = None,
    kind: str = 'line',
    title: Optional[str] = None,
    **kwargs
) -> plt.Figure:
    """
    Quick plot with sensible defaults

    Args:
        data: DataFrame to plot
        x: Column name for x-axis
        y: Column name for y-axis
        kind: Plot type ('line', 'bar', 'scatter', 'hist', 'box')
        title: Plot title
        **kwargs: Additional arguments for plotting

    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots()

    if kind == 'line':
        data.plot(x=x, y=y, kind='line', ax=ax, **kwargs)
    elif kind == 'bar':
        data.plot(x=x, y=y, kind='bar', ax=ax, **kwargs)
    elif kind == 'scatter':
        data.plot(x=x, y=y, kind='scatter', ax=ax, **kwargs)
    elif kind == 'hist':
        data[y or x].plot(kind='hist', ax=ax, **kwargs)
    elif kind == 'box':
        data[y or x].plot(kind='box', ax=ax, **kwargs)

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')

    plt.tight_layout()
    return fig


def plot_distribution(
    data: pd.Series,
    title: Optional[str] = None,
    bins: int = 30,
    kde: bool = True
) -> plt.Figure:
    """
    Plot distribution with histogram and KDE

    Args:
        data: Series to plot
        title: Plot title
        bins: Number of bins for histogram
        kde: Whether to show KDE curve

    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots()

    sns.histplot(data, bins=bins, kde=kde, ax=ax)

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    else:
        ax.set_title(f'Distribution of {data.name}', fontsize=14, fontweight='bold')

    ax.set_xlabel(data.name or 'Value', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)

    # Add statistics
    stats_text = f'Mean: {data.mean():.2f}\nMedian: {data.median():.2f}\nStd: {data.std():.2f}'
    ax.text(0.02, 0.98, stats_text,
            transform=ax.transAxes,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    return fig


def plot_correlation_matrix(
    data: pd.DataFrame,
    method: str = 'pearson',
    figsize: Tuple[int, int] = (12, 10),
    cmap: str = 'coolwarm',
    annot: bool = True
) -> plt.Figure:
    """
    Plot correlation matrix heatmap

    Args:
        data: DataFrame with numeric columns
        method: Correlation method ('pearson', 'spearman', 'kendall')
        figsize: Figure size
        cmap: Colormap name
        annot: Whether to annotate cells with values

    Returns:
        Matplotlib figure
    """
    # Calculate correlation matrix
    corr = data.select_dtypes(include=[np.number]).corr(method=method)

    fig, ax = plt.subplots(figsize=figsize)

    # Create heatmap
    sns.heatmap(
        corr,
        annot=annot,
        cmap=cmap,
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8},
        ax=ax,
        fmt='.2f' if annot else None
    )

    ax.set_title(f'Correlation Matrix ({method.capitalize()})',
                 fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    return fig


def plot_time_series(
    data: pd.DataFrame,
    date_column: str,
    value_columns: List[str],
    title: Optional[str] = None,
    rolling_window: Optional[int] = None,
    figsize: Tuple[int, int] = (14, 6)
) -> plt.Figure:
    """
    Plot time series data with optional rolling average

    Args:
        data: DataFrame with time series data
        date_column: Name of date column
        value_columns: List of columns to plot
        title: Plot title
        rolling_window: Window size for rolling average
        figsize: Figure size

    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    for col in value_columns:
        ax.plot(data[date_column], data[col], label=col, alpha=0.7)

        if rolling_window:
            rolling_avg = data[col].rolling(window=rolling_window).mean()
            ax.plot(data[date_column], rolling_avg,
                   label=f'{col} (MA-{rolling_window})',
                   linestyle='--', linewidth=2)

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    else:
        ax.set_title('Time Series Plot', fontsize=14, fontweight='bold')

    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_missing_values(data: pd.DataFrame, figsize: Tuple[int, int] = (12, 6)) -> plt.Figure:
    """
    Visualize missing values in DataFrame

    Args:
        data: DataFrame to analyze
        figsize: Figure size

    Returns:
        Matplotlib figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Missing values heatmap
    sns.heatmap(data.isnull(), cbar=False, yticklabels=False, cmap='viridis', ax=ax1)
    ax1.set_title('Missing Values Pattern', fontsize=12, fontweight='bold')

    # Missing values bar chart
    missing = data.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if len(missing) > 0:
        missing.plot(kind='barh', ax=ax2)
        ax2.set_title('Missing Values Count', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Count', fontsize=10)
    else:
        ax2.text(0.5, 0.5, 'No Missing Values',
                ha='center', va='center',
                fontsize=14, fontweight='bold')
        ax2.axis('off')

    plt.tight_layout()
    return fig


def plot_feature_importance(
    features: List[str],
    importances: List[float],
    top_n: int = 20,
    figsize: Tuple[int, int] = (10, 8)
) -> plt.Figure:
    """
    Plot feature importance

    Args:
        features: List of feature names
        importances: List of importance values
        top_n: Number of top features to show
        figsize: Figure size

    Returns:
        Matplotlib figure
    """
    # Create DataFrame and sort
    df = pd.DataFrame({
        'feature': features,
        'importance': importances
    }).sort_values('importance', ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=figsize)

    sns.barplot(data=df, y='feature', x='importance', ax=ax, palette='viridis')

    ax.set_title(f'Top {top_n} Feature Importances', fontsize=14, fontweight='bold')
    ax.set_xlabel('Importance', fontsize=12)
    ax.set_ylabel('Feature', fontsize=12)

    plt.tight_layout()
    return fig


def plot_categorical_distribution(
    data: pd.Series,
    top_n: Optional[int] = None,
    figsize: Tuple[int, int] = (12, 6)
) -> plt.Figure:
    """
    Plot categorical value distribution

    Args:
        data: Categorical series
        top_n: Show only top N categories
        figsize: Figure size

    Returns:
        Matplotlib figure
    """
    value_counts = data.value_counts()

    if top_n:
        value_counts = value_counts.head(top_n)

    fig, ax = plt.subplots(figsize=figsize)

    value_counts.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')

    ax.set_title(f'Distribution of {data.name}', fontsize=14, fontweight='bold')
    ax.set_xlabel('Category', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.tick_params(axis='x', rotation=45)

    # Add value labels on bars
    for i, v in enumerate(value_counts.values):
        ax.text(i, v, str(v), ha='center', va='bottom')

    plt.tight_layout()
    return fig


def plot_comparison(
    data: pd.DataFrame,
    x: str,
    y: str,
    hue: Optional[str] = None,
    kind: str = 'box',
    figsize: Tuple[int, int] = (12, 6)
) -> plt.Figure:
    """
    Plot comparison between groups

    Args:
        data: DataFrame
        x: Column for x-axis (categorical)
        y: Column for y-axis (numeric)
        hue: Column for color grouping
        kind: Plot type ('box', 'violin', 'bar', 'point')
        figsize: Figure size

    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    if kind == 'box':
        sns.boxplot(data=data, x=x, y=y, hue=hue, ax=ax)
    elif kind == 'violin':
        sns.violinplot(data=data, x=x, y=y, hue=hue, ax=ax)
    elif kind == 'bar':
        sns.barplot(data=data, x=x, y=y, hue=hue, ax=ax)
    elif kind == 'point':
        sns.pointplot(data=data, x=x, y=y, hue=hue, ax=ax)

    ax.set_title(f'{y} by {x}', fontsize=14, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    return fig


def save_plot(fig: plt.Figure, filepath: str, dpi: int = 300, **kwargs):
    """
    Save plot to file

    Args:
        fig: Matplotlib figure
        filepath: Output file path
        dpi: DPI for output
        **kwargs: Additional arguments for savefig
    """
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight', **kwargs)
    print(f"Plot saved to: {filepath}")
