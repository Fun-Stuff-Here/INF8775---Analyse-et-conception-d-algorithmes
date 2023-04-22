# source : https://www.geeksforgeeks.org/prims-minimum-spanning-tree-mst-greedy-algo-5/
# Prim's Minimum Spanning Tree (MST) algorithm.
import sys
import numpy as np
from problem import Problem
from node import TreeNode
from encloser import Encloser


class Graph:
    def __init__(self, problem: Problem):
        self.V = problem.n
        self.nodes = {}
        self.problem = problem

    def get_children(self, parent_index: int, parent: list) -> list:
        children = []
        for i in range(self.V):
            if parent[i] == parent_index:
                children.append(i)
        return children

    def printMST(self, parent: list) -> TreeNode:
        nodes = [
            TreeNode(
                encloser=Encloser(i, self.problem.size_encloser[i]),
                children=[],
                parent=None,
            )
            for i in range(self.V)
        ]

        for node_index in range(self.V):
            nodes[node_index].parent = (
                nodes[parent[node_index]] if parent[node_index] != -1 else None
            )
            children_indexes = self.get_children(node_index, parent)
            nodes[node_index].children = [
                nodes[child_index] for child_index in children_indexes
            ]

        return nodes[0]

    def minKey(self, key: int, mstSet: np.array):
        # Initialize min value
        min = sys.maxsize

        for v in range(self.V):
            if key[v] < min and mstSet[v] == False:
                min = key[v]
                min_index = v

        return min_index

    def primMST(self) -> TreeNode:
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


def get_root_tree(problem: Problem) -> np.array:
    g = Graph(problem)
    return g.primMST()
