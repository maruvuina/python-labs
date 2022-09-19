import numpy as np

def decorate_matrix_classic_version(dimension):
    matrix = [[0] * dimension for _ in range(dimension)]
    for i in range(dimension):
        for j in range(dimension):
            if (i == 0):
                matrix[i][j] = 1
            elif (i == dimension-1):
                matrix[i][j] = 1
            elif (j == 0):
                matrix[i][j] = 1
            elif (j == dimension-1):
                matrix[i][j] = 1
    return matrix            


def decorate_matrix_numpy_version(dimension):
    matrix = np.zeros((dimension, dimension))
    matrix[0] = matrix[:, :1] = matrix[:, dimension-1:dimension] = matrix[dimension-1] = 1
    return matrix


def main():
    dimension = 6
    print("Classic version")
    matrix = decorate_matrix_classic_version(dimension)
    print(matrix)
    print("\nNumpy version")
    matrix = decorate_matrix_numpy_version(dimension)
    print(matrix)


main()