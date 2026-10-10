import numpy as np


def matmul(A, B):
    """
    Multiply two matrices.

    Uses NumPy for optimized execution.
    A pure-Python fallback is available.
    """

    if np is not None:
        return np.matmul(
            np.asarray(A, dtype=np.float64),
            np.asarray(B, dtype=np.float64)
        )

    # Slower pure-Python fallback
    n = len(A)
    k = len(B)
    m = len(B[0])

    C = [[0.0 for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            for p in range(k):
                C[i][j] += A[i][p] * B[p][j]

    return C