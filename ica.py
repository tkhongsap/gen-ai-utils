"""
Independent Component Analysis (ICA) Implementation
SciCode Benchmark Task 31
"""

import numpy as np
import numpy.linalg as la
from scipy import signal


def center(X, divide_sd=True):
    '''Center the input matrix X and optionally scale it by the standard deviation.

    Args:
        X (np.ndarray): The input matrix of shape (nmix, time).
        divide_sd (bool): If True, divide by the standard deviation. Defaults to True.

    Returns:
        np.ndarray: The centered (and optionally scaled) matrix of the same shape as the input.
    '''
    D = X - np.mean(X, axis=1, keepdims=True)
    if divide_sd:
        D = D / np.std(X, axis=1, keepdims=True)
    return D


def whiten(X):
    '''Whiten matrix X so that covariance of output equals identity.

    Args:
        X (np.array): mixture matrix. Shape (nmix, time)

    Return:
        Z (np.array): whitened matrix. Shape (nmix, time)
    '''
    X_centered = X - np.mean(X, axis=1, keepdims=True)
    cov = np.cov(X_centered)
    eigenvalues, eigenvectors = la.eigh(cov)
    D_inv_sqrt = np.diag(1.0 / np.sqrt(eigenvalues))
    whitening_matrix = D_inv_sqrt @ eigenvectors.T
    Z = whitening_matrix @ X_centered
    return Z


def ica(X, cycles, tol):
    '''Perform independent component analysis using FastICA algorithm.

    Args:
        X (np.array): mixture matrix. Shape (nmix, time)
        cycles (int): number of max possible iterations
        tol (float): convergence tolerance

    Returns:
        S_hat (np.array): predicted independent sources. Shape (nmix, time)
    '''
    X_whitened = whiten(X)
    n_components, n_samples = X_whitened.shape
    W = np.zeros((n_components, n_components))

    for i in range(n_components):
        w = np.random.randn(n_components)
        w = w / la.norm(w)

        for _ in range(cycles):
            w_old = w.copy()

            wx = w @ X_whitened
            g_wx = np.tanh(wx)
            dg_wx = 1 - g_wx ** 2

            w = np.mean(X_whitened * g_wx, axis=1) - np.mean(dg_wx) * w

            for j in range(i):
                w = w - np.dot(w, W[j]) * W[j]

            w = w / la.norm(w)

            if la.norm(w - w_old) < tol:
                break

        W[i] = w

    S_hat = W @ X_whitened
    return S_hat


def create_test_signals(N=2000):
    '''Create test signals for ICA validation.'''
    time = np.linspace(0, 8, N)
    s1 = np.sin(2 * time)
    s2 = 2 * np.sign(np.sin(3 * time))
    s3 = 4 * signal.sawtooth(2 * np.pi * time)
    S = np.array([s1, s2, s3])
    A = np.array([[1, 1, 1], [0.5, 2, 1], [1.5, 1, 2]])
    X = A @ S
    return X, S, A


def test_center():
    X = np.array([[1, 2, 3, 4, 5], [10, 20, 30, 40, 50]])
    D = center(X, divide_sd=False)
    assert np.allclose(np.mean(D, axis=1), 0)
    assert D.shape == X.shape
    print("test_center: PASS")


def test_whiten():
    np.random.seed(42)
    X = np.random.randn(3, 100)
    Z = whiten(X)
    assert np.allclose(np.cov(Z), np.eye(3), atol=1e-10)
    assert Z.shape == X.shape
    print("test_whiten: PASS")


def test_ica():
    np.random.seed(0)
    X, S_original, _ = create_test_signals(N=2000)
    S_hat = ica(X, cycles=200, tol=1e-5)
    assert S_hat.shape == X.shape
    correlations = np.abs(np.corrcoef(S_hat, S_original)[:3, 3:])
    recovery_quality = np.mean(np.max(correlations, axis=1))
    assert recovery_quality > 0.9, f"Recovery quality: {recovery_quality:.4f}"
    print(f"test_ica: PASS (recovery: {recovery_quality:.4f})")


if __name__ == "__main__":
    test_center()
    test_whiten()
    test_ica()
    print("All tests passed!")
