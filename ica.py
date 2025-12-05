"""ICA - SciCode Task 31"""

import numpy as np
import numpy.linalg as la
from scipy import signal


def center(X, divide_sd=True):
    """Subquestion 31_31.1: Standardize matrix X along rows."""
    D = X - np.mean(X, axis=1, keepdims=True)
    if divide_sd:
        D = D / np.std(X, axis=1, keepdims=True)
    return D


def whiten(X):
    """Subquestion 31_31.2: Whiten matrix X (covariance = identity)."""
    X_centered = X - np.mean(X, axis=1, keepdims=True)
    cov = np.cov(X_centered)
    eigenvalues, eigenvectors = la.eigh(cov)
    D_inv_sqrt = np.diag(1.0 / np.sqrt(eigenvalues))
    whitening_matrix = D_inv_sqrt @ eigenvectors.T
    Z = whitening_matrix @ X_centered
    return Z


def ica(X, cycles, tol):
    """Subquestion 31_31.3: Perform ICA using FastICA."""
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


def create_signals(N=2000):
    """Create test signals for ICA (Test 4)."""
    time = np.linspace(0, 8, N)
    s1 = np.sin(2 * time)
    s2 = 2 * np.sign(np.sin(3 * time))
    s3 = 4 * signal.sawtooth(2 * np.pi * time)
    S = np.array([s1, s2, s3])
    A = np.array([[1, 1, 1], [0.5, 2, 1], [1.5, 1, 2]])
    X = A @ S
    return X, S


def test_identity(A):
    return np.allclose(A, np.eye(A.shape[0]))


X_test = np.array([
    [-4., -1.25837414, -4.2834508, 4.22567322, 1.43150983, -6.28790332],
    [-4., -3.22918707, -6.3417254, 6.31283661, 3.31575491, -8.14395166],
    [-8., -0.48756122, -6.62517619, 6.53850983, 0.74726474, -10.43185497]
])


if __name__ == "__main__":
    print("=== 31_31.1: center() ===")
    print(center(X_test), "\n")

    print("=== 31_31.2: whiten() ===")
    Z = whiten(X_test)
    print(f"Cov=I: {test_identity(np.cov(Z))}")
    print(Z, "\n")

    print("=== 31_31.3: ica() ===")
    np.random.seed(0)
    print(ica(X_test, cycles=200, tol=1e-5), "\n")

    print("=== 31_31.3 Test 4: Synthetic ===")
    np.random.seed(0)
    X, S = create_signals(N=2000)
    S_hat = ica(X, cycles=200, tol=1e-5)
    corr = np.abs(np.corrcoef(S_hat, S)[:3, 3:])
    print(f"Recovery: {np.mean(np.max(corr, axis=1)):.4f}")
