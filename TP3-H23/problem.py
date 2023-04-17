import numpy as np


class Solution:
    def __init__(self, zoo: np.array, attraction: float) -> None:
        self.zoo = zoo
        self.attraction = attraction


class Problem:
    def __init__(
        self,
        n: int,
        m: int,
        k: int,
        index_bonus: np.array,
        size_encloser: np.array,
        edge_matrix: np.array,
    ) -> None:
        self.n = n
        self.m = m
        self.k = k
        self.index_bonus = index_bonus
        self.size_encloser = size_encloser
        self.edge_matrix = self.edge_matrix_sym(edge_matrix)

    def edge_matrix_sym(self, edge_matrix: np.array) -> np.array:
        for i in range(self.n):
            for j in range(self.n):
                if j > i:
                    edge_matrix[i][j] = edge_matrix[i][j] + edge_matrix[j][i]
                    edge_matrix[j][i] = edge_matrix[i][j]
        return edge_matrix
