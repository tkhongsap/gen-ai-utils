"""Model Evaluation utilities for ML/AI models"""

from typing import Dict, Any, List, Optional
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
    mean_squared_error, mean_absolute_error, r2_score
)


def evaluate_classification(y_true: List, y_pred: List, labels: Optional[List[str]] = None) -> Dict[str, Any]:
    """Comprehensive classification evaluation"""
    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
        'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
        'f1_score': f1_score(y_true, y_pred, average='weighted', zero_division=0),
        'confusion_matrix': confusion_matrix(y_true, y_pred).tolist(),
        'classification_report': classification_report(y_true, y_pred, target_names=labels, output_dict=True) if labels else None
    }


def evaluate_regression(y_true: List, y_pred: List) -> Dict[str, float]:
    """Comprehensive regression evaluation"""
    return {
        'mse': mean_squared_error(y_true, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'mae': mean_absolute_error(y_true, y_pred),
        'r2_score': r2_score(y_true, y_pred),
        'mape': np.mean(np.abs((np.array(y_true) - np.array(y_pred)) / np.array(y_true))) * 100
    }


def calculate_metrics(y_true: List, y_pred: List, task: str = 'classification', **kwargs) -> Dict[str, Any]:
    """Calculate metrics based on task type"""
    if task == 'classification':
        return evaluate_classification(y_true, y_pred, **kwargs)
    elif task == 'regression':
        return evaluate_regression(y_true, y_pred)
    else:
        raise ValueError(f"Unknown task: {task}")
