from app import matmul


def as_list(result):
    if hasattr(result, "tolist"):
        return result.tolist()
    return result


def test_square_matrices():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

    result = as_list(matmul(A, B))

    assert result == [[19, 22], [43, 50]]


def test_rectangular_matrices():
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10], [11, 12]]

    result = as_list(matmul(A, B))

    assert result == [[58, 64], [139, 154]]


def test_identity_matrix():
    A = [[3, 7], [2, 5]]
    I = [[1, 0], [0, 1]]

    result = as_list(matmul(A, I))

    assert result == A