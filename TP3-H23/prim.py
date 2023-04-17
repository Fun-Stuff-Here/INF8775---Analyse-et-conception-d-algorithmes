# source : https://www.geeksforgeeks.org/prims-minimum-spanning-tree-mst-greedy-algo-5/
# Prim's Minimum Spanning Tree (MST) algorithm.
import sys
import numpy as np
from problem import Problem


class Graph:
    def __init__(self, problem: Problem):
        self.V = problem.edge_matrix.shape[0]
        self.nodes = {}
        self.problem = problem

    def printMST(self, parent: list) -> np.array:
        for i in range(1, self.V):
            if parent[i] not in self.nodes:
                self.nodes[parent[i]] = []
            self.nodes[parent[i]].append(
                {
                    "child": i,
                }
            )

        stack = [0]
        result = []
        while len(stack) > 0:
            current = stack.pop()
            result.append(current)
            if current in self.nodes:
                for child in self.nodes[current]:
                    stack.append(child["child"])
        return result

    def minKey(self, key: int, mstSet: np.array):
        # Initialize min value
        min = sys.maxsize

        for v in range(self.V):
            if key[v] < min and mstSet[v] == False:
                min = key[v]
                min_index = v

        return min_index

    def primMST(self) -> np.array:
        key = [sys.maxsize] * self.V
        parent = [None] * self.V
        key[0] = 0
        mstSet = [False] * self.V
        parent[0] = -1
        for cout in range(self.V):
            u = self.minKey(key, mstSet)
            mstSet[u] = True
            for v in range(self.V):
                uv_distance = self.problem.edge_matrix[u][v]
                if uv_distance > 0 and mstSet[v] == False and key[v] > uv_distance:
                    key[v] = uv_distance
                    parent[v] = u

        return self.printMST(parent)


def get_filling_order(problem: Problem) -> np.array:
    g = Graph(problem)
    return g.primMST()
